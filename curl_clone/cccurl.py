import socket
import argparse
from urllib.parse import urlparse


def main():
    parser = create_args_parser()
    args = parser.parse_args()
    if not args.request_method:
        args.request_method = "GET"
    parsed_url = parse_url(args.url)
    headers = [
        f"Host: {parsed_url['host']}",
        "Accept: */*",
        "Connection: close",
    ]
    if args.request_header:
        headers.append(args.request_header)
    request = create_request(
        parsed_url, args.request_method, headers, args.request_payload
    )
    response = send_request(request, parsed_url["host"], parsed_url["port"])

    split_response = response.split("\r\n\r\n")
    response_body = (
        split_response[1] if args.request_method.upper() == "HEAD" else ""
    )
    verbose_response_headers = get_verbose_response_headers(split_response[0])

    # Print the request and response in verbose mode if flag is true
    if args.verbose:
        verbose_request = get_verbose_request(request)
        print(verbose_request)
        print(verbose_response_headers)

    print(response_body)


def create_args_parser() -> argparse.ArgumentParser:
    """
    Returns a parser for handling CLI arguments and flags
    """
    parser = argparse.ArgumentParser(description="CLI utility to send requests")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-X", dest="request_method", type=str, help="Request method to use"
    )
    parser.add_argument("url", type=str, help="The URL to send request to")
    parser.add_argument(
        "-d",
        dest="request_payload",
        type=str,
        help="Payload to be sent with the request",
    )
    parser.add_argument(
        "-H",
        dest="request_header",
        type=str,
        help="Header to be sent with the request",
    )
    return parser


def parse_url(url: str) -> dict:
    """
    Wrote this function instead of just using the urlparse()
    method because some default values needed to be included
    """
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme or "http"
    host = parsed_url.hostname
    port = parsed_url.port or (80 if protocol == "http" else None)
    path = parsed_url.path or "/"

    return {
        "protocol": protocol,
        "host": host,
        "port": port,
        "path": path,
    }


def create_request(
    parsed_url: dict,
    request_method: str,
    headers: list[str],
    request_payload: str,
) -> str:
    """
    Returns an HTTP request in string form for the given URL
    """
    http_version = "HTTP/1.1"
    start_line = f"{request_method.upper()} {parsed_url['path']} {http_version}"
    if request_payload:
        headers.append(f"Content-Length: {len(request_payload)}")
    request = f"{start_line}\r\n" + "\r\n".join(headers) + "\r\n\r\n"
    if request_payload:
        request += request_payload
    return request


def send_request(request: str, host: str, port: int) -> str:
    """
    Opens a TCP socket connection to the server and sends
    the given request
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode("utf-8"))
        data = s.recv(1024)
    return data.decode("utf-8")


def get_verbose_response_headers(response_headers: str) -> str:
    """
    Appends a < symbol before each header for verbose mode
    """
    response_headers_lines = response_headers.splitlines()
    response_headers_lines = [f"< {line}" for line in response_headers_lines]
    verbose_response_headers = "\r\n".join(response_headers_lines) + f"\r\n<"
    return verbose_response_headers


def get_verbose_request(request: str) -> str:
    """
    Appends a > symbol before each header for verbose mode
    """
    request_lines = request.splitlines()
    request_lines = [f"> {line}" for line in request_lines]
    verbose_request = "\r\n".join(request_lines)
    return verbose_request


if __name__ == "__main__":
    main()
