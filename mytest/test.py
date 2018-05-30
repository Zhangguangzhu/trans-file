# -*- coding: utf-8 -*-
import time
import traceback


def divison():

	try:
		num1 = int(raw_input('num1: '))
		num2 = int(raw_input('num2:'))
		res = num1 / num2
		time.sleep(10)
	except ZeroDivisionError as e:
		traceback.print_exc()
		print 'num2 can\'t be zero'
	except :
		print 'user interrupt'
		traceback.print_exc()
	else:
		print res
	finally:
		print 'end'


divison()
