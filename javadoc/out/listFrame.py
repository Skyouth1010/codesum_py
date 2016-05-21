from mod_python import apache
import os
from common import *

def listFrameIndex(req):
    s = listIndex("overview-frame.html")
    href = ''
    hostUrl = 'http://' + req.hostname+'/'
    dirVer = listDirectory()
    for item in dirVer.keys():
        href = href + '<li>' + item + '<ul>'
        for ver in dirVer[item]:
            href = href + '<li> <a href="javascript:this.loadFrames(\''\
                + hostUrl + item + '/' + ver + '/\',\'' + hostUrl\
                + 'versionInfo.py/handler?item='+item+'&ver='+ver + '\')">' + ver + '</a></li>'
        href = href + '</ul></li>'
    print href
    return s.replace('{0}',href)
    
def handler(req):
    req.content_type = "text/html"
    req.write(listFrameIndex(req))

if __name__=='__main__':
    print listDirectory()
