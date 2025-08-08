import socket
import ssl

def fetch_secure_content():
    host = 'www.google.com'
    port = 443

    # Create SSL-wrapped socket
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Send GET request
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )
            ssock.sendall(request.encode())

            # Receive full response
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data

    # Separate headers from body
    header_end = response.find(b"\r\n\r\n")
    if header_end == -1:
        print("Failed to parse HTTP response")
        return

    headers = response[:header_end].decode(errors="replace")
    body = response[header_end + 4:]

    # Handle chunked transfer encoding if needed
    if "Transfer-Encoding: chunked" in headers:
        body = decode_chunked_body(body)

    # Save HTML body to file
    with open("response.html", "wb") as file:
        file.write(body)

def decode_chunked_body(body):
    """Decodes chunked transfer encoding."""
    decoded = b""
    while body:
        # Find the length of the next chunk
        pos = body.find(b"\r\n")
        if pos == -1:
            break
        length_str = body[:pos].decode().strip()
        try:
            length = int(length_str, 16)
        except ValueError:
            break
        if length == 0:
            break
        body = body[pos + 2:]
        decoded += body[:length]
        body = body[length + 2:]  # skip \r\n after chunk
    return decoded

if __name__ == "__main__":
    fetch_secure_content()
