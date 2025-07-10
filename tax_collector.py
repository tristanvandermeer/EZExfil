# Here goes the backend

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):

    def DoGet(self):
        self.send_Response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "WAR"
        self.wfile.write(bytes(message, "utf8"))

    def doPut(self):
        """Save a file following a HTTP PUT request"""
        filename = os.path.basename(self.path)

        # Don't overwrite files
        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode('utf-8'))
            return

        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), handler)
    print("Starting server at http://localhost:8000")
    server.serve_forever()