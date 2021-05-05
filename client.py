import socket
import struct
import random
import time
import sys

sock = socket.socket()

server_address = (sys.argv[1],  int(sys.argv[2]))
sock.connect(server_address)

packer = struct.Struct('c i')
gamegoing = True
upper = 100
lower = 1
op = b'<'
data = 0

while lower <= upper:
	try:
		if data:
			answer = packer.unpack(data)
			print("A tipp:", answer)

			if answer[0] == b'Y' or answer[0] == b'V' or answer[0] == b'K':
				gamegoing = False
				sock.close()
				break
			elif op == b'<':
				if answer[0] == b'I':
					upper = guess - 1
				elif answer[0] == b'N':
					lower = guess
				op = b'>'
			elif op == b'>':
				if answer[0] == b'I':
					lower = guess + 1
				elif answer[0] == b'N':
					upper = guess
				op = b'<'
		if upper - lower < 1:
			op = b'='
		guess = (int) ((upper + lower) / 2)
		packed_guess = packer.pack(op, guess)
		waittime = random.randint(1,5)
		time.sleep(waittime)
		sock.sendall(packed_guess)
		data = sock.recv(packer.size)
	finally:
		print(lower, upper)

if lower > upper:
	print("Hiba!")