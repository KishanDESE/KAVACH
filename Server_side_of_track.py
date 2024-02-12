import socket
from threading import Thread
import hashlib

# Global variable
connected = True		
FORMAT = 'utf-8'
dir1 = 0
dir2 = 0
First = 6
Second = 6
train1loc = 0
train2loc = 6
velocity1 = 0
velocity2 = 0
train1len = 0
train2len = 0

# two train connection

def same_direction_emergency():
	if ((First == 1 and abs(train1loc + train1len - train2loc) < 6) or (First == 2 and abs(train1loc - train2loc - train2len) < 6)):
		return 1
	else:
		return 0

def same_direction_warning():
	if(velocity1 > velocity2 and First == 1 and velocity1 * velocity2 > 0):
		return 0
	elif (velocity1 > velocity2 and First == 2 and velocity1 * velocity2 > 0):
		return 1
	elif(velocity2 > velocity1 and First == 2 and velocity1 * velocity2 > 0):
		return 0
	elif (velocity2 > velocity1 and First == 1 and velocity1 * velocity2 > 0):
		return 1
	elif (velocity1 == velocity2 and (First == 1 or First == 2) and velocity1 * velocity2 > 0):
		return 1
	else:
		return 0

def receive_password(client_socket):
	password = client_socket.recv(1024).decode(FORMAT)
	return password

def send_password(client_socket, password):
	client_socket.send(password.encode(FORMAT))

def server1():

	emergency1 = 0
	emergency2 = 0
	global First
	global Second
	global velocity1
	global velocity2
	global train1loc
	global train1len
	opposite = 0
	SERVER_IP = "10.114.241.36"
	Train2_PORT = 5050

	# Create a TCP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the server IP and port
	server_socket.bind((SERVER_IP, Train2_PORT))

	# Listen for incoming connections
	server_socket.listen(1)

	print("Station server is listening to train1 ...")

	while True:
		# Accept a client connection
		client_socket, client_address = server_socket.accept()
		print(f"Accepted connection from Train1")

		# Exchange passwords
		server_password = "server_password"
		send_password(client_socket, server_password)
		client_password = receive_password(client_socket)

		# Hash passwords for secure comparison
		hashed_server_password = hashlib.sha256(server_password.encode()).hexdigest()
		hashed_client_password = hashlib.sha256(client_password.encode()).hexdigest()

		if hashed_server_password == hashed_client_password:
			print("Password exchange successful. Connection secured.")
		else:
			print("Password exchange failed. Closing connection.")
			client_socket.close()
			continue

		while True:
			message = client_socket.recv(1024)
			msg = message.decode(FORMAT)
			values = msg.split()
			global dir1
			global dir2
			
			# Extract train_number from values
			train1 = int(values[0])
			track = int(values[1])
			loc1 = int(values[2])
			loc2 = int(values[3])
			speed1 = int(values[4])
			train1len = int(values[5])
			train1loc = loc1
			dir1 = loc2 - loc1
			velocity1 = (loc2 - loc1) * speed1
			if (track == 78):
				if (loc1 == 31 or loc1 == 49):
					
					
					if (First == 6):
						First = 1
						print(f"Train {train1} is first")
						message = "Go"
						client_socket.send(message.encode(FORMAT))
					elif (First == 1):
						Second = 1
						
					else :
						pass
				else :
					pass
				
				if(dir1 * dir2 < 0 and opposite == 1 and speed1 > 5) :
					message = "EMERGENCY STOP exceeded speed 5km/hr in opposite direction"
					client_socket.send(message.encode(FORMAT))
					emergency2 = 1
				else :
					pass
				if(dir1 * dir2 < 0 and opposite == 1 and speed1 > 2 and emergency2 == 0) :
					message = "WARNING exceeded speed 2 km/hr in opposite direction"
					client_socket.send(message.encode(FORMAT))
				else :
					pass
				if(First == 1 and dir1 * dir2 < 0 and opposite == 0) : #Lot of work left
					message = "STOP other train in opposite direction"
					client_socket.send(message.encode(FORMAT))
					opposite = 1
				else :
					pass
				if(First == 2 and dir1 * dir2 < 0 and opposite == 0) : #Lot of work left
					message = "STOP other train in opposite direction"
					client_socket.send(message.encode(FORMAT))
					opposite = 1
				else :
					pass

				if(Second == 1 and same_direction_emergency() == 1 and dir1 * dir2 > 0) :
					print(f"Train1 and Train2 came closer than required")
					emergency1 = 1
					message = "EMERGENCY STOP you are closer to next train"
					client_socket.send(message.encode(FORMAT))
				if(same_direction_emergency() == 1 and dir1 * dir2 < 0 ) :
					emergency1 = 1
					print(f"Train1 and Train2 came closer than required")
					message = "EMERGENCY STOP you are closer to next train"
					client_socket.send(message.encode(FORMAT))
				else :
					pass
				if(same_direction_warning()==1 and Second ==1 and dir1 * dir2 > 0 and emergency1 == 0) :
					print(f"Warning alert Train1 is at back")
					message = "Warning Alert slow down other Train is in front slower than you"
					client_socket.send(message.encode(FORMAT))

				else :
					message = "|"
					client_socket.send(message.encode(FORMAT))

def server2():

	emergency1 = 0
	emergency2 = 0
	global First
	global Second
	global velocity1
	global velocity2
	global train2loc
	global train2len
	opposite = 0
	SERVER_IP = "10.114.241.36"
	Train1_PORT = 5060

	# Create a TCP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the server IP and port
	server_socket.bind((SERVER_IP, Train1_PORT))

	# Listen for incoming connections
	server_socket.listen(1)

	print("Station server is listening to train2 ...")

	while True:
		# Accept a client connection
		client_socket, client_address = server_socket.accept()
		print(f"Accepted connection from Train2")

		# Exchange passwords
		server_password = "server_password"
		send_password(client_socket, server_password)
		client_password = receive_password(client_socket)

		# Hash passwords for secure comparison
		hashed_server_password = hashlib.sha256(server_password.encode()).hexdigest()
		hashed_client_password = hashlib.sha256(client_password.encode()).hexdigest()

		if hashed_server_password == hashed_client_password:
			print("Password exchange successful. Connection secured.")
		else:
			print("Password exchange failed. Closing connection.")
			client_socket.close()
			continue

		while True:
			message = client_socket.recv(1024)
			msg = message.decode(FORMAT)
			values = msg.split()
			global dir1
			global dir2

			# Extract train_number from values
			train2 = int(values[0])
			track = int(values[1])
			loc1 = int(values[2])
			loc2 = int(values[3])
			speed2 = int(values[4])
			train2len = int(values[5])
			train2loc = loc1
			dir2 = (loc2 - loc1)
			velocity2 = (loc2 - loc1) * speed2
			if (track == 78):
				if (loc1 == 31 or loc1 == 49):
					
					
					if (First == 6):
						First = 2
						print(f"Train {train2} is first")
						message = "Go"
						client_socket.send(message.encode(FORMAT))
					elif (First == 1):
						Second = 2
					else :
						pass
				else :
					pass
				if(dir1 * dir2 < 0 and opposite == 1 and speed2 > 5) :
					message = "EMERGENCY STOP exceeded speed 5km/hr in opposite direction"
					client_socket.send(message.encode(FORMAT))
					emergency2 = 1
				else :
					pass
				if(dir1 * dir2 < 0 and opposite == 1 and speed2 > 2 and emergency2 == 0) :
					message = "WARNING exceeded speed 2 km/hr in opposite direction"
					client_socket.send(message.encode(FORMAT))
				else :
					pass
				if(First == 2 and dir1 * dir2 < 0 and opposite == 0) :
					message = "STOP other train in opposite direction"
					client_socket.send(message.encode(FORMAT))
					opposite = 1
				else :
					pass
				if(First == 1 and dir1 * dir2 < 0 and opposite == 0) : #Lot of work left
					message = "STOP other train in opposite direction"
					client_socket.send(message.encode(FORMAT))
					opposite = 1
					
				else :
					pass
				
				if(Second == 2 and same_direction_emergency() == 1 and  dir1 * dir2 > 0 ) :
					emergency1 = 1
					print(f"Train1 and Train2 came closer than required")
					message = "EMERGENCY STOP you are closer to next train"
					client_socket.send(message.encode(FORMAT))
				else :
					pass
				if(same_direction_emergency() == 1 and dir1 * dir2 < 0 ) :
					emergency1 = 1
					print(f"Train1 and Train2 came closer than required")
					message = "EMERGENCY STOP you are closer to next train"
					client_socket.send(message.encode(FORMAT))
				else :
					pass	
				if(same_direction_warning()==1 and Second ==2 and dir1 * dir2 > 0 and (emergency1 == 0)) :
					print(f"Warning alert Train2 is at back")
					message = "Warning Alert slow down other Train is in front slower than you"
					client_socket.send(message.encode(FORMAT))

				else :
					message = "|"
					client_socket.send(message.encode(FORMAT))

Thread(target=server2).start()
Thread(target=server1).start()

