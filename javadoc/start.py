#-*- coding: utf-8 -*-
import sys,os
from ifm.flow import IfmFlow
from ifm.logger import Logger
#0、外部参数说明
'''
帮助说明参考ifm.txt
'''
scriptPath=os.path.dirname(sys.argv[0])
log = Logger(scriptPath)
if len(sys.argv) != 4 and len(sys.argv) != 5:
    log.error('input argv incorrect')
    with open(os.path.join(scriptPath,"ifm.txt"),"r") as f:
        print f.read()
    exit()
ifmFlow = IfmFlow(sys.argv)
#1、同步rtc代码
ifmFlow.loadSrc()
#通过调度的频率控制
#if r[0]==0 or '工作空间未更改' in r[1]:
#    logger.error('src unchanged')
#    exit()
#2、生成javadoc，暂且不考虑成功与否，可通过日志分析
ifmFlow.javadoc()
#3、javadoc版本比较，生成changelist
ifmFlow.listChangedClasses()
#4、生成word文档
#5、生成cs代码并打包
#6、打包java-api源码
ifmFlow.jarApi()
#7、生成版本信息
ifmFlow.genverConf()
#8、上传javadoc、changelist、java/cs代码
ifmFlow.uploadFolder()

    