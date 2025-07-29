# tests/test_llm_rerank.py

import pytest
from tang_yuan_mlops_sdk.llm.rerank import RerankClient

@pytest.mark.asyncio
async def test_rerank():
    client = RerankClient(base_url="http://222.186.32.152:10002", token="aB3fG7kL9mN1pQ5rS8tU2vW4xYz0Aa")

    query = "What is Deep Learning?"
    texts = ["Deep Learning is not...", "Deep learning is..."]
    response = await client.rerank(query, texts)

    assert response is not None
    print("Status:", "ok")
    print("Response:", response)