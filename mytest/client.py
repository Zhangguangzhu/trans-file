#coding:utf-8
import traceback
from socket import *
import struct, json, hashlib,os,time,sys

class Client(object):

	def __init__(self):
		self.host = ''
		self.port = 9999
		self.addr = (self.host, self.port)
		self.ClientSock = socket(AF_INET, SOCK_STREAM)
		self.readsize = 1024
		self.ClientSock.connect(self.addr)

	def check_md5(self, filename):
		md5_value = self.ClientSock.recv(32)
		check_md5 = hashlib.md5()
		with open(filename+'.temp', 'r') as f:
			for line in f.xreadlines():
				check_md5.update(line)
		download_file_md5 = check_md5.hexdigest()
		print 'downloadfilemd5: %s\nrealmd5:%s' % (download_file_md5, md5_value)
		if download_file_md5 != md5_value:
			print 'download failed'
		else:
			print 'download success'
			os.rename(filename+'.temp', filename)
			if os.path.exists(filename+'.temp_info'):
				os.remove(filename+'.temp_info')

	def trans_data(self):
		filelist = self.ClientSock.recv(1024)
		print filelist
		download_file = raw_input('input file name:  ')
		if os.path.exists(download_file+'.temp_info'):
			with open(download_file+'.temp_info', 'r') as f:
				count = int(f.read())
				openmode = 'ab'
		else:
			count = 0
			openmode = 'wb'
		requst_file_info = struct.pack('i124s', count, download_file)
		self.ClientSock.sendall(requst_file_info)
		with open(download_file+'.temp', openmode) as f:
			try:
				while True:
					real_data_len_str = self.ClientSock.recv(4)
					real_data_len = struct.unpack('i', real_data_len_str)
					# print real_data_len
					remain_data_len = real_data_len[0]
					if not real_data_len[0]:
						break
					elif real_data_len[0] == 0:
						break
					while True:
						recv_data = self.ClientSock.recv(remain_data_len)
						f.write(recv_data)
						recv_data_len = len(recv_data)
						remain_data_len = remain_data_len - recv_data_len
						if remain_data_len <= 0:
							break
			except KeyboardInterrupt:
				count = str(f.tell())
				with open(download_file+'.temp_info', 'w') as f:
					f.write(count)
				self.ClientSock.close()
				raise

		self.check_md5(download_file)

if __name__ == '__main__':
	try:
		client = Client()
		client.trans_data()
	except KeyboardInterrupt as e:
		print 'closed connection', e