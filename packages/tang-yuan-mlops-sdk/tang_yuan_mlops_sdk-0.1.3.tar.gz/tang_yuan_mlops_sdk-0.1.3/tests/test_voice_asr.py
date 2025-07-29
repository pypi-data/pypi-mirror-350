# tests/test_voice_asr.py

import pytest
from tang_yuan_mlops_sdk.voice.asr import ASRClient

@pytest.mark.asyncio
async def test_asr():
    client = ASRClient(base_url="http://222.186.32.152:10003")
    # 读取本地 demo.wav
    with open("demo_tts.wav", "rb") as f:
        file_bytes = f.read()

    response = await client.recognize(file_bytes)
    assert response is not None
    print("Status:", "ok")
    print("Response:", response)