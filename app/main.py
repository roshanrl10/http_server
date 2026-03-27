import socket
import threading


def handle_client(client_socket):
    print("new client connected")
    request = client_socket.recv(1024).decode()
    print("request received :")
    print(request)
    # parse request line
    request_line = request.split("\r\n")[0]
    method, path, version = request_line.split(" ")

    # simple routing
    if path == "/":
        with open("index.html", "r") as file:
            body = file.read()

    elif path == "/home":
        body = " welcome to home page"

    elif path == "/about":
        body = "welcome to about page. This is build with your trust"

    else:
        body = "404 not found"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    client_socket.send(response.encode())

    client_socket.close()

    print("Client disconnected\n")

# this creeates a tcp socket

# server_socket = socket.socket(
#     socket.AF_INET, socket.SOCK_STREAM)  # AF_INET=ipv4 address SOCK_STREAM=tcp protocol
# server_socket.bind(("localhost", 8080))  # bind address with 8080 port
# # This turns the socket into a server socket. 5 means the maximum qued connection
# server_socket.listen(5)
# print("Server running on http://localhost:8080")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(5)
print("server running on http://localhost:8080")

while True:
    client_socket, address = server_socket.accept()
    # create a new thread for each client
    thread = threading.Thread(
        target=handle_client,
        args=(client_socket,))
    thread.start()

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
