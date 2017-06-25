#!/usr/bin/env python
# coding=utf-8

#carhome-spider.py

import re
import sys
import time 
import traceback
import codecs
import json
import chardet

reload(sys)
sys.setdefaultencoding("utf-8")

items_list=[]

def readfile_2_list():
    g=codecs.open('./output.txt','w','utf8')
    f=codecs.open('./58data.txt','r','utf8')
    lines=f.readlines()
    for line in lines:
        line=line.encode('utf8')
        house_item=[]
        outstr=""
        words=line.split(',')
        house_item.append(str(words[0]))
        house_item.append(str(words[-1]))
        for word in words:
            word=str(word).encode('utf8')
            if '(\d+)m' in word:
                house_item.append(word)
            if '地铁站' in word:
                house_item.append(word)
            if '\d室' in word:
                house_item.append(word)
        line=re.sub(",","",line)
        house_item.append(line.encode('utf8'))
        outstr=",".join(house_item)
        outstr=re.sub("\r\n","",outstr)
        print(outstr.encode('utf8'))
        g.write(outstr.encode('utf8'))
        g.write("\r\n")

readfile_2_list()      

                imgUrl = getImgUrl(imgcontent)

                                if imgUrl:
                                                       fileurl.write(str(imgUrl[0].decode("gb2312").encode("utf-8")) + '\n')#
                                                                          urlShow = str(imgUrl[0].decode("gb2312").encode("utf-8"))
                                                                                             print imgUrl[0].decode("utf-8").encode(sys.getfilesystemencoding())

                                                                                                                filename = os.path.basename(urlShow) #I路,^G件M


                                                                                                                                   if os._exists(seriesPath + '\\'+filename):
                                                                                                                                                              print 'exist \n'
                                                                                                                                                                                 else:
                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                          urllib.urlretrieve(urlShow, seriesPath + '\\'+filename)
                                                                                                                                                                                                                                                                 except (urllib.ContentTooShortError, IOError), e:
                                                                                                                                                                                                                                                                                              # logger.log("Error downloading NZB: " + str(sys.exc_info()) + " - " + ex(e), logg
                                                                                                                                                                                                                                                                                              er.ERROR)
                                                                                                                                                                                                                                                                                                                        if os.path.exists(seriesPath + '\\'+filename):
                                                                                                                                                                                                                                                                                                                                                         os.remove(seriesPath + '\\'+filename)
                                                                                                                                                                                                                                                                                                                                                                                      time.sleep(1)
                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                                                             time.sleep(0.1)
                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                                             '))
