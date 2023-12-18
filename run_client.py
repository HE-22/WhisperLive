from whisper_live.client import TranscriptionClient

HOST = "localhost"
PORT = 9090

transcription_client: TranscriptionClient = TranscriptionClient(
    HOST, PORT, is_multilingual=True, lang="en", translate=False
)


# SOCKET_URI: str = "ws://localhost:8765/socket/ad617927-0e9e-4f63-ad1f-910fdd10889f"

HLS_URL: str = "http://127.0.0.1:8000/hls/stream.m3u8"
# hls_url = "http://as-hls-ww-live.akamaized.net/pool_904/live/ww/bbc_1xtra/bbc_1xtra.isml/bbc_1xtra-audio%3d96000.norewind.m3u8"


transcription_client(hls_url=HLS_URL)
