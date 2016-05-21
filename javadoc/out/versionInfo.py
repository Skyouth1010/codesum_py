#-*- coding: utf-8 -*-
from mod_python import apache
import os,ConfigParser
from common import *

def listVerIndex(req, hf, item, ver):
    s = listIndex(hf)
    print s
    cf = ConfigParser.ConfigParser()
    cf.read(getLocalPath()+item+'/'+ver+'/version.conf')
    if cf is not None:
        s = s.replace('{prj}',cf.get("version","project"))
        s = s.replace('{ver}',cf.get("version","version"))
        s = s.replace('{date}',cf.get("version","date"))

    if os.path.exists(getLocalPath()+item+'/'+ver+'/changeFiles.txt'):
        f=open(getLocalPath()+item+'/'+ver+'/changeFiles.txt','r')
        aline=''
        for line in f:
            href = 'http://' + req.hostname+'/'+item+'/'+ver +'/' +line.replace('.','/') + '.html'
            aline = aline + '<a href="' +href+ '" target="javadocFrame">'+line+'</a>'
        s = s.replace('{changeFiles}',aline)
    else:
        s = s.replace('{changeFiles}',u'无'.encode('gbk'))

    if os.path.exists(getLocalPath()+item+'/'+ver+'/javasrc.rar'):
        s = s.replace('{javadl}','http://' + req.hostname+'/'+item+'/'+ver +'/javasrc.rar')
    else:
        s = s.replace('{jdstyle}','display:none')

    if os.path.exists(getLocalPath()+item+'/'+ver+'/cssrc.rar'):
        s = s.replace('{csdl}','http://' + req.hostname+'/'+item+'/'+ver +'/cssrc.rar')
    else:
        s = s.replace('{csstyle}','display:none')
    return s

def handler(req, item, ver):
    req.content_type = "text/html"
    req.write(listVerIndex(req, "versionInfo.html", item, ver))

if __name__=='__main__':
    print listDirectory()
