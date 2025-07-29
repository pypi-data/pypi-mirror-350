# mlops_sdk/llm/embedding.py

from typing import List
from tang_yuan_mlops_sdk.core.http_client import BaseAsyncClient

class EmbeddingClient(BaseAsyncClient):
    """
    用于和 Embedding 服务交互的客户端
    """

    async def get_embeddings(self, texts: List[str]) -> dict:
        """
        :param texts: 输入的文本列表
        :return: 返回服务端 JSON 解析后的结果
        """
        payload = {"inputs": texts}
        # endpoint 只写后半部分，例如 "embed"
        return await self.post("embed", payload)