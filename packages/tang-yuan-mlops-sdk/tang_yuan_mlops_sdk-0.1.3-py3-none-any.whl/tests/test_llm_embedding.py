# tests/test_llm_rerank.py

import pytest
from tang_yuan_mlops_sdk.llm.embedding import EmbeddingClient

@pytest.mark.asyncio
async def test_embedding():
    client = EmbeddingClient(base_url="http://222.186.32.152:10001", token="aB3fG7kL9mN1pQ5rS8tU2vW4xYz0Aa")

    texts = ["Deep Learning is not...", "Deep learning is..."]
    response = await client.get_embeddings(texts)

    assert response is not None
    print("Status:", "ok")
    print("Response:", response)