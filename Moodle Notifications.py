import requests
from bs4 import BeautifulSoup,SoupStrainer
import time
import getpass
import subprocess

import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify

class MoodleNotifications:

	baseurl="http://id.bits-hyderabad.ac.in/moodle/"
	

	def __init__(self):
		#Load Cookie from file
		#Check validity of cookie by getting home page
		#If invalid, promt for login
		self.ses=requests.session()
		self.login()

	def login(self):
		print('Username: ',end='')
		uname=input()
		pwd=getpass.getpass('Password: ')
		authdata = {
			'action': 'login',
			'username': uname,
			'password': pwd
		}
		res = self.ses.post(self.baseurl+'login/index.php',data=authdata,allow_redirects=False)
		#print(res.status_code)

	def getUnixTimeStamp(self,da):
		# da="Monday, 1 May 2017, 10:04 AM"
		# da must be of the above format

		s=da.split(',')
		d=s[1][1::]
		t=s[2][1::]
		t=time.strptime(d+' '+t,"%d %B %Y %I:%M %p")
		return time.mktime(t)

	def getLastAccessedCourse(self,id,course):
		params={
				"id":id,
				"course":course
				}
		r=self.ses.get(self.baseurl+'user/view.php',params=params)
		only_dd = SoupStrainer("dd")
		s=BeautifulSoup(r.text,"html.parser",parse_only=only_dd)
		datestring=s.find_all("dd")[2].string
		j=0
		for i in range(1,len(datestring)):
			if datestring[i]=='M' and (datestring[j]=='A' or datestring[j]=='P'):
				break
			else:
				j=j+1
		t=datestring[0:j+2:]
		return self.getUnixTimeStamp(t)
	
	def getLastLoggedIn(self,id):
		params={
			"id":id
		}
		r=self.ses.get(self.baseurl+'user/view.php',params=params)
		only_dd = SoupStrainer("dd")
		s=BeautifulSoup(r.text,"html.parser",parse_only=only_dd)
		datestring=s.find_all("dd")[2].string
		j=0
		for i in range(1,len(datestring)):
			if datestring[i]=='M' and (datestring[j]=='A' or datestring[j]=='P'):
				break
			else:
				j=j+1
		t=datestring[0:j+2:]
		return self.getUnixTimeStamp(t)


userid=5150
courseid=1965
m=MoodleNotifications()
t0=m.getLastAccessedCourse(userid,courseid)
i=0
while(True):
	t1=m.getLastAccessedCourse(userid,courseid)
	print(t0,t1,' ',i*5,'minutes passed')
	if(t1>t0):
		Notify.init("Moodle Notifications")
		Noti=Notify.Notification.new("Moodle Notifications","Public Policy Course Updated")
		Noti.show()
		print("Changed")
		
		break
	t0=t1
	i=i+1
	time.sleep(300)
