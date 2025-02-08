import socket

def echo_client(hostname, port):
    # Resolve address using getaddrinfo
    addr_info = socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM)

    # Select the first suitable address
    for res in addr_info:
        family, socktype, proto, canonname, sockaddr = res
        try:
            client_socket = socket.socket(family, socktype, proto)
            client_socket.connect(sockaddr)
            print(f"Connected to server: {sockaddr}")
            break
        except socket.error as e:
            print(f"Failed to connect using {sockaddr}: {e}")
            continue
    else:
        print("Failed to connect to server.")
        return

    # Send and receive data
    try:
        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == "exit":
                break
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(f"Echoed from server: {data.decode()}")
    finally:
        client_socket.close()
        print("Disconnected from server.")

if __name__ == "__main__":
    # Change to "ip6-localhost" for IPv6, "localhost" for IPv4
    hostname = "localhost"
    port = 12345
    echo_client(hostname, port)

