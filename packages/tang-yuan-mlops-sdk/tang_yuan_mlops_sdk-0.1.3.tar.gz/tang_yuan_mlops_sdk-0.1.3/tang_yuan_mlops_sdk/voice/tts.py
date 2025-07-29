# mlops_sdk/voice/tts.py
import asyncio
from typing import Optional

import httpx
from httpx import ReadTimeout

from tang_yuan_mlops_sdk.core.http_client import BaseAsyncClient


class TTSClient(BaseAsyncClient):
    """
    用于和文本转语音(TTS)服务交互的客户端
    """

    async def synthesize(self, tts_text: str, spk_id: str, endpoint: str = "inference_sft",
                         params: Optional[dict] = None) -> bytes:
        """
        通过 GET 请求流式返回音频
        :param tts_text: 合成文本
        :param spk_id:   说话人ID
        :param endpoint: 接口后缀, 默认 "inference_sft"
        :param params:   额外的get参数(如果需要)
        :return:         合成后的语音的原始二进制流
        """
        if params is None:
            params = {}
        params.update({
            "tts_text": tts_text,
            "spk_id": spk_id
        })

        retries = 3
        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    url = f"{self.base_url}/{endpoint}"
                    async with client.stream("GET", url, data=params) as response:
                        response.raise_for_status()
                        audio_bytes = b""
                        async for chunk in response.aiter_bytes():
                            audio_bytes += chunk
                        return audio_bytes
            except ReadTimeout:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
