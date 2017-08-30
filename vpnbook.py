import requests
import re
from subprocess import Popen,PIPE,call
from bs4 import BeautifulSoup

r=requests.get('http://176.126.252.71/')
f=r.text
soup=BeautifulSoup(f,'html.parser')
#f.close()

ans=soup.find(text=re.compile('Password: '))
ans=ans.split(' ')
print(ans[1])
password=ans[1]

pathtoovpnfile=""
try:
	call(["sudo","openvpn",pathtoovpnfile])
except KeyboardInterrupt:
	print("Exiting")
#p=Popen(["sudo","openvpn",pathtoovpnfile],stdin=PIPE)
#p.communicate(input=('vpnbook\n'+password+'\n'))
