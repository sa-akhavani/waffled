import socket
import ssl
import sys
import os
import argparse

# from hostnames import target_urls

_BUFFER_SIZE = 4096  # 4 KB
_TIMEOUT = 20  # 20 seconds (Change if you receive empty response)


class Relay:
    def __init__(self, host, port, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl

    def forward_request(self, raw_request) -> bytes:
        """
        Forward the raw request to the target server and return the response
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.settimeout(_TIMEOUT)

                if self.use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    with context.wrap_socket(
                        client_socket, server_hostname=self.host
                    ) as ssl_socket:
                        ssl_socket.sendall(raw_request)
                        response = self._receive_response(ssl_socket)
                else:
                    client_socket.sendall(raw_request)
                    response = self._receive_response(client_socket)

                return response

        except Exception as e:
            print(f"Error: {e}")
            return None

    def _receive_response(self, client_socket) -> bytes:
        """
        Receive the response from the target server and return it
        """
        response = b""
        while True:
            try:
                data = client_socket.recv(_BUFFER_SIZE)
                if not data:
                    break
                response += data
            except socket.timeout:
                break
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break

        return response


def read_requests_from_file(filename) -> list[bytes]:
    """
    Read raw HTTP requests from a file where each line is a Python byte object.
    Requests in the file have to be in Byte-Object format. b'''<request>'''
    """
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' does not exist.")
        return []

    with open(filename, "r") as file:
        requests = file.readlines()

    # Parse each line into a Python bytes object
    return [eval(req.strip()) for req in requests if req.strip()]


def parse_arguments() -> tuple[str, int, str, bool]:
    """
    Parses command-line arguments, supporting both positional and optional formats.
    Returns the parsed host, port, request file, and SSL flag for HTTPS connections.
    """
    parser = argparse.ArgumentParser(
        # description="Send HTTP requests from a file through a relay using sockets.",
        usage="\npython http_relay.py [host] [port] [requests_filename] [-s (for ssl)]\n"
        "or\n"
        "python http_relay.py -H <host> -p <port> -r <requests_filename> [-s (for ssl)]"
    )

    # Optional arguments (with --flags)
    parser.add_argument("-H", "--host", help="Target host (e.g., example.com)")
    parser.add_argument("-p", "--port", type=int, help="Target port (e.g., 80 or 443)")
    parser.add_argument(
        "-r",
        "--request",
        help="File containing HTTP requests in byte object format (b'''...''')",
    )
    parser.add_argument(
        "-s", "--ssl", action="store_true", help="Use SSL for connections (optional)"
    )

    # Positional arguments (without --flags)
    parser.add_argument("host_positional", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument("port_positional", nargs="?", type=int, help=argparse.SUPPRESS)
    parser.add_argument("request_positional", nargs="?", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Resolve conflicts between positional and optional arguments
    host = args.host or args.host_positional
    port = args.port or args.port_positional
    request_file = args.request or args.request_positional

    # Validate required fields
    if not host or not port or not request_file:
        parser.print_help()
        sys.exit(0)

    return host, port, request_file, args.ssl


if __name__ == "__main__":
    host, port, request_file, use_ssl = parse_arguments()
    relay = Relay(host=host, port=port, use_ssl=use_ssl)
    requests = read_requests_from_file(request_file)

    if not requests:
        print("No requests to send. Exiting.")
        sys.exit(0)

    # Send each request sequentially
    for i, request in enumerate(requests, 1):
        print(f"Sending request {i}:")
        print(request)

        response = relay.forward_request(request)

        if response:
            print("Response:")
            print(response.decode())
        else:
            print("No response received.")
        print("##########################")
