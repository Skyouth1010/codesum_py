#-*- coding: utf-8 -*-
'''
java工程代码统计
@author: skyouth
'''
import os

codecounts = {'source':[0,0,0],'config':[0,0,0],'other':[0,0,0], 'jar':[0,0,0]}
sourceSuffix = ['java','jsp','css','js']
configSuffix = ['xml','properties']
blacklist = ['docx','doc','xls','xlsx','txt', 'swf']

def count(path):
    for f in os.listdir(path):
        if f == '.settings' or f == '.svn' or (path.endswith('web') and f == 'emoticons'):
            continue
        elif os.path.isdir(path + '/' + f):
            count(path + '/' + f)
        else:
            # get suffix
            splits = f.strip().rsplit('.',1)
            # 不带后缀，归类其他
            s = countJavaF(path + '/' + f)
            if len(splits) == 1:
                filecount = codecounts['other'][0] + s[0]
                countJava = codecounts['other'][1] + s[1]
                countComment = codecounts['other'][2] + s[2]
                codecounts['other'] = [filecount, countJava, countComment]
                continue
            if splits[1] == 'class':continue
            if splits[1] in sourceSuffix:
                filecount = codecounts['source'][0] + s[0]
                countJava = codecounts['source'][1] + s[1]
                countComment = codecounts['source'][2] + s[2]
                codecounts['source'] = [filecount, countJava, countComment]
            elif splits[1] in configSuffix:
                filecount = codecounts['config'][0] + s[0]
                countJava = codecounts['config'][1] + s[1]
                countComment = codecounts['config'][2] + s[2]
                codecounts['config'] = [filecount, countJava, countComment]
            elif splits[1] == 'jar':
                filecount = codecounts['jar'][0] + s[0]
                countJava = codecounts['jar'][1] + s[1]
                countComment = codecounts['jar'][2] + s[2]
                codecounts['jar'] = [filecount, countJava, countComment]
            elif splits[1] in blacklist: continue
            else:
                filecount = codecounts['other'][0] + s[0]
                countJava = codecounts['other'][1] + s[1]
                countComment = codecounts['other'][2] + s[2]
                codecounts['other'] = [filecount, countJava, countComment]

def countJavaF(path):
    countComment = 0
    countJava = 0
    try:
        fj = open(path)
        for line in fj:
            validLine = line.strip()
            if len(validLine) == 0:
                continue
            elif validLine.startswith('//') or validLine in ['/**','*','*/'] or validLine.startswith('*'):
                countComment = countComment+1
            else:
                countJava = countJava + 1
    except Exception as e:
        print path + ' open error' + str(e)
    finally:
        if fj: fj.close()
    
    return [1, countJava, countComment]

if __name__ == '__main__':
    for f in os.listdir("D:/workspace_zh/teatalk"):
        codecounts = {'source':[0,0,0],'config':[0,0,0],'other':[0,0,0], 'jar':[0,0,0]}
        if f.startswith('.'):
            continue
        count("D:/workspace_zh/teatalk/" + f)
        print (f + "\t"),
        print str(codecounts['source'][0]) + "\t" + str(codecounts['source'][1]) + "\t" + str(codecounts['source'][2]) + "\t",
        print str(codecounts['config'][0]) + "\t" + str(codecounts['config'][1]) + "\t",
        print str(codecounts['other'][0]) + "\t" + str(codecounts['other'][1]) + "\t" + str(codecounts['other'][2]) + "\t",
        print str(codecounts['jar'][0]) + "\t"
