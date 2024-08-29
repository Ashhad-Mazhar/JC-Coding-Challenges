import sys
from urllib.parse import urlparse

def main():
    url = sys.argv[1]
    parsed_url = parse_url(url)
    request = create_get_request(parsed_url)
    print_message(parsed_url, request)

def parse_url(url: str) -> dict:
    parsed_url = urlparse(url)

    protocol = parsed_url.scheme or 'http'
    host = parsed_url.hostname
    port = parsed_url.port or (80 if protocol == 'http' else None)
    path = parsed_url.path or '/'

    return {
        'protocol': protocol,
        'host': host,
        'port': port,
        'path': path,
    }

def create_get_request(parsed_url: dict) -> str:
    request = (
        f'GET {parsed_url['path']} '
        f'HTTP/1.1\n'
        f'Host: {parsed_url['host']}\n'
        'Accept: */*'
    )
    return request

def print_message(parsed_url: dict, request: str) -> None:
    print(f'connecting to {parsed_url['host']}')
    print(f'Sending request {request}')


if __name__ == '__main__':
    main()