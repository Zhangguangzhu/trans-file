# -*- coding: utf-8 -*-

from socket import *
import os, struct, threading


class Server(object):
	def __init__(self):
		Host = '127.0.0.1'
		Port = 8000
		self.SerSock = socket(AF_INET, SOCK_STREAM)
		self.SerSock.bind((Host, Port))
		self.SerSock.listen(2)

	def upload(self, CliSock):
		fheadsize = struct.calcsize('128sl')
		fheadinfo = CliSock.recv(fheadsize)
		if fheadinfo:
			filename, filesize = struct.unpack('128sl', fheadinfo)
			recv_size = 0
			with open(filename.strip('\00'), 'wb') as f:
				while not recv_size == filesize:
					if filesize - recv_size > 1024:
						data = CliSock.recv(1024)
						if not data:
							break
					else:
						data = CliSock.recv(filesize - recv_size)
						if not data:
							break
					recv_size += len(data)
					f.write(data)
			print 'recived file:%s' % filename.strip('\00')

	def download(self, CliSock):
		fliststr = ''
		for i in os.listdir('.'):
			if os.path.isfile(i):
				fliststr += i + '\n'
		fliststr = fliststr + '\00' * (1024 - len(fliststr))
		CliSock.sendall(fliststr)
		print str(len(fliststr)), fliststr
		fname = CliSock.recv(struct.calcsize('128s')).strip('\00')
		fheadinfo = struct.pack('128sl', fname, os.path.getsize(fname))
		CliSock.send(fheadinfo)
		with open(fname, 'rb') as f:
			while True:
				data = f.read(1024)
				if not data:
					break
				CliSock.send(data)
		print 'send file :%s succeed' % fname

	def conn_thread(self, CliSock):
		while True:
			# print '1'
			data = CliSock.recv(1)
			# print '1end'
			if data:
				if data == '1':
					self.upload(CliSock)
				elif data == '2':
					self.download(CliSock)
				elif data == 'exit':
					break
				else:
					continue
			else:
				break
		CliSock.close()

	def main(self):
		threads = []
		try:
			while True:
				print 'waiting for connection.................'
				CliSock, CliAddr = self.SerSock.accept()
				print 'connection from %s %s' % (CliAddr[0], CliAddr[1])
				t = threading.Thread(target=self.conn_thread, args=(CliSock,))
				threads.append(t)
				threads.pop(0).start()
		except KeyboardInterrupt:
			self.SerSock.close()


server = Server()
server.main()
