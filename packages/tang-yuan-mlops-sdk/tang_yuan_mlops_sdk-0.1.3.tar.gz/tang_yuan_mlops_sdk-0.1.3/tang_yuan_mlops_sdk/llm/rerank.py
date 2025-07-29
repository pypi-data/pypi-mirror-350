# mlops_sdk/llm/rerank.py

from typing import List
from tang_yuan_mlops_sdk.core.http_client import BaseAsyncClient

class RerankClient(BaseAsyncClient):
    """
    用于和 Rerank 服务交互的客户端
    """

    async def rerank(self, query: str, texts: List[str]) -> dict:
        """
        :param query: 查询问题
        :param texts: 待重排序的文本列表
        :return: 服务端返回的 JSON 解析后结果
        """
        payload = {
            "query": query,
            "texts": texts
        }
        return await self.post("rerank", payload)