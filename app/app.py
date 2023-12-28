"""Application thatt serves an htttp server with two routes:
- 8080:/
- 8080:/healht
as the first  one returns local time for all the locations in the LOCATION_TIMEZONES (Feel free
to add more locations in this list), and the second one return status code 200 in JSON format.
"""

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


class WiliotHandler(BaseHTTPRequestHandler):
    """Class that serves as the Handler Class for the HTTP Server. You can add more routes
    and behaviors for them updating the do_GET() method with a new path condition."""

    # pylint:disable=invalid-name
    def do_GET(self):
        """Define the server behaviors for specific routes on GET calls"""
        if self.path == "/":
            self.get_local_time()
        elif self.path == "/health":
            self.get_status()

    def get_local_time(self):
        """Get local time for all the Locations defined in the LOCATION_TIMEZONES
        variable and present them as text/HTML as a response."""
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
        """Send status code 200 in JSON format as the server response"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(bytes(json.dumps({"status_code": 200}), "utf-8"))


def run_server(server_class=HTTPServer, handler_class=WiliotHandler):
    """Start and run the HTTP server during the whole app execution.

    Arguments:
        server_class(HTTPServer):
            Class used to create the server.
        handler_class(BaseHTTPRequestHandler):
            Handler that will be used to define the server behaviors.
    """
    server_address = ("", SERVER_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    logging.info("Starting server at port %s", SERVER_PORT)
    run_server()
