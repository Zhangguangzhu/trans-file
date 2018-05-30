# -*- coding: utf-8

from socket import *
import re, struct, os

class Client(object):

	def __init__(self):
		Host = '127.0.0.1'
		Port = 8000
		self.CliSock = socket(AF_INET, SOCK_STREAM)
		self.CliSock.connect((Host, Port))

	def main(self):
		regex = re.compile(r'^(1|2|3)$')
		while True:
			choice = raw_input('1.upload\n2.download\n3.exit\ninput your choice:> ')
			res = regex.search(choice)
			if not res:
				print 'Usage: [1-3]'
				continue
			elif choice == '3':
				break
			elif choice == '1':
				self.CliSock.sendall(choice)
				self.upload()
			elif choice == '2':
				self.CliSock.sendall(choice)
				self.download()
		print 'bye!'
		self.CliSock.close()

	def upload(self):
		filelist = [ f for f in os.listdir('.') if os.path.isfile(f) ]
		for i in filelist:
			print i
		UploadFile = raw_input('input file name:> ')
		if not os.path.exists(UploadFile):
			print 'file not exist'
			return
		fhead = struct.pack('128sl', UploadFile, os.path.getsize(UploadFile))
		self.CliSock.send(fhead)
		with open(UploadFile, 'rb') as f:
			while True:
				data = f.read(1024)
				if not data:
					break
				self.CliSock.send(data)
		print 'send file:%s succeed' % UploadFile

	def download(self):
		flist = self.CliSock.recv(1024)
		print flist.strip('\00')
		fname = raw_input('input file name:> ')
		fnameinfo = struct.pack('128s', fname)
		self.CliSock.send(fnameinfo)
		fheadsize = struct.calcsize('128sl')
		fheadinfo = self.CliSock.recv(fheadsize)
		fname, fsize = struct.unpack('128sl', fheadinfo)
		recv_size = 0
		with open(fname.strip('\00'), 'wb') as f:
			while not recv_size == fsize:
				if fsize - recv_size > 1024:
					data = self.CliSock.recv(1024)
					if not data:
						break
				else:
					data = self.CliSock.recv(fsize-recv_size)
					if not data:
						break
					recv_size += len(data)
				f.write(data)
		print 'recived file:%s ' % fname.strip('\00')

client = Client()
client.main()