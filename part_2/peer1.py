import socket
import threading
import time
import os

PEER_ID = 1
PEERS = [("127.0.0.1", 5002), ("127.0.0.1", 5003)]
LEADER = None
FILES_LOG = "Peer_files.log"

def handle_client_connection(client_socket):
    try:
        data = client_socket.recv(1024).decode()
        print(f"Received request: {data}")
        
        if data.startswith("ID:"):
            peer_id = int(data.split(":")[1])
            print(f"Received ID from Peer {peer_id}")
        
        elif data.startswith("REQUEST:"):
            requested_file = data.split(":")[1]
            print(f"Received request for file: {requested_file}")
            # Check if the leader has the file
            if requested_file == "rollnumber.png" and os.path.exists(requested_file):
                print("Leader has the requested file. Sending file...")
                send_file(client_socket, requested_file)
            else:
                # If the leader doesn't have the file, check the logs
                file_found = check_file_in_log(requested_file)
                if file_found:
                    print(f"File {requested_file} found in log. Sending file...")
                    send_file(client_socket, requested_file)
                else:
                    print(f"File {requested_file} not found. Sending 404 response.")
                    client_socket.send("404 Not Found".encode())
                    
        client_socket.close()
    except Exception as e:
        print(f"Error handling client connection: {e}")

def send_file(client_socket, filename):
    with open(filename, 'rb') as f:
        file_data = f.read()
        client_socket.send(file_data)
        print(f"Sent file {filename} to client.")

def check_file_in_log(filename):
    # Read the peer files log and check if any peer has the file
    if os.path.exists(FILES_LOG):
        with open(FILES_LOG, 'r') as log_file:
            files = log_file.readlines()
            for line in files:
                if filename in line:
                    return True
    return False

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5001))
    server.listen(5)
    print(f"Peer {PEER_ID} server listening on 127.0.0.1:5001")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client_connection, args=(client_socket,)).start()

def start_client():
    time.sleep(2)  # Wait for the servers to be ready
    for peer in PEERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer[0], peer[1]))
            print(f"Connected to Peer at {peer[0]}:{peer[1]}")
            s.send(f"ID:{PEER_ID}".encode())
            s.close()
        except ConnectionRefusedError as e:
            print(f"Error: Connection to {peer[0]}:{peer[1]} refused. Is the peer server running?")
            print(f"Details: {e}")
        except Exception as e:
            print(f"Error: {e}")

def elect_leader():
    peer_ids = [PEER_ID]
    for peer in PEERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer[0], peer[1]))
            s.send(f"ID:{PEER_ID}".encode())
            data = s.recv(1024).decode()
            if data:
                print(f"Received ID from Peer: {data}")
                peer_ids.append(int(data.split(":")[1]))  # Split and extract ID
            s.close()
        except Exception as e:
            print(f"Error during leader election: {e}")

    global LEADER
    LEADER = min(peer_ids)
    print(f"Leader elected: Peer {LEADER}")

    # After election, listen for file requests
    if PEER_ID == LEADER:
        print("Leader is ready to handle file requests.")
    else:
        print("Not the leader. Waiting for file request.")

def main():
    threading.Thread(target=start_server).start()
    time.sleep(1)
    start_client()
    elect_leader()

if __name__ == "__main__":
    main()

