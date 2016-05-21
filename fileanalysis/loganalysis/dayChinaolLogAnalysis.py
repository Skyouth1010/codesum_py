#-*- coding: utf-8 -*-
from ftpUtils import MyFTP
from uipLogAnalysis import uipLogAnalysis
from owkLogAnalysis import owkLogAnalysis
import time,zlib,tarfile,os
from datetime import date,timedelta,datetime

def dayChinaolLogAnalysis(nowDay, localPath):
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
    '''
    lf = MyFTP()
    try:
        if not os.path.exists(localPath+fileNameOwk):
            lf.download("99.6.137.69","21","sync","sync",
                        remotePath+fileNameOwk,localPath+fileNameOwk)
            print fileNameOwk+' download successfully!'
        else:
            print fileNameOwk+' exist'
        if not os.path.exists(localPath+fileNameUip):
            lf.download("99.6.137.69","21","sync","sync",
                        remotePath+fileNameUip,localPath+fileNameUip)
            print fileNameUip+' download successfully!'
        else:
            print fileNameUip+' exist'
    except:
        raise
    else:
        print 'files decompressing!'
        #文件已解压就直接使用
        if not (os.path.exists(localPath+"uip-hotel-warn.log." + yesterday2)):
            tarobj = tarfile.open(localPath+fileNameUip, "r:gz")
            for tarinfo in tarobj:
                if tarinfo.name.find("hotel-warn") >= 0:
                    uiplogsFiles.append(localPath+tarinfo.name)
                    if not os.path.exists(localPath+tarinfo.name):
                        tarobj.extract(tarinfo.name, localPath)
                else:
                    pass
            tarobj.close()
        else:
            uiplogsFiles.append(localPath+"uip-hotel-warn.log." + yesterday2)
    print 'decompressed!'
    print uiplogsFiles
    '''

    fw=open(localPath+"chinaol.txt","a")
    f=open(localPath+"uip-hotel-warn.log." + yesterday2,'r')
    for line in f:
        if line.find("Chinaol.createBooking success") > 0 :
            fw.write(line[0:8]+"\t" +line.split("! ")[1].split("ms")[0]+"\n")
    f.close()
    #os.remove(uiplogsFile)
    fw.close()
    
    print 'analyzed'
