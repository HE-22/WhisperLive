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
transcription_clients = {}


async def handle_audio(websocket, path):
    """
    Handles incoming audio stream via WebSocket and sends it for transcription.
    Each WebSocket connection is handled separately based on the path.
    """
    stream_id = path  # Unique identifier for the stream

    # Create a new TranscriptionClient for this stream if it doesn't exist
    if stream_id not in transcription_clients:
        transcription_clients[stream_id] = Client(
            HOST, PORT, is_multilingual=True, lang="en", translate=False
        )

    transcription_client = transcription_clients[stream_id]

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                audio_array = Client.bytes_to_float_array(message)

                # Write to the buffer specific to this stream
                audio_buffers[stream_id].write(audio_array.tobytes())

                # Sending the audio bytes to the transcription service
                transcription_client.send_packet_to_server(
                    audio_buffers[stream_id].getvalue()
                )
                logging.debug("Received audio bytes, sending to transcription service.")

                # Reset buffer after sending
                audio_buffers[stream_id] = BytesIO()
            elif isinstance(message, str):
                # Handle text messages (e.g., control messages) here
                logging.info(f"Received message: {message}")

    except Exception as e:
        logging.error("Error occurred in handle_audio: %s", e, exc_info=True)
    finally:
        # Clean up the buffer for this stream
        del audio_buffers[stream_id]
        del transcription_clients[stream_id]
        logging.debug("handle_audio cleanup completed for stream %s.", stream_id)


async def main():
    """
    Starts the WebSocket server.
    """
    async with websockets.serve(handle_audio, "localhost", 8765):
        await asyncio.Future()  # Run the server until it's manually stopped


if __name__ == "__main__":
    asyncio.run(main())
