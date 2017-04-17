import sys
import os
import commands
import shutil

def rmworking():
    if os.path.exists('working'):
        os.remove('working')

def packing(argvs):
    # 获取参数
    try:
        projectPath = argvs[1]
        projectName = argvs[2]
        configuration = argvs[3]
        scheme = argvs[4]
        exportFormat = argvs[5]
        exportProvisioningProfile = argvs[6]
        exportPath = argvs[7]
        exportName = argvs[8]
    except:
        return 1 << 14, ''
    # 读取本地文件,判断是否在执行打包
    if os.path.exists('working'):
        return 1 << 15, ''
    # 打包脚本未执行,创建文件,执行打包
    else:
        working = open('working', 'w')
        working.close()
    try:
        if not os.path.exists(projectPath):
            rmworking()
            print '项目路径不存在'
            return 1 << 16, ''
        if not os.path.exists(exportPath):
            # 如果目标目录不存在则创建该目录
            os.makedirs(exprotPath)
        # clean
        project = os.path.join(projectPath, projectName + '.xcodeproj')
        if not os.path.exists(project):
            rmworking()
            print '.xcodeproj 文件不存在'
            
            return 1 << 17, ''
        print 'CLEANING'
        statusC, outputC = commands.getstatusoutput('xcodebuild clean -project ' + project + ' -configuration ' + configuration + ' -alltargets')
        if statusC:
            rmworking()
            print outputC
            print 'CLEAN ERROR'
            return 1 << 18, ''
        print 'CLEAN SUCCEED'
        # archive
        print 'ARCHIVING, IT WILL TAKE 3 TO 5 MINUTES'
        archivePath = os.path.join(projectPath, projectName + '.xcarchive')
        statusA, outputA = commands.getstatusoutput('xcodebuild archive -project ' + project + ' -scheme ' + scheme + ' -archivePath ' + archivePath)
        if statusA:
            rmworking()
            print outputA
            print 'ARCHIVE ERROR'
            return 1 << 19, ''
        print 'ARCHIVE SUCCEED'
        # exportArchive
        print 'EXPORTARCHIVING'
        ipaName = projectName + '.' + exportFormat
        if os.path.exists(os.path.join(exportPath, exportName)):
            os.remove(os.path.join(exportPath, exportName))
        statusE, outputE = commands.getstatusoutput('xcodebuild -exportArchive -archivePath ' + archivePath + ' -exportPath ' + os.path.join(exportPath, exportName) + ' -exportFormat ' + exportFormat + ' -exportProvisioningProfile ' + exportProvisioningProfile)
        shutil.rmtree(archivePath)
        if statusE:
            rmworking()
            print outputE
            print 'EXPORTARCHIVE ERROR'
            return 1 << 20, ''
        print 'EXPORTARCHIVE SUCCEED'
        rmworking()
        return 0, os.path.join(exportPath, ipaName)
    except:
        rmworking()
        return -1, ''

if __name__ == '__main__':
    # 参数列表:
    # projectPath projectName configuration scheme exportFormat exportProvisioningProfile exportPath exportName
    # 项目路径     项目名称      Release/Debug scheme 目标文件格式   描述文件                    导出路径    导出的文件名
    # 外部输入格式:
    # python packing.py (上述参数列表)
    print packing(sys.argv)
