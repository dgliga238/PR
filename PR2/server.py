from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import psycopg2
import urllib.parse
import cgi

# Database connection
connection = psycopg2.connect(
    database="DanaPR",
    user="postgres",
    password="Dana080603",
    host="localhost",
    port=8888
)
cursor = connection.cursor()


class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/devices"):
            self.get_all_devices()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == "/post_devices":
            self.create_device()
        elif self.path == "/upload_json":
            self.upload_json()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_PUT(self):
        if self.path.startswith("/put_devices/"):
            device_id = self.path.split("/")[-1]
            self.update_device(device_id)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_DELETE(self):
        if self.path.startswith("/delete_devices/"):
            device_id = self.path.split("/")[-1]
            self.delete_device(device_id)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def get_all_devices(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        limit = int(query_params.get("limit", [100])[0])
        offset = int(query_params.get("offset", [0])[0])

        cursor.execute("SELECT * FROM devices LIMIT %s OFFSET %s;", (limit, offset))
        records = cursor.fetchall()

        response = []
        for record in records:
            response.append({
                "device_id": record[0],
                "name_device": record[1],
                "price": record[2]
            })

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def create_device(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        device_data = json.loads(post_data)

        name_device = device_data.get("name_device")
        price = device_data.get("price")

        if name_device and price:
            cursor.execute(
                "INSERT INTO devices (name_device, price) VALUES (%s, %s) RETURNING device_id;",
                (name_device, price)
            )
            connection.commit()
            device_id = cursor.fetchone()[0]

            response = {"device_id": device_id, "name_device": name_device, "price": price}
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request")

    def upload_json(self):
        content_type = self.headers.get("Content-Type")
        if content_type.startswith("multipart/form-data"):
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

            # Retrieve the uploaded file
            file_item = form["file"]

            if file_item.filename:
                file_data = file_item.file.read()
                try:
                    json_data = json.loads(file_data.decode("utf-8"))

                    # Process the JSON data (e.g., save to DB or file)
                    # Here, we just return the JSON back for demonstration
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(json_data).encode("utf-8"))
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Invalid JSON file")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No file uploaded")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Unsupported Content-Type")

    def update_device(self, device_id):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length)
        device_data = json.loads(put_data)

        name_device = device_data.get("name_device")
        price = device_data.get("price")

        cursor.execute(
            "UPDATE devices SET name_device = %s, price = %s WHERE device_id = %s;",
            (name_device, price, device_id)
        )
        connection.commit()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"device_id": device_id, "name_device": name_device, "price": price}
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def delete_device(self, device_id):
        cursor.execute("DELETE FROM devices WHERE device_id = %s;", (device_id,))
        connection.commit()

        self.send_response(204)
        self.end_headers()


# Define server address and port
server_address = ('', 8000)
httpd = HTTPServer(server_address, MyRequestHandler)

print("Starting server on port 8000...")
httpd.serve_forever()

# Close the database connection when the server stops
connection.close()
