# import asyncio
# import json
# from collections import defaultdict
# import websockets
# from io import BytesIO
# import logging

# from whisper_live.client import Client

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )

# HOST = "localhost"
# PORT = 8765

# # Dictionary to store buffers for each stream
# audio_buffers = defaultdict(BytesIO)

# # Dictionary to store TranscriptionClients for each stream
# transcription_clients_dict = {}


# async def handle_audio(websocket, path):
#     """
#     Handles incoming audio stream via WebSocket and sends it for transcription.
#     Each WebSocket connection is handled separately based on the path.
#     """
#     stream_id = path  # ex. /socket/b025774a-8e18-4475-be97-9e0465ed784d
#     logging.info(f"Connected to audio channel: {stream_id}")

#     # Ensure there is a buffer for the current stream
#     # if stream_id not in audio_buffers:
#     #     audio_buffers[stream_id] = BytesIO()
#     #     logging.info(f"Created a new audio buffer for stream: {stream_id}")

#     # Ensure there is a TranscriptionClient for the current stream
#     # if stream_id not in transcription_clients_dict:
#     #     transcription_clients_dict[stream_id] = Client(stream_id)
#     #     logging.info(f"Created a new TranscriptionClient for stream: {stream_id}")

#     try:
#         async for message in websocket:
#             logging.debug(f"Received message from stream: {stream_id}")
#             logging.debug(f"Message from {stream_id}: ({type(message)}) {message} ")
#             # audio_buffers[stream_id].write(message)
#             # await process_message(message, stream_id, transcription_clients_dict[stream_id])
#     except Exception as e:
#         logging.error(f"Error occurred in handle_audio: {e}", exc_info=True)


# async def main():
#     """
#     Starts the WebSocket server and logs server information.
#     """
#     server = await websockets.serve(handle_audio, HOST, PORT)
#     logging.info(f"WebSocket server started on {HOST}:{PORT}")
#     await asyncio.Future()  # Run the server until it's manually stopped


# if __name__ == "__main__":
#     asyncio.run(main())
