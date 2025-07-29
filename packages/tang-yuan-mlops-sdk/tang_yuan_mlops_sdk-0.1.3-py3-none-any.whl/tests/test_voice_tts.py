# tests/test_voice_tts.py

import numpy as np
import pytest
import scipy.io.wavfile as wavfile

from tang_yuan_mlops_sdk.voice.tts import TTSClient


@pytest.mark.asyncio
async def test_tts():
    client = TTSClient(base_url="http://222.186.32.152:10004")

    tts_text = "你好，我是通义千问语音合成大模型.哈哈哈哈"
    spk_id = "中文女"
    audio_bytes = await client.synthesize(tts_text, spk_id, endpoint="inference_sft", params={})

    # 转换为 tensor
    tts_speech = np.frombuffer(audio_bytes, dtype=np.int16)
    # 写出到本地
    wavfile.write("demo_tts.wav", 22050, tts_speech)
    # wavfile.write("demo_tts.wav", 16000, tts_speech)

    assert len(audio_bytes) > 0
    print("Status:", "ok")
    print("Audio length:", len(audio_bytes))