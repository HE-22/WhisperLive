from whisper_live.client import TranscriptionClient

CLOUD_RUN_WS_URL: str = "wss://whisper-live-cpu-linux-amd64-m4qdxgpsza-uc.a.run.app"
MOCK_WS_URL: str = "ws://localhost:8765"
HLS_URL = "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_1xtra/bbc_1xtra.isml/bbc_1xtra-audio%3d96000.norewind.m3u8"
PATH_TO_AUDIO: str = "my_code/live_translation/audio/1xtra.mp3"
# HLS_URL: str = "http://127.0.0.1:8000/hls/stream.m3u8"

transcription_client: TranscriptionClient = TranscriptionClient(
    cloud_run_url=MOCK_WS_URL, lang="en", translate=False, is_multilingual=True
)

transcription_client(hls_url=HLS_URL)
