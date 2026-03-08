import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # TODO: Uncomment the code below to pass the first stage

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    sock, adr = server_socket.accept()  # wait for client
    # print(f"Connection from {adr} has been established!")
    sock.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))
    # sock.close()


if __name__ == "__main__":
    main()
