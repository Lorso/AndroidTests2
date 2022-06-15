import schedule
import time
import paramiko

from Functions.TelegramApi import Send_File
from Functions.TelegramApi import SendMessage
from Functions.DataName import NowDate
from Tests.Tests_Auth import AutoTest


#from Tesdroid import startIos
import os
from subprocess import Popen
def startIos():
 host = "127.0.0.1"
 port = 22
 username = "mobile"
 password = "alpine"

 command = "/usr/local/bin/4iniziator123base"

 ssh = paramiko.SSHClient()
 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 ssh.connect(host, port, username, password)

 stdin, stdout, stderr = ssh.exec_command(command)
 lines = stdout.readlines()
 print(lines)

def job():

    startIos()
    import Test_MT_Auth
#schedule.every().day.at("10:34").do(job)


startIos()
while True:
    schedule.run_pending()
    time.sleep(1)