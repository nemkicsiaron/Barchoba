import socket
import struct
import select
import random
import sys

num = random.randint(1,100)
packer = struct.Struct('c i')
print("A varázsszám: ", num)
gamegoing = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	server_address = (sys.argv[1], int(sys.argv[2]))
	server.bind(server_address)
	server.listen(1)
	
	sockets = [server]


	while True:
		w,r,e = select.select(sockets,sockets,sockets,1)
		for s in w:
			if s is server:
				client, client_address = server.accept()
				print("Kapcsolodott: ", client_address)
				client.setblocking(1)
				sockets.append(client)
			elif not gamegoing:
				s.sendall(packer.pack(b'V', num))
				sockets.remove(s)
				w.remove(s)
			elif gamegoing:
				data = s.recv(packer.size)
				if not data:
					print("Kliens kilepett")
					sockets.remove(s)
					s.close()
				else:
					unpacked_data = packer.unpack(data)
					print ('Tipp: ', unpacked_data)
					if unpacked_data[0].decode() == '=':
						goodtip = unpacked_data[1] == num
						print(goodtip)
						if goodtip:
							gamegoing = False
							s.sendall(packer.pack(b'Y', unpacked_data[1]))
							w.remove(s)
							sockets.remove(s)
							break
						else:
							s.sendall(packer.pack(b'K', unpacked_data[1]))
					else:
						goodtip = eval(str(num)+str(unpacked_data[0].decode())+str(unpacked_data[1]))
						print(goodtip)
						if goodtip:
							s.sendall(packer.pack(b'I', unpacked_data[1]))
						else:
							s.sendall(packer.pack(b'N', unpacked_data[1]))
