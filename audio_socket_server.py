import asyncio
import json
from collections import defaultdict
import websockets
from io import BytesIO
import logging

from whisper_live.client import Client

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

HOST = "localhost"
PORT = 8765

# Dictionary to store buffers for each stream
audio_buffers = defaultdict(BytesIO)

# Dictionary to store TranscriptionClients for each stream
transcription_clients_dict = {}


async def handle_audio(websocket, path):
    """
    Handles incoming audio stream via WebSocket and sends it for transcription.
    Each WebSocket connection is handled separately based on the path.
    """
    stream_id = path
    transcription_client = get_or_create_transcription_client(stream_id)

    try:
        async for message in websocket:
            await process_message(message, stream_id, transcription_client)
    except Exception as e:
        logging.error("Error occurred in handle_audio: %s", e, exc_info=True)
    finally:
        cleanup_resources(stream_id)


def get_or_create_transcription_client(stream_id) -> Client:
    """
    Get an existing TranscriptionClient or create a new one for the given stream_id.
    """
    if stream_id not in transcription_clients_dict:
        transcription_clients_dict[stream_id] = Client(
            HOST, PORT, is_multilingual=True, lang="en", translate=False
        )
    return transcription_clients_dict[stream_id]


async def process_message(message, stream_id, transcription_client):
    """
    Process a single message from the WebSocket connection.
    """
    if isinstance(message, bytes):
        await handle_audio_message(message, stream_id, transcription_client)
    elif isinstance(message, str):
        handle_control_message(message)


async def handle_audio_message(message, stream_id, transcription_client):
    """
    Handle an audio message from the WebSocket connection.
    """
    audio_array = Client.bytes_to_float_array(message)
    audio_buffers[stream_id].write(audio_array.tobytes())
    transcription_client.send_packet_to_server(audio_buffers[stream_id].getvalue())
    logging.debug("Received audio bytes, sending to transcription service.")
    audio_buffers[stream_id] = BytesIO()


def handle_control_message(message):
    """
    Handle a control (text) message from the WebSocket connection.
    """
    logging.info(f"Received message: {message}")


def cleanup_resources(stream_id):
    """
    Clean up resources associated with a given stream_id.
    """
    del audio_buffers[stream_id]
    del transcription_clients_dict[stream_id]
    logging.debug("Cleanup completed for stream %s.", stream_id)


async def main():
    """
    Starts the WebSocket server.
    """
    async with websockets.serve(handle_audio, HOST, PORT):
        await asyncio.Future()  # Run the server until it's manually stopped


if __name__ == "__main__":
    asyncio.run(main())
