#-*- coding: utf-8 -*-
from dayLogAnalysis import dayLogAnalysis
from dayChinaolLogAnalysis import dayChinaolLogAnalysis
from dayAbeTimesLogAnalysis import dayAbeTimesLogAnalysis
import time,calendar
from datetime import date

with open("Readme.txt","r") as f:
    print f.read()
print '\n'
continueFlag = "y"
while(continueFlag == "y" or continueFlag == "yes"):
    nowDay = raw_input(u'请输入要分析的日志日期:'.encode("utf-8"))
    if len(nowDay) == 6:
        #当前日期
        days = time.strftime('%d',time.localtime(time.time()))
        try:
            if date.today().replace(int(nowDay[0:4]), int(nowDay[4:6]), int(days)) < date.today():
                #如果是以前的月份，正月循环
                ca = calendar.Calendar().itermonthdays(int(nowDay[0:4]),int(nowDay[4:6]))
            else:
                ca = []
        except Exception as error:
            print 'format error'
            print error
            continue
        localPath = raw_input(u'请输入分析结果产出文件路径:'.encode("utf-8"))
        nowMonth = nowDay[0:4] + "-" + nowDay[4:6]
        if localPath=='':
            localPath="D:/ftpserver/logs/"+nowMonth+"/"
        if ca == []:
            #如果是当前月份，循环到当天为止
            ca = range(int(days)+1)
        #flight,hotel,other,ewinws
        errorMsgsMonth=[{},{},{},{}]
        totalDays = 0
        for i in ca:
            if i == 0:continue
            if i>totalDays:
                totalDays = i
            day = str(nowDay) + str(i).zfill(2)
            try:
                errorMsgs = dayLogAnalysis(day,localPath)
                #dayChinaolLogAnalysis(day,localPath)
                dayAbeTimesLogAnalysis(day,localPath)
                for cnt in range(len(errorMsgs)):
                    for k,v in errorMsgs[cnt].iteritems():
                        if k not in errorMsgsMonth[cnt]:
                            errorMsgsMonth[cnt][k] = v
                        else:
                            errorMsgsMonth[cnt][k] += v
            except Exception as error:
                print day + " analysis failed"
                print error
                continue
        fw=open(localPath+"averageLogAnalysis.txt","a")
        for eachErrorMsgsMonth in errorMsgsMonth:
            fw.write("------------------------------------------------------------------------------\n")
            for errorMsgF in sorted(eachErrorMsgsMonth.iteritems(),key=lambda d:d[1],reverse = True):
                if errorMsgF[0].find("\n") < 0 and errorMsgF[0].find("\r\n") < 0:
                    fw.write(str(errorMsgF[1]/totalDays) + "次：" + errorMsgF[0] + "\n")
                else:
                    fw.write(str(errorMsgF[1]/totalDays) + "次：" + errorMsgF[0])
        fw.close
    else:
        if len(nowDay) == 8:
            try:
                date.today().replace(int(nowDay[0:4]), int(nowDay[4:6]), int(nowDay[6:8]))
            except:
                print 'format error'
                continue
        elif len(nowDay) > 8 or (len(nowDay) < 8 and len(nowDay) > 0):
            print 'format error'
            continue
        localPath = raw_input(u'请输入分析结果产出文件路径:'.encode("utf-8"))
        try:
            dayLogAnalysis(nowDay,localPath)
            dayChinaolLogAnalysis(nowDay,localPath)
            dayAbeTimesLogAnalysis(nowDay,localPath)
        except Exception, e:
            print e
    continueFlag = raw_input(u"处理结束，日志分析输出：".encode("utf-8")+localPath+"*logAnalysis.txt\n"
              +u"是否继续处理（yes/no）:".encode("utf-8"))
