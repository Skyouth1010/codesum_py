#-*- coding: utf-8 -*-
from ftpUtils import MyFTP
from uipLogAnalysis import uipLogAnalysis
from owkLogAnalysis import owkLogAnalysis
import time,tarfile,os
from datetime import date,timedelta

def dayLogAnalysis(nowDay, localPath):
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
    lf = MyFTP()
    try:
        if not os.path.exists(localPath+fileNameOwk):
            try:
                lf.download("99.6.137.69","21","sync","sync",
                        remotePath+fileNameOwk,localPath+fileNameOwk)
            except:
                print fileNameOwk+' NOT FOUND.'
            else:
                print fileNameOwk+' download successfully!'
        else:
            print fileNameOwk+' exist'
        if not os.path.exists(localPath+fileNameUip):
            try:
                lf.download("99.6.137.69","21","sync","sync",
                        remotePath+fileNameUip,localPath+fileNameUip)
            except:
                print fileNameUip+' NOT FOUND.'
            else:
                print fileNameUip+' download successfully!'
        else:
            print fileNameUip+' exist'
    except:
        raise
    else:
        print 'files decompressing!'
        #文件已解压就直接使用
        '''
        if not os.path.exists(localPath+"log/SL/" + nowDay + "/log/SL/owk-1.15/system-job.logjobowDay2):
            if os.path.exists(localPath+fileNameOwk):
                tarobj = tarfile.open(localPath+fileNameOwk, "r:gz")
                for tarinfo in tarobj:
                    if tarinfo.name.find("system") >= 0:
                        owklogsFiles.append(localPath+tarinfo.name)
                        if not os.path.exists(localPath+tarinfo.name):
                            tarobj.extract(tarinfo.name, localPath)
                    else:
                        pass
                tarobj.close()
        else:
            owklogsFiles.append(localPath+"log/SL/" + nowDay + "/log/SL/owk-1.15/system-job.logjobowDay2)
        '''
        if not (os.path.exists(localPath+"uip-flight-error.log." + yesterday2)
                and os.path.exists(localPath+"uip-hotel-error.log." + yesterday2)
                and os.path.exists(localPath+"uip-other-error.log." + yesterday2)):
            if os.path.exists(localPath+fileNameUip):
                tarobj = tarfile.open(localPath+fileNameUip, "r:gz")
                for tarinfo in tarobj:
                    if tarinfo.name.find("error") >= 0 or tarinfo.name.find("uip-flight-warn") >= 0:
                        uiplogsFiles.append(localPath+tarinfo.name)
                        if not os.path.exists(localPath+tarinfo.name):
                            tarobj.extract(tarinfo.name, localPath)
                    else:
                        pass
                tarobj.close()
        else:
            uiplogsFiles.append(localPath+"uip-flight-error.log." + yesterday2)
            uiplogsFiles.append(localPath+"uip-hotel-error.log." + yesterday2)
            uiplogsFiles.append(localPath+"uip-other-error.log." + yesterday2)
    print 'decompressed!'
    try:
        owkLogAnalysis(owklogsFiles,localPath+"owkLogAnalysis.txt")
    except Exception as error:
        print nowDay + "owk analysis failed"
        print error
    if len(uiplogsFiles) == 0:
        print 'no uiplog Files'
        return []
    errorMsgsFlight, errorMsgsHotel, errorMsgsOther, errorMsgsEwinws={},{},{},{}
    for log in uiplogsFiles:
        if log.find("flight") >= 0:
            errorMsgsFlight = uipLogAnalysis(log,localPath+"flightLogAnalysis.txt")
        elif log.find("hotel") >= 0:
            errorMsgsHotel = uipLogAnalysis(log,localPath+"hotelLogAnalysis.txt")
        elif log.find("other") >= 0:
            errorMsgsOther = uipLogAnalysis(log,localPath+"otherLogAnalysis.txt")
        elif log.find("ewinws") >= 0:
            errorMsgsEwinws = uipLogAnalysis(log,localPath+"ewinwsLogAnalysis.txt")
        else:
            uipLogAnalysis(log,localPath+"logAnalysis.txt")
    print 'analyzed'
    return [errorMsgsFlight, errorMsgsHotel, errorMsgsOther, errorMsgsEwinws]
