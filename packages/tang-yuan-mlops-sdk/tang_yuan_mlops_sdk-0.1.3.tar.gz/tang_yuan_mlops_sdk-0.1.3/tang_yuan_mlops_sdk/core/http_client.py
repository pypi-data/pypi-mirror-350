# mlops_sdk/core/http_client.py

import httpx
from typing import Any, Dict, Optional

class BaseAsyncClient:
    def __init__(self, base_url: str, token: str = ""):
        """
        :param base_url: 服务端的基础 URL, 例如: "http://222.186.32.152:10001"
        :param token:    Bearer Token, 用于鉴权
        """
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def post(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的POST请求封装
        """
        headers = {
            "Content-Type": "application/json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint}"
            resp = await client.post(url, json=json_data, headers=headers)
            resp.raise_for_status()  # 如果非 2xx，会抛出异常
            return resp.json()

    async def post_file(self, endpoint: str, files: Dict[str, Any]) -> Dict[str, Any]:
        """
        统一的POST请求封装(文件上传)
        """
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint}"
            resp = await client.post(url, files=files, headers=headers)
            resp.raise_for_status()
            return resp.json()

    async def get_stream(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        用于流式返回语音或其他流数据的异步 get
        """
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint}"
            async with client.stream("GET", url, params=params, headers=headers) as resp:
                resp.raise_for_status()
                return resp
