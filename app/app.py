# webapp.py

from datetime import datetime
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from location import Location
import pytz


LOCATION_TIMEZONES = [
    Location("New York", "America/New_York"),
    Location("Berlin", "Europe/Berlin"),
    Location("Tokyo", "Asia/Tokyo"),
]
SERVER_PORT = 8080

# TODO: Set logging level at .env file
logging.basicConfig(level=logging.INFO)


class wiliotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.get_local_time()
        elif self.path == "/health":
            self.get_status()

    def get_local_time(self):
        local_time = {}
        presentation = "<b> Welcome to wiliot code challenge!</b><br><br>This app returns local time for different cities.<br><br>"
        try:
            for location in LOCATION_TIMEZONES:
                time_zone = pytz.timezone(location.timezone)
                local_time = datetime.now(time_zone).time()
                presentation += (
                    f"{location.city}: {local_time.hour}:{local_time.minute}<br>"
                )
        except Exception as e:
            logging.error(
                "Failed to get local time for location %s. Cause: %s.", location, e
            )
            self.send_response(500)
            raise e

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(presentation, "utf-8"))

    def get_status(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes(json.dumps({"status_code": 200}), "utf-8"))


def run_server(server_class=HTTPServer, handler_class=wiliotHandler):
    server_address = ("", SERVER_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    logging.info("Starting server at port %s", SERVER_PORT)
    run_server()
