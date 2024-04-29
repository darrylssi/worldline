import re
from http.server
import json
import socketserver

class handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
		if re.search('/hello', self.path):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            # Return json, even though it came in as POST URL params
            message = "Hello, World! Here is a GET response"
         	self.wfile.write(bytes(message, "utf8"))

        else:
            self.send_response(403)
        self.end_headers()


	def do_POST(self):
		self._set_headers()
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))

		self.send_response(200)
		self.end_headers()

		data = json.loads(self.data_string)
		insert_to_database(data)
		return

if __name__ == '__main__':
    with socketserver.TCPServer(("", 8000), handler) as httpd:
    print("serving at port", 8000)
    httpd.serve_forever()