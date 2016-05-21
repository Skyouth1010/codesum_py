import os

local = 'D:\python\javadocout\\'

def listDirectory():
    dir = os.listdir(local)
    for item in dir[:]:
        if not os.path.isdir(local+item):
            dir.remove(item)
    dirVer = {}
    for item in dir:
        vers = os.listdir(local+item)
        for ver in vers[:]:
            if not os.path.isdir(local+item+'\\'+ver):
                vers.remove(ver)
        dirVer[item] = vers
    return dirVer

def listIndex(hf):
    with open(getLocalPath()+hf,"r") as f:
        s = f.read()
    return s

def getLocalPath():
    return local