import socket
import ssl

def fetch_secure_content():
    host = 'www.google.com'
    port = 443

    # Socket With SSL
    context = ssl.create_default_context()
    connection = socket.create_connection((host, port))
    secure_connection = context.wrap_socket(connection, server_hostname=host)

    # Send an HTTP GET request for the root path
    request = "GET / HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += "Connection: close\r\n\r\n"
    secure_connection.send(request.encode())

    # Receive the HTTP response
    response = b""
    while True:
        data = secure_connection.recv(4096)
        if not data:
            break
        response += data

    # Save the response content to a file
    with open("response.html", "wb") as file:
        file.write(response)

    # Close the connection
    secure_connection.close()

if __name__ == "__main__":
    fetch_secure_content()
