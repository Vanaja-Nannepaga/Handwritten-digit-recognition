import socket

def echo_server(port):
    # Create a socket for IPv4 and IPv6 using AF_INET6
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to the given port, allowing IPv4/IPv6 compatibility
    server_socket.bind(("::", port))  # "::" listens on both IPv4/IPv6
    server_socket.listen(5)
    print(f"Server listening on port {port} (IPv4/IPv6)...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        # Echo received data back to client
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            conn.sendall(data)  # Echo the data back

        conn.close()
        print(f"Connection closed with {addr}")

if __name__ == "__main__":
    port = 12345
    echo_server(port)

