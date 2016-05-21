#-*- coding: utf-8 -*-
import time,os,re
from datetime import date,timedelta,datetime

def uipLogAnalysis(uiplogsFile,logOutput):
    fw=open(logOutput,"a")
    fw.write("\n------------------------------------"+uiplogsFile[uiplogsFile.rfind("/")+1:]+"统计数据------------------------------\n")
    f=open(uiplogsFile,'r')
    #errorMsgs结构：{错误信息：{"detail":详细错误信息,"count":计数}}
    #错误信息为[ERROR]所在行的信息，详细错误信息为其下一行
    #lineError有两条错误信息后清空，第一条是错误信息，第二条是详细错误信息
    errorMsgs={}
    lineError=[]
    #去重用变量
    errorSet=set()
    duplicate = False
    for line in f:
        #跳过多余日志
        if line.find("[ERROR]") > 0 and line.find("com.chinaol.Client") > 0 and line.find("send error") > 0:
            continue
        #日志存在重复打印的，去重
        if duplicate:
            if line.find("[ERROR]") > 0:
                duplicate = False
            else:
                continue
        #三种日志可能重复：com.rb.owk.wolfs.ebox，com.elong，com.chinaol
        if line.find("[ERROR]") > 0 and (line.find("com.rb.owk.wolfs.ebox") > 0
                                         or line.find("com.elong") > 0
                                         or line.find("com.chinaol") > 0):
            errorNotExist = line.split("]:")[0]
            if errorNotExist not in errorSet:
                errorSet.add(errorNotExist)
            else:
                duplicate = True
                continue
        #组装errorMsgs变量
        if len(lineError) == 1:
            if line.find("[ERROR]") > 0:
                #连续两行有[ERROR]，说明没有详细错误信息，直接计数
                if lineError[0] not in errorMsgs:
                    errorMsgs[lineError[0]]={"detail":lineError[0],"count":1}
                else:
                    errorMsgs[lineError[0]]["count"]+=1
                #清空lineError，从头开始
                lineError = []
                lineError.append(line.split("]:")[1])
            else:
                lineError.append(line)
                if lineError[0] not in errorMsgs:
                    errorMsgs[lineError[0]]={"detail":line,"count":1}
                else:
                    errorMsgs[lineError[0]]["count"]+=1
                #清空lineError
                lineError = []
        elif line.find("[ERROR]") > 0:
            lineError.append(line.split("]:")[1])
    errorMsgsFormat={}
    #errorMsgsFormat结构：{错误信息：错误次数}，错误信息可能为[ERROR]所在行的信息，也可能为其下一行
    errors = ["ATS错误：指令发送超时。"]
    errors.append("到到 远程访问出错: org.apache.axis2.databinding.ADBException: Unexpected subelement url")
    errors.append("Server returned HTTP response code: 500 for URL: http://switch.chinaonline.net.cn/Col_switch_ws/Availability.asmx?op=Availability")
    errors.append("Server returned HTTP response code: 500 for URL: http://content.daodao.com/ContentService")
    errors.append("planPolicySchedule失败")
    errors.append("orderMaintainInit失败")
    errors.append("提取电子客票票面失败")
    errors.append("ATS错误：网络通讯错误，请重试或检查ATS状态")
    errors.append("preparePolicySchedule失败")
    errors.append("ABE远程方法调用错误，请核对报文参数")
    errors.append("\s*外部获取\S*天气失败，请检查网络/账户原因！")
    errors.append("\s*getTicketNoResponse\S*异常")
    errors.append("\s*(\d\.\S+\s)+[A-Z0-9]{6}")
    errors.append("畅联创建订单失败！")
    errors.append("畅联取消订单失败！")
    errors.append("cancelOrder失败")
    errors.append("畅联 远程访问出错: System.Web.Services.Protocols.SoapException: Server was unable to process request.")
    for errorMsg in errorMsgs:
        if errorMsg.find("运行错误：") >= 0:
            detail = errorMsgs[errorMsg]["detail"].split("EBoxException:")[1]
            for error in errors:
                if detail.find(error) >= 0:
                    detail = error
                    break
            if detail in errorMsgsFormat:
                errorMsgsFormat[detail] += 1
            else:
                errorMsgsFormat[detail] = 1
        else:
            abbr = ""
            for error in errors:
                if errorMsg.find(error) >= 0 or re.match(error,errorMsg):
                    if "\s*(\d\.\S+\s)+[A-Z0-9]{6}"==error:
                        abbr = "退改签失败原因：PNR未出票"
                    else:
                        abbr = error
                    break
            if abbr != "":
                if abbr in errorMsgsFormat:
                    errorMsgsFormat[abbr] += errorMsgs[errorMsg]["count"]
                else:
                    errorMsgsFormat[abbr] = errorMsgs[errorMsg]["count"]
            else:
                frequentErrors=["Read timed out","Network is unreachable","Connection refused",
                                "The host did not accept the connection within timeout of 20000 ms",
                                "Can't overwrite cause","instantConfirmResponse is null"]
                for error in frequentErrors:
                    if errorMsg.find("Chinaol.availability")>=0:
                        abbr = "Chinaol.availability["+error+"]"
                        break
                    elif errorMsg.find("ELONG.getHotelList")>=0 or errorMsg.find("艺龙 getHotelList")>=0:
                        abbr = "ELONG.getHotelList["+error+"]"
                        break
                    elif errorMsg.find("ELONG.getHotelOrderDetailById")>=0:
                        abbr = "ELONG.getHotelList["+error+"]"
                        break
                    elif errorMsg.find("Elong.instantConfirm failed")>=0:
                        abbr = "Elong.instantConfirm failed["+error+"]"
                        break
                    elif errorMsg.find("畅联 远程访问出错: ")>=0:
                        abbr = "畅联 远程访问出错: "+error
                        break
                else:
                    abbr = errorMsg
                if abbr in errorMsgsFormat:
                    errorMsgsFormat[abbr] += errorMsgs[errorMsg]["count"]
                else:
                    errorMsgsFormat[abbr] = errorMsgs[errorMsg]["count"]
    for errorMsgF in sorted(errorMsgsFormat.iteritems(),key=lambda d:d[1],reverse = True):
        if errorMsgF[0].find("\n") < 0 and errorMsgF[0].find("\r\n") < 0:
            fw.write(str(errorMsgF[1]) + "次：" + errorMsgF[0] + "\n")
        else:
            fw.write(str(errorMsgF[1]) + "次：" + errorMsgF[0])
    f.close()
    #os.remove(uiplogsFile)
    fw.close()
    return errorMsgsFormat
