from subprocess import Popen
import time



k=0
while k<1000:
 Popen('pytest -s Test_MT_Ident.py')
 time.sleep(4000)
 Popen('pytest -s Test_MT_Auth.py')
 time.sleep(3600)
 k+=1



