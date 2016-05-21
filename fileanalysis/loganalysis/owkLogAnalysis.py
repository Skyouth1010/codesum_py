#-*- coding: utf-8 -*-
from datetime import datetime

def owkLogAnalysis(owklogsFiles,logOutput):
    if len(owklogsFiles) == 0: pass
    nowDay2 = owklogsFiles[0][-10:]
    fw=open(logOutput,"a")
    fw.write("\n------------------------------------"+nowDay2+"配送统计数据------------------------------\n")
    for log in owklogsFiles:
        opts,addjobs,cnt=[],[],[0,0,0]
        with open(log,'r') as f:
            for line in f:
                if line.find(u"定时任务开始过号处理！".encode("utf-8")) > 0:
                    if len(opts)%2 != 0:
                        opts.append("error")
                    opts.append(line[0:10] + " " + line[12:20])
                elif line.find(u"定时任务过号处理结束！".encode("utf-8")) > 0:
                    opts.append(line[0:10] + " " + line[12:20])
                elif ((line.find(u"开始生成作业档！".encode("utf-8")) > 0 and line.find("OperationAddJob") > 0)
                or line.find(u"TMC发票作业档生成完成！".encode("utf-8")) > 0):
                    addjobs.append(line[0:10] + " " + line[12:20])
                elif line.find(u"过号操作失败----无需处理".encode("utf-8")) > 0:
                    cnt[0] += 1
                elif line.find(u"过号操作失败----异常".encode("utf-8")) > 0:
                    cnt[1] += 1
                elif line.find(u"过号操作失败".encode("utf-8")) > 0:
                    cnt[2] += 1
        optTimes,optWarnTimes,optErrorCnt,optSuccessCnt=[],[],0,0
        for i in range(0,len(opts), 2):
            if i+1 >= len(opts):
                optErrorCnt += 1
            elif opts[i+1] == "error":
                optErrorCnt += 1
            else:
                start = datetime.strptime(opts[i],'%Y-%m-%d %H:%M:%S')
                end = datetime.strptime(opts[i+1],'%Y-%m-%d %H:%M:%S')
                optTimes.append((end-start).total_seconds())
                if (end-start).total_seconds() >= 40 :
                    optWarnTimes.append({opts[i] : (end-start).total_seconds()})
                optSuccessCnt += 1
        start = datetime.strptime(addjobs[0],'%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(addjobs[1],'%Y-%m-%d %H:%M:%S')
        fw.write("过号定时任务耗时(秒)："+str(optTimes))
        fw.write("\n耗时超过40秒的过号定时任务："+str(optWarnTimes))
        fw.write("\n生成作业档定时任务耗时(分)："+str((end-start).total_seconds()/60))
        fw.write("\n过号定时任务成功次数："+str(optSuccessCnt))
        fw.write("\n过号定时任务失败次数："+str(optErrorCnt))
        fw.write("\n过号操作失败----无需处理次数："+str(cnt[0]))
        fw.write("\n过号操作失败----异常次数："+str(cnt[1]))
        fw.write("\n过号操作失败次数："+str(cnt[2]))
    fw.close()
