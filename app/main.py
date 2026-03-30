import socket
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# this creeates a tcp socket

# server_socket = socket.socket(
#     socket.AF_INET, socket.SOCK_STREAM)  # AF_INET=ipv4 address SOCK_STREAM=tcp protocol
# server_socket.bind(("localhost", 8080))  # bind address with 8080 port
# # This turns the socket into a server socket. 5 means the maximum qued connection
# server_socket.listen(5)
# print("Server running on http://localhost:8080")


# while True:

#     client_socket, address = server_socket.accept()

#     request = client_socket.recv(1024).decode()

#     lines = request.split("\r\n")

#     request_line = lines[0]

#     method, path, version = request_line.split(" ")

#     headers = {}

#     for line in lines[1:]:
#         if line == "":
#             break

#         key, value = line.split(": ", 1)
#         headers[key] = value

#     print("Method:", method)
#     print("Path:", path)

#     print("\nHeaders:")
#     for k, v in headers.items():
#         print(k, ":", v)

# if path == "/":
#     with open("index.html", "r") as file:
#         body = file.read()

#     response = (
#         "HTTP/1.1 200 OK\r\n"
#         "Content-Type: text/html\r\n"
#         f"Content-Length: {len(body)}\r\n"
#         "\r\n"
#         f"{body}"
#     )

#     client_socket.send(response.encode())

#     client_socket.close()

def handle_client(client_socket):

    request = client_socket.recv(1024).decode()

    lines = request.split("\r\n")

    request_line = lines[0]
    method, path, version = request_line.split(" ")

    # Extract headers
    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(": ", 1)
        headers[key] = value

    # Extract body
    body = ""
    if "" in lines:
        empty_index = lines.index("")
        body = "\r\n".join(lines[empty_index + 1:])

    print("Method:", method)
    print("Path:", path)
    print("Body:", body)

    # Handle POST /login
    if method == "POST" and path == "/login":

        data = {}
        if body:
            pairs = body.split("&")
            for pair in pairs:
                key, value = pair.split("=")
                data[key] = value

        username = data.get("username", "")
        password = data.get("password", "")

        response_body = f"Received username={username}, password={password}"

    else:
        response_body = "Hello from server"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
    )

    client_socket.send(response.encode())
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(5)

print("Server running at http://localhost:8080")

while True:
    client_socket, address = server_socket.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,)
    )
    thread.start()
