from whisper_live.client import TranscriptionClient


client = TranscriptionClient(
    "localhost", 9090, is_multilingual=True, lang="hi", translate=True
)


client(
    "/Users/hassen/Dev/Jeenie/whisper-live-fork/WhisperLive/my_code/assets/audio/Multilingual test.m4a"
)
