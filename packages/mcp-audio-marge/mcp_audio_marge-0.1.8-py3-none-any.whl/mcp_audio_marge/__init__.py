import asyncio
import httpx
import json # 导入 json 模块
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, HttpUrl, ValidationError # 导入 ValidationError
from typing import List, Optional

# 定义 marge-server API 的基础 URL
import os

# 定义 marge-server API 的基础 URL，从环境变量读取，默认为 http://localhost:8000
MARGE_SERVER_BASE_URL = os.environ.get("MARGE_SERVER_BASE_URL", "http://localhost:8000")

# 定义音频合成请求的 Pydantic 模型
class AudioSynthesisRequest(BaseModel):
    audio_urls: List[HttpUrl] = Field(..., description="需要合成的音频 URL 列表")
    output_filename: Optional[str] = Field("synthesized_audio.mp3", description="期望的合成后音频输出文件名")

# 初始化 FastMCP Server
mcp = FastMCP("AudioSynthesisServer")

@mcp.tool()
async def synthesize_audio(request: AudioSynthesisRequest | str, ctx: Context) -> str: # 允许 request 为字符串类型
    """
    提交音频合成任务并返回下载地址。

    Args:
        request: 包含音频 URL 列表和输出文件名的请求对象。
        ctx: FastMCP 上下文对象。

    Returns:
        合成音频的下载地址。
    """
    # 检查并解析 request 参数
    if isinstance(request, str):
        try:
            request_data = json.loads(request)
            request = AudioSynthesisRequest.model_validate(request_data)
            await ctx.info("成功解析并验证字符串化 request 参数")
        except json.JSONDecodeError as e:
            await ctx.error(f"解析 request 字符串失败: {e}")
            return f"错误: 无效的 request 参数格式 - {e}"
        except ValidationError as e:
            await ctx.error(f"验证解析后的 request 数据失败: {e}")
            return f"错误: request 数据不符合 AudioSynthesisRequest 模型 - {e}"
        except Exception as e:
            await ctx.error(f"处理字符串化 request 参数时发生未知错误: {e}")
            return f"错误: 处理 request 参数时发生未知错误 - {e}"
    elif not isinstance(request, AudioSynthesisRequest):
         await ctx.error(f"接收到非预期的 request 参数类型: {type(request)}")
         return f"错误: 接收到非预期的 request 参数类型: {type(request)}"

    # 确保 request 现在是 AudioSynthesisRequest 实例
    if not isinstance(request, AudioSynthesisRequest):
         # 这应该不会发生，但作为安全检查
         await ctx.error("request 参数未能转换为 AudioSynthesisRequest 实例")
         return "错误: 内部错误，无法处理 request 参数"

    async with httpx.AsyncClient() as client:
        # 1. 提交音频合成任务
        submit_url = f"{MARGE_SERVER_BASE_URL}/api/v1/audio/synthesize"
        try:
            await ctx.info(f"提交合成任务到: {submit_url}")
            
            # 将 AudioSynthesisRequest 转换为字典，并手动处理 HttpUrl 字段
            request_data = request.model_dump()
            if 'audio_urls' in request_data and isinstance(request_data['audio_urls'], list):
                # 确保列表中的每个元素都是 HttpUrl 对象，然后转换为字符串
                request_data['audio_urls'] = [str(url) for url in request_data['audio_urls'] if isinstance(url, HttpUrl)]

            response = await client.post(submit_url, json=request_data) # 使用处理后的字典
            response.raise_for_status() # 检查 HTTP 错误
            task_ticket = response.json()
            task_id = task_ticket.get("task_id")
            await ctx.info(f"任务提交成功，任务 ID: {task_id}")
        except httpx.HTTPStatusError as e:
            await ctx.error(f"提交合成任务失败: HTTP 错误 {e.response.status_code} - {e.response.text}")
            # 考虑抛出自定义异常或返回结构化错误
            return f"错误: 提交合成任务失败 - {e.response.status_code}"
        except httpx.RequestError as e:
            await ctx.error(f"提交合成任务失败: 请求错误 - {e}")
            # 考虑抛出自定义异常或返回结构化错误
            return f"错误: 提交合成任务失败 - {e}"
        except Exception as e:
            await ctx.error(f"提交合成任务失败: 未知错误 - {e}")
            # 考虑抛出自定义异常或返回结构化错误
            return f"错误: 提交合成任务失败 - {e}"

        if not task_id:
            await ctx.error("提交合成任务成功但未返回 task_id")
            # 考虑抛出自定义异常或返回结构化错误
            return "错误: 未获取到任务 ID"

        # 2. 轮询任务状态
        status_url_template = f"{MARGE_SERVER_BASE_URL}/api/v1/audio/status/{{task_id}}"
        status_url = status_url_template.format(task_id=task_id)
        # 设置轮询超时时间 (例如 5 分钟)
        polling_timeout = 300 # seconds
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < polling_timeout:
            await asyncio.sleep(2) # 每隔 2 秒轮询一次
            try:
                await ctx.info(f"查询任务状态 (任务 ID: {task_id}): {status_url}")
                status_response = await client.get(status_url)
                status_response.raise_for_status() # 检查 HTTP 错误
                task_status = status_response.json()
                status = task_status.get("status")
                await ctx.info(f"任务 ID {task_id} 当前状态: {status}")

                if status == "finished":
                    result_data = task_status.get("result", {})
                    download_url = result_data.get("download_url")
                    file_path = result_data.get("file_path") # 尝试从 file_path 提取文件名

                    if download_url:
                        await ctx.info(f"任务完成，下载地址: {download_url}")
                        return download_url
                    elif file_path:
                         # 如果没有直接的 download_url，尝试构建一个
                         # 需要从 file_path 中提取文件名
                         filename = file_path.split("/")[-1] if "/" in file_path else file_path
                         manual_download_url = f"{MARGE_SERVER_BASE_URL}/api/v1/audio/download/{task_id}/{filename}"
                         await ctx.info(f"任务完成，从 file_path 构建下载地址: {manual_download_url}")
                         return manual_download_url
                    else:
                        await ctx.error(f"任务完成但未获取到下载地址或文件路径: {task_status}")
                        # 可以考虑抛出更具体的异常
                        return "错误: 未获取到下载地址或文件路径"
                elif status == "failed":
                    error_info = task_status.get("error", {})
                    await ctx.error(f"任务失败: {error_info}")
                    # 可以考虑抛出更具体的异常
                    return f"错误: 任务失败 - {error_info.get('message', '未知错误')}"
                elif status not in ["queued", "started", "deferred"]:
                     await ctx.warning(f"任务状态未知或异常: {status}")
                     # 可以考虑抛出更具体的异常
                     return f"错误: 任务状态未知或异常 - {status}"

            except httpx.HTTPStatusError as e:
                await ctx.error(f"查询任务状态失败: HTTP 错误 {e.response.status_code} - {e.response.text}")
                # 可以在这里增加重试逻辑
                # return f"错误: 查询任务状态失败 - {e.response.status_code}" # 不立即返回，继续轮询直到超时
            except httpx.RequestError as e:
                await ctx.error(f"查询任务状态失败: 请求错误 - {e}")
                # 可以在这里增加重试逻辑
                # return f"错误: 查询任务状态失败 - {e}" # 不立即返回，继续轮询直到超时
            except Exception as e:
                await ctx.error(f"查询任务状态失败: 未知错误 - {e}")
                # 可以在这里增加重试逻辑
                # return f"错误: 查询任务状态失败 - {e}" # 不立即返回，继续轮询直到超时

        # 轮询超时
        await ctx.error(f"任务 {task_id} 轮询超时")
        # 可以考虑抛出更具体的异常
        return "错误: 任务轮询超时"


if __name__ == "__main__":
    # 运行 FastMCP Server，使用 Streamable HTTP transport
    mcp.run(transport="streamable-http", host="127.0.0.1", port=58001) # 使用不同的端口避免冲突