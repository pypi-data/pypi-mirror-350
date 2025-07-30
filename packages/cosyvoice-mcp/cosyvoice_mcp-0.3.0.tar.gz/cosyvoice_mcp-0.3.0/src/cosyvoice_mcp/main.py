from typing import Annotated
from pydantic import Field
from dashscope.audio.tts_v2 import SpeechSynthesizer
from fastmcp import FastMCP
import base64
import logging
logging.basicConfig(level=logging.INFO)
logging.info("Initializing FastMCP...")

mcp = FastMCP("CosyVoice TTS Server")
logging.info("FastMCP initialized")

@mcp.tool(
    name="text_to_speech",
    description="调用百炼平台CosyVoice V2进行语音合成",
)
def text_to_speech(
    text: Annotated[str, Field(description="待合成文本", max_length=2000)],
    voice_type: Annotated[
        str, 
        Field(description="音色类型", max_length=20)
    ] = "longxiaocheng_v2"
) -> dict:
    """语音合成工具（支持实时性能监控）[4,5](@ref)
    
    参数说明：
    - text: 支持中/英/日/韩/粤语混合文本（最大2000字符）
    - voice_type: 预设音色（longxiaochun_v2/晓辰，longxiaoyu_v2/晓雨等）
    - format: 输出音频格式（wav或mp3）
    
    返回结构：
    - 成功：{"status": "success", "audio": bytes, "metrics": {...}}
    - 失败：{"status": "error", "message": "错误详情"}
    """
    try:
        # 初始化语音合成器（网页6的API调用方式）
        synthesizer = SpeechSynthesizer(
            model="cosyvoice-v2",
            voice=voice_type,
        )
        
        # 执行同步合成（网页4推荐生产环境用同步模式）
        audio_data = synthesizer.call(text)
        
        # 返回结构包含性能指标（网页5的性能监控建议）
        return {
            "request_id": synthesizer.get_last_request_id(),
            "output": {
                "audio": {
                    "data": base64.b64encode(audio_data).decode("utf-8"),
                    "mime_type": "audio/mpeg",
                    "file_name": f"{text[:10]}_{voice_type}.mp3"
                },
                "metrics": {
                    "first_byte_latency": synthesizer.get_first_package_delay(),
                    "text_length": len(text)
                }
            }
        }
    
    except Exception as e:
        # 错误处理（网页4的异常处理规范）
        error_msg = str(e)
        if "QuotaExhausted" in error_msg:
            error_msg = "API调用配额不足，请联系管理员"
        elif "InvalidParameter" in error_msg:
            error_msg = "参数校验失败，请检查音色/格式参数"
            
        return {
            "status": "error",
            "message": error_msg,
            "error_code": getattr(e, "code", "UNKNOWN_ERROR")
        }


mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)

# DASHSCOPE_API_KEY=sk-xxx fastmcp run src/cosyvoice_mcp/main.py