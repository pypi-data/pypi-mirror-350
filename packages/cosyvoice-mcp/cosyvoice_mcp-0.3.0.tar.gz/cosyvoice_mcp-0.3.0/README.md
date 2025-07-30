# cosyvoice-mcp
A Python-based MCP server for integrating CosyVoice TTS with the Baichuan platform.

## Installation
```bash
pip install cosyvoice-mcp
```

## Usage
```bash
DASHSCOPE_API_KEY=sk-xxx cosyvoice-mcp
```

## Features
Supports JSON-RPC over HTTP (streamable-http)
Compatible with FastMCP and DashScope TTS
Base64-encoded audio output


## Request
- url: http://localhost:8000/mcp/tools/text_to_speech
- method: POST

## Parameters
- text: text string to  be synthesized
- voice_type: Such as the enumeration value of longxiaocheng_v2. Please refer to https://help.aliyun.com/zh/model-studio/cosyvoice-python-api?spm=a2c4g.11186623.0.i2#fbe0209896w38

## 返回
```json
{
  "request_id": "7f6da1729d7345babb976d497f8bfaaa",
  "output": {
    "audio": {
      "data": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Lj...", //base64 encoded audio
      "mime_type": "audio/mpeg",
      "file_name": "哈哈_longxiaocheng_v2.mp3"
    },
    "metrics": {
      "first_byte_latency": 738.578125,
      "text_length": 2
    }
  }
}
```