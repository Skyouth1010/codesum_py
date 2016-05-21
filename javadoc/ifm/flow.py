#-*- coding: utf-8 -*-
from filecmp import dircmp,cmpfiles
import os,ConfigParser,sys,logger,shutil,time
from util import external_cmd
from ftplib import FTP

class IfmFlow():
    def __init__(self,argv):
        self.scriptPath=os.path.dirname(sys.argv[0])
        self.screamName=sys.argv[1]
        self.assemName=sys.argv[2]
        self.srcPath=sys.argv[3]
        if len(sys.argv) == 5:
            self.workspace = sys.argv[4]
        else:
            self.workspace = 'MyWorkspace'
        self.log = logger.Logger(self.scriptPath)
        cf = ConfigParser.ConfigParser()
        files = []
        files.append(os.path.join(self.srcPath,'javadoc.conf'))
        files.append(os.path.join(self.scriptPath, 'ifm','ifm.conf'))
        cf.read(files)
        self.jdConf={}
        for section in cf.sections():
            for c in cf.items(section):
                self.jdConf[section+'.'+c[0]]=c[1]
    
    def loadSrc(self):
        scmCmd=[]
        scmCmd.append('scm')
        scmCmd.append('accept')
        scmCmd.append('-r')
        scmCmd.append('local')
        scmCmd.append('-s')
        scmCmd.append(self.screamName)
        scmCmd.append('-C')
        scmCmd.append(self.assemName)
        scmCmd.append('-t')
        scmCmd.append(self.workspace)
        self.log.debug(scmCmd)
        try:
            stdout_val, stderr_val = external_cmd(' '.join(scmCmd))
            if stderr_val is None or stderr_val == '':
                self.log.debug(stdout_val)
                return (1,stderr_val)
            else:
                self.log.error(stderr_val)
                return (0,stderr_val)
        except Exception as er:
            self.log.exception("loadSrc failed")
            return (0,str(er))
    
    def javadoc(self):
        javadoccmd = []
        javadoccmd.append('"'+os.path.join(os.environ.get('JAVA_HOME'),'bin','javadoc')+'"')
        javadoccmd.append('-d')
        javadoccmd.append(os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version']))
        if self.jdConf['javadoc.lib'] is not None and self.jdConf['javadoc.lib'] is not '':
            javadoccmd.append('-classpath')
            javadoccmd.append(';'.join(map(lambda x: os.path.join(self.scriptPath,'ifm','lib',x), self.jdConf['javadoc.lib'].split(';'))))
        javadoccmd.append('-encoding')
        javadoccmd.append(self.jdConf['javadoc.encoding'])
        javadoccmd.append('-public')
        javadoccmd.append('-sourcepath')
        javadoccmd.append(os.path.join(self.srcPath,'src','main','java'))
        javadoccmd.append(self.jdConf['javadoc.package'])
        self.log.debug(javadoccmd)
        try:
            if os.path.exists(os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version'])):
                shutil.rmtree(os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version']))
            stdout_val, stderr_val = external_cmd(' '.join(javadoccmd))
            if stderr_val is None or stderr_val == '':
                self.log.debug(stdout_val)
                self.log.info(u'javadoc生成成功'.encode('gbk'))
                return True
            else:
                self.log.error(u'javadoc生成失败：'.encode('gbk')+stderr_val)
                return False
        except Exception as er:
            self.log.exception("javadoc failed")
            return False

    def listChangedClasses(self):
        '''
        输出两个版本的javadoc中的变更类集合，lf和rf均为javadoc的根目录，比较时只比较com子目录
        '''
        if self.jdConf['javadoc.oldversion'] is None or self.jdConf['javadoc.oldversion'] == '':
            self.log.info(u'没有历史版本'.encode('gbk'))
            return
        lf = os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.oldversion'])
        rf = os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version'])
        delfiles,addfiles,changefiles = self.__ifdircmp(os.path.join(lf,'com'),os.path.join(rf,'com'))
        spl = os.sep+'com'+os.sep
        fw=open(os.path.join(rf,"changeList.txt"),"w+")
        try:
            if len(delfiles) > 0:
                fw.write("deleted Classes:\n")
                for f in delfiles:
                    try:
                        fw.write('com.'+f.split(spl)[1].replace(os.sep,'.').replace('.html',''))
                        fw.write('\n')
                    except Exception as e:
                        self.log.exception("deleted Classes failed")
                        continue
            if len(addfiles) > 0:
                fw.write("added Classes:\n")
                for f in addfiles:
                    try:
                        fw.write('com.'+f.split(spl)[1].replace(os.sep,'.').replace('.html',''))
                        fw.write('\n')
                    except Exception as e:
                        self.log.exception("added Classes failed")
                        continue
            if len(changefiles) > 0:
                fw.write("changed Classes:\n")
                for f in changefiles:
                    try:
                        fw.write('com.'+f.split(spl)[1].replace(os.sep,'.').replace('.html',''))
                        fw.write('\n')
                    except Exception as e:
                        self.log.exception("changed Classes failed")
                        continue
            if len(delfiles) > 0 or len(addfiles) > 0 or len(changefiles) > 0:
                self.log.info(u'changeList生成完成'.encode('gbk'))
            else:
                self.log.info(u'没有接口变更'.encode('gbk'))
        finally:
            if fw is not None:
                fw.close()
        
    def jarApi(self):
        jarApicmd = []
        jarApicmd.append('jar')
        jarApicmd.append('cf')
        jarApicmd.append(os.path.join(self.srcPath,'src','main','java','apisrc.jar'))
        jarApicmd.append(self.jdConf['javadoc.package'].replace('.',os.sep))
        self.log.debug(jarApicmd)
        try:
            os.chdir(os.path.join(self.srcPath,'src','main','java'))
            stdout_val, stderr_val = external_cmd(' '.join(jarApicmd))
            if stderr_val is None or stderr_val == '':
                self.log.debug(stdout_val)
                shutil.move(os.path.join(self.srcPath,'src','main','java','apisrc.jar'),\
                                os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version'],'apisrc.jar'))
                self.log.info(u'jarapi生成完成'.encode('gbk'))
                return True
            else:
                self.log.error(u'jarapi生成失败：'.encode('gbk')+stderr_val)
                return False
        except Exception as er:
            self.log.exception("jarApi failed")
            return False
    def genverConf(self):
        cf = ConfigParser.ConfigParser()
        cf.add_section('version')
        cf.set('version','project',self.jdConf['javadoc.schema'])
        cf.set('version','version',self.jdConf['javadoc.version'])
        cf.set('version','date',time.strftime('%Y-%m-%d',time.localtime(time.time())))
        cf.write(open(os.path.join(self.srcPath,'version.conf'), "w"))
        shutil.move(os.path.join(self.srcPath,'version.conf'),os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version'],'version.conf'))

    def uploadFolder(self):
        '''
        
        '''
        remotehost = self.jdConf['ftp.host']
        remoteport = self.jdConf['ftp.port']
        loginname = self.jdConf['ftp.user']
        loginpassword = self.jdConf['ftp.pwd']
        remotepath = self.jdConf['ftp.remotepath']
        localpath = os.path.join(self.srcPath,self.jdConf['javadoc.output'],self.jdConf['javadoc.version'])
        schema = self.jdConf['javadoc.schema']
        version = self.jdConf['javadoc.version']
        ftp = FTP()
        try:
            ftp.connect(remotehost,remoteport,600)
        except:
            return (0,'conncet failed')
        else:  
            try:  
                ftp.login(loginname,loginpassword)
                ftp.cwd(remotepath)
                dirs=[]
                ftp.retrlines('MLSD',dirs.append)
                def f(d):
                    if 'type=dir' in d:
                        return True
                if schema is not None:
                    if schema not in map(lambda y:y[-1].strip(),filter(f ,map(lambda x: x.split(';'),dirs))):
                        ftp.mkd(schema)
                    ftp.cwd(schema)
                if version is not None:
                    dirs=[]
                    ftp.retrlines('MLSD',dirs.append)
                    if version in map(lambda y:y[-1].strip(),filter(f ,map(lambda x: x.split(';'),dirs))):
                        #已存在就先删除
                        self.__rmdFolder(ftp,remotepath+'/'+schema+'/'+version)
                        self.log.debug(u'远端文件删除完成'.encode('gbk'))
                    ftp.mkd(version)
                    ftp.cwd(version)
            except Exception as Er:
                self.log.exception("uploadFolder failed")
                return (0,'login failed')
        for root,folders,files in os.walk(localpath):
            os.chdir(root)
            relativePath = root.replace(localpath, '').split(os.sep)
            for p in relativePath:
                if p != '':
                    ftp.cwd(p)
            for file in files:
                ftp.storbinary('STOR ' + file, open(file, 'rb'))
            for folder in folders:
                ftp.mkd(folder)
            #back to root path
            ftp.cwd(remotepath)
            if schema is not None:
                ftp.cwd(schema)
            if version is not None:
                ftp.cwd(version)
        self.log.info(u'文档上传成功'.encode('gbk'))
        ftp.close()
        return (1,'success')
        
    def __rmdFolder(self,ftp,remotePath):
        ftp.cwd(remotePath)
        items=[]
        ftp.retrlines('MLSD',items.append)
        for item in items:
            if 'type=file' in item:
                ftp.delete((item.split(';')[-1]).strip())
            elif 'type=dir' in item:
                rp= remotePath+'/'+(item.split(';')[-1]).strip()
                self.__rmdFolder(ftp,rp)
        ftp.cwd('..')
        ftp.rmd(remotePath.split('/')[-1])

    def __listAllFiles(self,*path):
        '''
        列出path及其子目录下所有文件
        '''
        fs=[]
        if path is None or len(path) == 0:
            return fs
        for p in path:
            for root, dirs, files in os.walk(p):
                if len(files) > 0:
                    fs.extend(map(lambda a:os.path.join(root,a),files))
        return fs

    def __ifdircmp(self, lf, rf):
        '''
        目录lf和rf和他们的子目录下的所有差异文件列表
        左边为老版本目录，右边为新版本目录
        1、左边存在，右边不存在的文件，删除的文件
        2、左边不存在，右边存在的文件，新增的文件
        3、两边都存在，变更的文件
        '''
        def joinlf(a): return os.path.join(lf , a)
        def joinrf(a): return os.path.join(rf , a)
        delfiles,addfiles,changefiles=[],[],[]
        x = dircmp(lf, rf)
        #deleted files
        delfiles.extend(filter(os.path.isfile,map(joinlf, x.left_only)))
        delfiles.extend(self.__listAllFiles(*filter(os.path.isdir,map(joinlf, x.left_only))))
        #added files
        addfiles.extend(filter(os.path.isfile,map(joinrf, x.right_only)))
        addfiles.extend(self.__listAllFiles(*filter(os.path.isdir,map(joinrf, x.right_only))))
        #changed files
        sf,df,ef = cmpfiles(lf,rf,x.common_files)
        changefiles.extend(map(joinrf, df))
        if len(x.common_dirs) > 0:
            for cd in x.common_dirs:
                d,a,c = self.__ifdircmp(os.path.join(lf,cd),os.path.join(rf,cd))
                delfiles.extend(d)
                addfiles.extend(a)
                changefiles.extend(c)
        return delfiles,addfiles,changefiles