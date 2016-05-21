#-*- coding: utf-8 -*-
import time as _time,re,calendar
from datetime import *
#from hessianlib import Hessian


nowMonth = _time.strftime('%d',_time.localtime(_time.time()))
localPath="D:/ftpserver/logs/"+nowMonth+"/"
#nowDay = raw_input('please enter the date(YYYYMMDD) of logAnalysis:')
#print str(date.today().replace(int(nowDay[0:4]), int(nowDay[4:6]), int(nowDay[6:8]))-timedelta(days=1))
#time.ctime(time.mktime(time.strptime('20130111','%Y%m%d')))-timedelta(days=1)
#owkLogAnalysis(['D:/ftpserver/logs/2013-01/log/SL/20130109/log/SL/owk-1.15/system-job.log2013-01-09'],localPath+"logAnalysis.txt")
#uipLogAnalysis(['D:/ftpserver/logs/2013-01/uip-flight-error.log.2013-01-09','D:/ftpserver/logs/2013-01/uip-hotel-error.log.2013-01-09','D:/ftpserver/logs/2013-01/uip-other-error.log.2013-01-09'],localPath+"logAnalysis.txt")
'''
url = "http://99.6.137.241/dis/ebox"
proxy = Hessian(url)
#response = proxy.__invoke('selectDisArea',{"areaLevel":1,"areaType":1})
response = proxy.helloworld()
print response
'''
