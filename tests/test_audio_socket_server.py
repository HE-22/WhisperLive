# test_audio_socket_server.py

import pytest
import asyncio
from unittest.mock import Mock, patch
from websockets.exceptions import ConnectionClosedError
from audio_socket_server import (
    handle_audio,
    get_or_create_transcription_client,
    process_message,
    handle_audio_message,
    cleanup_resources,
)


@pytest.fixture
def websocket():
    # Mock a websocket connection
    ws = Mock()
    ws.recv = Mock(
        side_effect=[
            b"audio_data_1",  # Mock binary data for audio
            b"audio_data_2",
            "control_message",  # Mock control message (string)
            ConnectionClosedError,  # Simulate a closed connection
        ]
    )
    ws.send = Mock()
    ws.close = Mock()
    return ws


@pytest.fixture
def path():
    # Mock the path to represent the stream ID
    return "/test_stream"


@pytest.mark.asyncio
async def test_handle_audio(websocket, path):
    with patch(
        "audio_socket_server.get_or_create_transcription_client"
    ) as mock_get_client:
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        with patch("audio_socket_server.cleanup_resources") as mock_cleanup:
            await handle_audio(websocket, path)

            # Check if the client was created
            mock_get_client.assert_called_with(path)

            # Check if the cleanup function was called after the connection was closed
            mock_cleanup.assert_called_with(path)


@pytest.mark.asyncio
async def test_process_message(websocket, path):
    mock_client = Mock()
    transcription_client = get_or_create_transcription_client(path)

    # Mock the handle_audio_message function to test process_message separately
    with patch("audio_socket_server.handle_audio_message") as mock_handle_audio:
        await process_message(b"audio_data", path, transcription_client)
        mock_handle_audio.assert_called_with(b"audio_data", path, transcription_client)

    # Mock the handle_control_message function to test process_message separately
    with patch("audio_socket_server.handle_control_message") as mock_handle_control:
        await process_message("control_message", path, transcription_client)
        mock_handle_control.assert_called_with("control_message")


@pytest.mark.asyncio
async def test_handle_audio_message(websocket, path):
    mock_client = Mock()
    transcription_client = get_or_create_transcription_client(path)

    # Mock the send_packet_to_server method of the Client
    with patch.object(
        transcription_client, "send_packet_to_server"
    ) as mock_send_packet:
        await handle_audio_message(b"audio_data", path, transcription_client)

        # Check if the send_packet_to_server method was called with the correct data
        mock_send_packet.assert_called()


# Add more tests for edge cases, such as empty audio data, very large audio data, etc.

# Run the tests
if __name__ == "__main__":
    pytest.main()
