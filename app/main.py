import socket
import threading
import os

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

    if not request:
        client_socket.close()
        return

    lines = request.split("\r\n")

    # =========================
    # REQUEST LINE
    # =========================
    request_line = lines[0]
    method, path, version = request_line.split(" ")

    print(f"\n{method} {path}")

    # =========================
    # HEADERS
    # =========================
    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(": ", 1)
        headers[key] = value

    # =========================
    # BODY
    # =========================
    body = ""
    if "" in lines:
        empty_index = lines.index("")
        body = "\r\n".join(lines[empty_index + 1:])

    # =========================
    # HANDLE POST /login
    # =========================
    if method == "POST" and path == "/login":

        data = {}

        if body:
            pairs = body.split("&")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    data[key] = value

        username = data.get("username", "")
        password = data.get("password", "")

        response_body = f"""
        <html>
        <body>
            <h2>Login Result</h2>
            <p>Username: {username}</p>
            <p>Password: {password}</p>
            <a href="/form.html">Go Back</a>
        </body>
        </html>
        """

        content_type = "text/html"

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n"
            f"{response_body}"
        )

        client_socket.send(response.encode())
        client_socket.close()
        return

    # =========================
    # HANDLE GET (FILES)
    # =========================
    if path == "/":
        filepath = "index.html"
    else:
        filepath = path[1:]  # remove leading "/"

    # 🔥 IMPORTANT FIX: Correct file path
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, filepath)

    print("Opening file:", full_path)

    try:
        with open(full_path, "r") as file:
            response_body = file.read()
        status = "200 OK"

    except FileNotFoundError:
        response_body = "<h1>404 Not Found</h1>"
        status = "404 Not Found"

    # =========================
    # CONTENT TYPE
    # =========================
    if filepath.endswith(".html"):
        content_type = "text/html"
    elif filepath.endswith(".css"):
        content_type = "text/css"
    else:
        content_type = "text/plain"

    # =========================
    # RESPONSE
    # =========================
    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
    )

    client_socket.send(response.encode())
    client_socket.close()


# =========================
# START SERVER
# =========================
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
