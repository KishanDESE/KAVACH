import socket
import hashlib
import time
Mytrain_number = "1534"
# message = "Train no" + RFID Tag{"Track no" + "loc1"} + "loc2" + "Speed"
#RFID = 0100111000011111 = 78 31 
#opposite
messages = ["1534 78 31 32 100 1", "1534 78 33 34 3 1", "1534 78 35 36 6 1", "1534 78 37 38 0 1"]
#same direction	      do after 4 couple of tags train1 completed								skipping to next tags
#messages = ["1534 78 31 32 100 1", "1534 78 33 34 98 1", "1534 78 35 36 94 1", "1534 78 37 38 70 1", "1534 78 39 40 50 1", "1534 78 44 45 100 1", "1534 78 46 47 100 1", "1534 78 48 49 100 1"]
connected = True		
FORMAT = 'utf-8'
SERVER_TCP_IP = "10.114.241.36"
TCP_PORT = 5060
FORMAT = 'utf-8'

def receive_password(client_socket):
    password = client_socket.recv(1024).decode(FORMAT)
    return password

def send_password(client_socket, password):
    client_socket.send(password.encode(FORMAT))

def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((SERVER_TCP_IP, TCP_PORT))
    except socket.error as e:
        print("EMERGENCY STOP THERE IS A TECHNICAL ISSUE IN CONNECTION TO SERVER")
        return

    # Exchange passwords
    client_password = "server_password"
    send_password(client_socket, client_password)

    server_password = receive_password(client_socket)

    # Hash passwords for secure comparison
    hashed_client_password = hashlib.sha256(client_password.encode()).hexdigest()
    hashed_server_password = hashlib.sha256(server_password.encode()).hexdigest()

    if hashed_client_password == hashed_server_password:
        print("Password exchange successful. Connection secured.")
    else:
        print("Password exchange failed. Closing connection.")
        client_socket.close()
        return

    # Send and receive messages

    for m in messages:
        start_time = time.time()
        client_socket.send(m.encode(FORMAT))
        print(f"Sent: {m}")

        client_socket.settimeout(2)  # 2 seconds timeout for receiving response
        try:
            mesg = client_socket.recv(1024)
        except socket.timeout:
            print("EMERGENCY STOP SERVER ERROR")

        msg = mesg.decode(FORMAT)

        if msg != "":
            print(f"Received: {msg}")

        end_time = time.time()
        time_delay = end_time - start_time
        print("Time delay:", time_delay, "seconds")

        time.sleep(3)

    client_socket.close()

if __name__ == "__main__":
    main()

