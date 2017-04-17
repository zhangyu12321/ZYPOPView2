# -*- coding: utf-8 -*-

import commands
import sys
import os
import shutil
from biplist import *
import traceback
import packing
    
# ===============  main函数  ===============
def main(argvs):
    
    # 0.获取外部参数
    versions = []
    domainnames = []
    if len(argvs) > 1 :
        tmp = ''
        # 将相应参数存至对应列表
        for i in range(len(argvs) - 1):
            arg = argvs[i+1]
            if arg == '-v':
                tmp = '-v'
            elif arg == '-d':
                tmp = '-d'
            if tmp == '-v' and arg != '-v':
                versions.append(arg)
            elif tmp == '-d' and arg != '-d':
                domainnames.append(arg)
    else:
        print '请输入参数:-v xxx xxx -d xxx'
        return
    if len(versions) == 0:
        print '请输入版本号(至少一个)'
        return
    elif len(domainnames) == 0:
        print '请输入域名简写(可多选): m3, m-beta, m-beta-b'
        return
    
    print 'versions : ' + ' '.join(versions)
    print 'domainnames : ' + ' '.join(domainnames)
    
    # 1.获取代理商参数
    print '获取代理商参数'
    try:
        # cwd = os.getcwd()
        cwd = os.path.abspath(__file__).split('/test-agents.py')[0]
        pathPlist = readPlist(os.path.join(cwd, 'Path.plist'))
        proPath = pathPlist['3.1']['path']
        proId = pathPlist['3.1']['id']
        infoPlist = readPlist(os.path.join(cwd, 'Info.plist'))
        agentsDic = infoPlist[proId]
    except:
        print '2.获取代理商参数失败'
        return
    for version in versions:
        for domainname in domainnames:
            # 2.修改 plist
            for key in agentsDic.keys():
                print '\n' + key + ' :'
                print '1.修改 plist'
                try:
                    # 2.1修改自定义 plist
                    agentsplistPath = findfile(proPath, 'Agents.plist')
                    if agentsplistPath == '':
                        print 'Agents.plist Was Not Found'
                        return
                    agentsPlist = readPlist(agentsplistPath)
                    # 2.1.1修改升级参数
                    agentsPlist['kPlatform'] = agentsDic[key]['kPlatform']
                    # 2.1.2修改分享相关
                    agentsPlist['Share'] = agentsDic[key]['Share']
                    # 2.1.3修改域名简写
                    agentsPlist['DomainNameId'] = domainname
                    # 2.1.4保存修改
                    writePlist(agentsPlist, agentsplistPath, False)
                    # 2.2修改系统 plist
                    yqmsplistPath = findfile(proPath, 'YQMS-Info.plist')
                    if yqmsplistPath == '':
                        print 'YQMS-Info.plist Was Not Found'
                        return
                    yqmsplist = readPlist(yqmsplistPath)
                    # 2.2.1修改应用名
                    yqmsplist['CFBundleDisplayName'] = agentsDic[key]['appName']
                    # 2.2.2修改分享相关
                    for item in yqmsplist['CFBundleURLTypes']:
                        if not 'CFBundleURLName' in item.keys():
                            continue
                        if item['CFBundleURLName'] == 'weixin':
                            item['CFBundleURLSchemes'][0] = agentsDic[key]['Share']['WeChat']['appKey']
                        elif item['CFBundleURLName'] == 'QQ':
                            item['CFBundleURLSchemes'][0] = 'QQ'+hex(int(agentsDic[key]['Share']['QQ']['appKey']))[2:]
                    # 2.2.3修改版本号
                    yqmsplist['CFBundleShortVersionString'] = version
                    yqmsplist['CFBundleVersion'] = version
                    # 2.2.4保存修改
                    writePlist(yqmsplist, yqmsplistPath, False)
                except:
                    print '2.修改 plist 失败'
                    return
                
                # 3.替换图片
                print '2.替换图片'
                # 3.1获取资源列表
                try:
                    imageDir = os.path.join(cwd, 'AgentsImages')
                    # imagePaths = []
                    imageNames = []
                    agentImageDir = os.path.join(imageDir, key)
                    for file in os.listdir(agentImageDir):
                        if file[0] == '.':
                            continue
                        # imagePaths.append(os.path.join(agentImageDir, file))
                        imageNames.append(file)
                except:
                    print 'Get ImagePaths Error'
                    return
                # 3.2替换项目中名字相同(可能含有-1, -2)的资源文件
                try:
                    imageDir = os.path.join(proPath, 'yqms2.1beta01/Images.xcassets')
                    for root, dirs, files in os.walk(imageDir):
                        for file in files:
                            file = file.decode('utf8')
                            for imageName in imageNames:
                                if file == imageName:
                                    # 名字相同的
                                    fromPath = os.path.join(agentImageDir, imageName)
                                    toPath = os.path.join(root, file)
                                    if replace(fromPath, toPath):
                                        print 'Replace File Error 1'
                                        return
                                elif file.split(''.join([imageName.split('.')[0], '-']))[0] == '':
                                    # 名字以资源文件名加-为开头的
                                    fromPath = os.path.join(agentImageDir, imageName)
                                    toPath = os.path.join(root, file)
                                    if replace(fromPath, toPath):
                                        print fromPath
                                        print toPath
                                        print 'Replace File Error 2'
                                        return
                except Exception as e:
                    print repr(imageName)
                    print repr(file)
                    print 'Replace File Error 0'
                    print traceback.format_exc()
                    return
                
                # 4.打包
                packingPath = os.path.join(cwd, 'packing.py')
                exportProvisioningProfile = 'com.20150612Distribution'
                exportPath = os.path.join(cwd, 'build')
                exportName = '%s_v%s_%s'%(key.encode('utf8'), version, domainname)
                print '3.开始打包%s(大约需要3-5分钟)'%exportName
                cmdList = ['python', packingPath, proPath, 'YQMS', 'Release', 'YQMS', 'ipa', exportProvisioningProfile, exportPath, exportName]
                status, output = commands.getstatusoutput(' '.join(cmdList))
                if status:
                    print '4.打包%s失败'%exportName
                    print output
                else:
                    print '4.打包%s成功'%exportName


# ===============  其他函数  ===============
def findfile(path, filename, getStr = True):
    fileList = []
    for root, dirs, files in os.walk(path):
            for file in files:
                if file == filename:
                    filePath = os.path.join(root, file)
                    if getStr:
                        return filePath
                    else:
                        fileList.append(filePath)
    return fileList

def replace(fromPath, toPath):
    # 初始路径不存在
    if not os.path.exists(fromPath):
        return 111
    # 初始路径是个文件夹
    elif os.path.isdir(fromPath):
        # 目标路径存在, 删除
        if os.path.exists(toPath):
            if os.path.isdir(toPath):
                shutil.rmtree(toPath)
            else:
                os.remove(toPath)
        # 复制到目标路径
        shutil.copytree(fromPath, toPath)
        return 0
    # 初始路径是个文件
    else:
        # 目标路径存在, 删除
        if os.path.exists(toPath):
            if os.path.isdir(toPath):
                shutil.rmtree(toPath)
            else:
                os.remove(toPath)
        # 复制到目标路径
        shutil.copy(fromPath, toPath)
        return 0



if __name__ == '__main__':
    main(sys.argv)
    '''do something'''
