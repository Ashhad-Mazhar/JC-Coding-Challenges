import sys
import socket
from urllib.parse import urlparse

def main():
    url = sys.argv[1]
    parsed_url = parse_url(url)
    headers = [
        f'Host: {parsed_url['host']}',
        'Accept: */*',
        'Connection: close'
    ]
    request = create_get_request(parsed_url, headers)
    print(f'connecting to {parsed_url['host']}')
    print(f'Sending request {request}')
    response = send_request(request, parsed_url['host'], parsed_url['port'])
    print(response)

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

def create_get_request(parsed_url: dict, headers: list[str]) -> str:
    '''
    Returns a GET request in string form for the given URL
    '''
    http_version = 'HTTP/1.1'
    start_line = f'GET {parsed_url['path']} {http_version}'
    request = f'{start_line}\r\n' + '\r\n'.join(headers) + '\r\n\r\n'
    return request

def send_request(request: str, host: str, port: int) -> str:
    '''
    Opens a TCP socket connection to the server and sends
    the given request
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode('utf-8'))
        data = s.recv(1024)
    return data.decode('utf-8')
        

if __name__ == '__main__':
    main()