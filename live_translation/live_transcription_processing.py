# TODO: 1) Mock translation input
# TODO: 2) convert live incoming translation to segmeetns (or use existing segments)
# TODO: 3) translate each segment asyncronously
# TODO: 4) stitch translated segments together in the right order
# TODO: 5) display live translation


# TODO: check the fastest possible time from speech to live translation


import asyncio
import json
import websockets
import random
import time

# Define a set of mock segment data
mock_segments = [
    {"start": 0, "end": 5, "text": "Hello, this is a test."},
    {"start": 5, "end": 10, "text": "The quick brown fox jumps over the lazy dog."},
    {"start": 10, "end": 15, "text": "Another segment of transcribed text."},
    # Add more mock segments as needed
]


async def send_mock_segments(websocket, path):
    # Send a SERVER_READY message to the client
    await websocket.send(json.dumps({"uid": "mock_uid", "message": "SERVER_READY"}))

    # Start sending mock segment data to the client
    for segment in mock_segments:
        # Simulate a delay between segments
        await asyncio.sleep(random.uniform(0.5, 1.5))

        # Send the segment to the client
        await websocket.send(json.dumps({"uid": "mock_uid", "segments": [segment]}))

        # Simulate the end of the stream
        if segment == mock_segments[-1]:
            await websocket.send(
                json.dumps({"uid": "mock_uid", "message": "DISCONNECT"})
            )
            break


# Start the mock WebSocket server
start_server = websockets.serve(send_mock_segments, "localhost", 8765)

# Run the server until it is manually stopped
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
