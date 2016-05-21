#-*- coding: utf-8 -*-
from ftpUtils import MyFTP
from uipLogAnalysis import uipLogAnalysis
from owkLogAnalysis import owkLogAnalysis
import time,zlib,tarfile,os
from datetime import date,timedelta,datetime

def dayAbeTimesLogAnalysis(nowDay, localPath):
    if nowDay == '':
        nowDay = time.strftime('%Y%m%d',time.localtime(time.time()))
    nowMonth = nowDay[0:4] + "-" + nowDay[4:6]
    nowDay2 = nowMonth + "-" + nowDay[6:8]
    yesterday=(date.today().replace(int(nowDay[0:4]), int(nowDay[4:6]),
            int(nowDay[6:8]))-timedelta(days=1)).strftime('%Y%m%d')
    yesterday2=(date.today().replace(int(nowDay[0:4]), int(nowDay[4:6]),
            int(nowDay[6:8]))-timedelta(days=1)).strftime('%Y-%m-%d')
    remotePath="/"+u"商旅系统".encode('utf-8')+"/"+nowMonth+"/"+nowDay+"/"
    if localPath == '':
        localPath = "D:/ftpserver/logs/"+nowMonth+"/"
    fileNameOwk="sl-19-"+yesterday+".tar.gz"
    fileNameUip="uip-logserver-"+nowDay2+".tar.gz"
    owklogsFiles,uiplogsFiles=[],[]

    fw=open(localPath+"abeTimes.txt","a")
    f=open(localPath+"uip-flight-warn.log." + yesterday2,'r')
    spliter = "通过WebService外联访问机票接口耗时:"
    count,times = 0,0
    for line in f:
        if line.find(spliter) > 0 :
            count = count + 1
            times = times + int(line.split(spliter)[1].split("ms")[0])
    fw.write("uip-flight-warn.log." + yesterday2 + ",访问ABE次数：")
    fw.write(str(count) + ",总耗时：" + str(times) + ",平均耗时：" + str(times/count) + "\n")
    f.close()
    #os.remove(uiplogsFile)
    fw.close()
    
    print 'analyzed'
