import sys, time

total = 31
current = 0






while total > current:
	current += 1
	sys.stdout.write("\r" + '  {:.2%}'.format(current/total) + "\r")
	sys.stdout.flush()
