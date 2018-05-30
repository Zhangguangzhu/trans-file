#coding: utf-8
import threading
from socket import *
import json, os, struct,traceback,sys

class Server(object):

	def __init__(self):
		self.host = ''
		self.port = 9999
		self.addr = (self.host, self.port)
		self.SerSock = socket(AF_INET, SOCK_STREAM)
		self.SerSock.bind(self.addr)
		self.SerSock.listen(3)
		self.readsize = 1024
		os.chdir('file/')

	def get_md5(self, filename):
		with open('hash.json', 'r') as f:
			hash_dict = json.load(f, encoding='utf-8')
			return hash_dict[filename]

	def trans_data(self, clientsock):

		file_list_str = os.listdir('.')
		filelist = ''
		for filename in file_list_str:
			filelist += filename+'\n'
		try:
			clientsock.sendall(filelist)
		except error as e:
			print 'send filelist failed', e
		recv_file_name_info = clientsock.recv(128)
		if not recv_file_name_info:
			raise error, 'client connection closed'
		recv_file_info, recv_file_name = struct.unpack('i124s', recv_file_name_info)
		recv_file_name = recv_file_name.strip('\x00')
		with open(recv_file_name, 'rb') as f:
			f.seek(recv_file_info)
			while True:
				data = f.read(self.readsize)
				if not data:
					break
				SendData = struct.pack('i%ds' % data.__len__(), data.__len__(), data)
				clientsock.sendall(SendData)
		clientsock.sendall('\x00\x00\x00\x00')
		md5_value = self.get_md5(recv_file_name)
		print md5_value,type(md5_value)
		clientsock.sendall(md5_value)
		clientsock.close()

		print 'send md5 value '

class Create_Threads(threading.Thread):

	def __init__(self, funcname, args):
		super(Create_Threads, self).__init__()
		self.funcname = funcname
		self.args = args
		self.exc_traceback = ''
		self.test = 'hahahaha'
		# self.exitcode = 0
		# self.exception = None

	def run(self):
		# try:
		apply(self.funcname, self.args)
		# except Exception as e:
			# self.exitcode = 1
			# self.exception = e
		self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))
			# raise

def main():
	server = Server()
	try:
		while True:
			print 'waiting for connection'
			ClientSock, ClientAddr = server.SerSock.accept()
			print 'connection from %s:%d' % (ClientAddr[0], ClientAddr[1])
			t = Create_Threads(server.trans_data,(server.trans_data, (ClientSock,))
			t.start()
			print threading.active_count()
	except Exception as e:
		print  e


if __name__ == '__main__':
		main()
		os.access
