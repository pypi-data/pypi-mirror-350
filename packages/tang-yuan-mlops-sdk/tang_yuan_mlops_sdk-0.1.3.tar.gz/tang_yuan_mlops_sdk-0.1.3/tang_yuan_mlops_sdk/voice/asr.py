# mlops_sdk/voice/asr.py

from tang_yuan_mlops_sdk.core.http_client import BaseAsyncClient

class ASRClient(BaseAsyncClient):
    """
    用于和语音识别(ASR)服务交互的客户端
    """

    async def recognize(self, file_bytes: bytes, filename="demo.wav") -> dict:
        """
        :param file_bytes: wav文件的二进制内容
        :param filename:   文件名, 默认 "demo.wav"
        :return:           服务端返回的 JSON
        """
        files = {
            "file": (filename, file_bytes, "audio/wav")
        }
        return await self.post_file("recognize", files)