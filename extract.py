#!/usr/bin/evn python 
#coding:utf-8
#author: John Chan
#Email: chenyj@bcc.ac.cn
import os
import gzip
import shutil
'''
This tool is to download and extract the PubChem Database.
Identifing invalid .gz file, delete it and download the new one.
Check if all files are consecutive. If not download the missing one.
'''
consecutiveId=0
maximumDisconnectedAllowed = 3


def checkIfDecompressed(filePath):
    global maximumDisconnectedAllowed
    if os.path.exists(filePath):
        print filePath + ' exists: skip'
        if os.path.exists(filePath+'.gz'):
            os.remove(filePath+'.gz')
            print filePath+'.gz: removed'
        return
    elif os.path.exists(filePath+'.gz'):
        decompress(filePath)
        return
    else:
        print 'gz source file need to be download'
        ftpPubChem(filePath)
        return

def ftpPubChem(filePath):
    global maximumDisconnectedAllowed
    try:
        command='nohup wget -m -np ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/XML/'+filePath+'.gz &'
        os.system(command)
        print filePath+'.gz: downloaded'
    except:
        print filePath+'.gz: download fail'
        maximumDisconnectedAllowed = maximumDisconnectedAllowed - 1
        if maximumDisconnectedAllowed > 0:
            ftpPubChem(filePath)
        else:
            print filePath+'.gz: downloadFail'
        
    finally:
        maximumDisconnectedAllowed = 3
        return

def decompress(filePath):
    global maximumDisconnectedAllowed
    with open(filePath, 'wb') as xmlFile:
        with gzip.open(filePath+'.gz', 'rb') as gzFile:
            try:
                shutil.copyfileobj(gzFile, xmlFile)
                print filePath+'.gz: decompressed'
                os.remove(filePath+'.gz')
                print filePath+'.gz: removed'
            except Exception,e:
                # Differ from Linux gunzip command, xmlFile will have been created and incomplete bytes will have been copied
                # even through
                # some origin gzFile's details of gzFile missed
                # So, remove xmlFile -> try downloading new compressed GZfile -> remove incomplete GZfile 
                os.remove(filePath)
                print filePath+'.gz: '+e.message
                ftpPubChem(filePath)
    
def main():
    global consecutiveId
    while consecutiveId <= 129300000:
        filePath = '/datapool/biodata/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/Compound_'+str(consecutiveId+1).zfill(9)+'_'+str(consecutiveId+25000).zfill(9)+'.xml'
        print filePath
        checkIfDecompressed(filePath)
        consecutiveId = consecutiveId + 25000
if __name__ == '__main__':
    main()
