import http.server
import socketserver
import os

# Port number for the HTTP server
PORT = 8000

# Directory containing the HLS stream files
DIRECTORY = "/Users/hassen/Dev/Jeenie/whisper-live-fork/WhisperLive/my_code/assets/hls"


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


# Create an HTTP server and socket server, using the custom handler
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print(f"Serving directory '{DIRECTORY}' at http://localhost:{PORT}")
    httpd.serve_forever()
