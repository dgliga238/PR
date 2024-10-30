

# Import the HTTP server classes
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define the server address (host, port)
host = "localhost"
port = 8000

# Create the HTTP server and define a handler
server = HTTPServer((host, port), SimpleHTTPRequestHandler)

print(f"Serving HTTP on {host} port {port} (http://{host}:{port}/)")

# Start the server
server.serve_forever()
