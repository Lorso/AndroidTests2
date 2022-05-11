from subprocess import Popen
import time



k=0
while k<1000:
 Popen('pytest --alluredir results Test_MT.py')
 time.sleep(5400)
 k+=1