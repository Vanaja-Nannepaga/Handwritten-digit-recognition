import socket
import threading
import time
import os

PEER_ID = 3  # Unique Peer ID for Peer 3
PEERS = [("127.0.0.1", 5001), ("127.0.0.1", 5002)]  # Update the IPs accordingly for each peer
LEADER = None

def request_file():
    # Wait for the leader to be elected, then request the file
    time.sleep(5)
    leader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    leader_socket.connect(("127.0.0.1", 5001))  # Assuming Peer1 is the leader
    print(f"Peer {PEER_ID}: Requesting file 'rollnumber.png' from Leader...")
    leader_socket.send(f"REQUEST:rollnumber.png".encode())
    
    response = leader_socket.recv(1024)
    if response == b"404 Not Found":
        print("Peer {PEER_ID}: File not found on any peer.")
    else:
        # If file is found, save it to disk
        with open('rollnumber.png', 'wb') as f:
            f.write(response)
        print(f"Peer {PEER_ID}: File received successfully.")
    
    leader_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5003))  # Peer 3 listens on port 5003
    server.listen(5)
    print(f"Peer {PEER_ID} server listening on 127.0.0.1:5003")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Peer {PEER_ID}: Connection from {addr}")
        data = client_socket.recv(1024).decode()
        print(f"Peer {PEER_ID}: Received: {data}")
        client_socket.close()

def start_client():
    time.sleep(2)  # Wait for servers to be ready
    for peer in PEERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer[0], peer[1]))
            print(f"Peer {PEER_ID}: Connected to Peer at {peer[0]}:{peer[1]}")
            s.send(f"ID:{PEER_ID}".encode())
            s.close()
        except ConnectionRefusedError as e:
            print(f"Error: Connection to {peer[0]}:{peer[1]} refused. Is the peer server running?")
            print(f"Details: {e}")
        except Exception as e:
            print(f"Error: {e}")

def elect_leader():
    # Logic for leader election (same as in peer1.py)
    pass

def main():
    threading.Thread(target=start_server).start()  # Start the server in a separate thread
    time.sleep(1)  # Ensure the server is ready
    start_client()  # Start client connections to other peers
    elect_leader()  # Elect the leader
    request_file()  # Request file from the leader

if __name__ == "__main__":
    main()

