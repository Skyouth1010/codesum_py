#-*- coding: utf-8 -*-
import os

commands = ['get','set','lpush','lpop']
concurrency = [10000,20000,30000,40000,50000]
fw=open("an.txt","a")
for c in commands:
    fw.write(c+"\t"+"minseconds"+"\t"+"maxseconds"+"\t"+"avgseconds"+"\t"+"maxtps"+"\t"+"mintps"+"\t"+"avgtps"+"\n")
    for num in concurrency:
        minseconds = 100
        maxseconds = 0
        toalseconds = 0
        maxtps = 0
        mintps = 20000
        totaltps = 0
        for i in range(1,11):
            outputfile = "./"+ c + "/" + str(num) + "/c" + str(i) + ".out"
            if not os.path.exists(outputfile):
                continue
            f=open(outputfile,'r')
            for line in f:
                if line.find("completed")>0:
                    res = line.strip().split(" ")[4]
                    if (float(res) > maxseconds):
                        maxseconds = float(res)
                    elif (float(res) < minseconds):
                        minseconds = float(res)
                    toalseconds += float(res)
                if line.find("requests per second")>0:
                    res = line.strip().split(" ")[0]
                    if (float(res) > maxtps):
                        maxtps = float(res)
                    elif (float(res) < mintps):
                        mintps = float(res)
                    totaltps += float(res)
            f.close()
        fw.write(str(num)+"\t")
        fw.write(str(minseconds)+"\t")
        fw.write(str(maxseconds)+"\t")
        fw.write(str(toalseconds/10)+"\t")
        fw.write(str(maxtps)+"\t")
        fw.write(str(mintps)+"\t")
        fw.write(str(totaltps/10)+"\t\n")
fw.close()