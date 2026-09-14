from http.server import HTTPServer, BaseHTTPRequestHandler

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # This mimics the exact text GitHub Pages shows for an unclaimed site
        self.wfile.write(b"There isn't a GitHub Pages site here.")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), MockHandler)
    print("Mock vulnerable server running at http://localhost:8000")
    server.serve_forever()