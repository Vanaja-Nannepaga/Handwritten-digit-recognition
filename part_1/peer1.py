import socket
import threading
import random
import time

# Peer info
ID = 1
IP = "127.0.0.1"
PORT = 5001
PEER_LIST = [(2, "127.0.0.1", 5002), (3, "127.0.0.1", 5003)]  # List of other peers

# File log data (for simulation)
FILES = ["file1.txt", "file2.txt", "file3.txt"]

# Elect leader function
def elect_leader():
    # Send ID to all peers and get the smallest ID
    peer_ids = [ID]
    for peer in PEER_LIST:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer[1], peer[2]))
            s.sendall(f"ID:{ID}".encode())
            data = s.recv(1024).decode()
            peer_ids.append(int(data.split(":")[1]))
    
    leader_id = min(peer_ids)
    if leader_id == ID:
        print(f"Node {ID} is the leader.")
        return True  # This node is the leader
    else:
        print(f"Node {ID} is not the leader.")
        return False  # This node is not the leader

# Handle connections as the leader
def handle_leader():
    # Send SEND command to peers
    for peer in PEER_LIST:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer[1], peer[2]))
            s.sendall("SEND".encode())
            data = s.recv(1024).decode()
            with open("peer_files.log", "a") as log:
                log.write(f"From {peer[0]}: {data}\n")
            print(f"Received file log from {peer[0]}: {data}")

# Handle client connections
def handle_client(client_socket, addr):
    data = client_socket.recv(1024).decode()
    if data.startswith("ID:"):
        client_socket.sendall(f"ID:{ID}".encode())  # Respond with own ID
    elif data == "SEND":
        # Send file log to leader
        file_log = "; ".join(FILES)
        client_socket.sendall(file_log.encode())
    client_socket.close()

# Start TCP server
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((IP, PORT))
        server_socket.listen(5)
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# Start client connection to other peers
def start_client():
    for peer in PEER_LIST:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer[1], peer[2]))
            s.sendall(f"ID:{ID}".encode())
            data = s.recv(1024).decode()
            print(f"Received ID from Peer {peer[0]}: {data}")

# Main function
def main():
    print(f"Starting Peer {ID}...")
    threading.Thread(target=start_server).start()
    time.sleep(5)  # Wait 5 seconds to ensure server initialization
    start_client()

    # Elect leader
    if elect_leader():
        handle_leader()


if __name__ == "__main__":
    main()

