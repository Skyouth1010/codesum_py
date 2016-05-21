#-*- coding: utf-8 -*-
from datetime import timedelta,datetime

f=open("D:/ftpserver/logs/2013-02/getHotelList2.22.log",'r')
fNull=open("D:/ftpserver/logs/2013-02/null.txt",'r')
fw=open("D:/ftpserver/logs/2013-02/getHotelList2.22new_2s.log","a")
logtime,logThread=[],[]
for line in fNull:
    lineTime = datetime(2013,2,26,int(line[9:11]),int(line[12:14]),int(line[15:17]),int(line[18:21])*1000)
    lineThread = line.split("]:")[0].split("HtlElongServiceImpl")[1]
    if len(logtime) == 0 or logtime[len(logtime)-1] != lineTime:
        logtime.append(lineTime)
        logThread.append(lineThread)
fNull.close()

for line in f:
    timeLog = datetime(2013,2,26,int(line[9:11]),int(line[12:14]),int(line[15:17]),int(line[18:21])*1000)
    for cnt in range(len(logtime)):
        if timeLog <= logtime[cnt] and timeLog > logtime[cnt]-timedelta(seconds=2) and line.find(logThread[cnt])>0:
            fw.write(line)
            break
        elif timeLog < logtime[cnt]-timedelta(seconds=2):
            break
f.close()
fw.close()
