# coding:utf-8
# -*- coding: utf-8 -*-
import base64
#from config import QQWRY_PATH, CHINA_AREA
#from util.IPAddress import IPAddresss
import re
#from util.compatibility import text_
import htmlsample
import sys
from bs4 import BeautifulSoup
reload(sys)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'qiye'
from lxml import etree

class Html_Parser(object):
    def __init__(self):
        #self.ips = IPAddresss(QQWRY_PATH)
        self.html = htmlsample.html
        pass

    def parse(self, response, parser):
        '''
        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        print parser
        if parser['type'] == 'xpath':
            return self.XpathPraser(response, parser)
        elif parser['type'] == 'regular':
            return self.RegularPraser(response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(response, parser)
        else:
            return None

    def AuthCountry(self, addr):
        '''
        用来判断地址是哪个国家的
        :param addr:
        :return:
        '''
        for area in CHINA_AREA:
            if text_(area) in addr:
                return True
        return False

    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                type = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr
            except Exception as e:
                continue
            # updatetime = datetime.datetime.now()
            # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

            # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
            proxy = {'ip': ip, 'port': int(port), 'types': int(type), 'protocol': int(protocol), 'country': country,
                     'area': area, 'speed': 100}
            proxylist.append(proxy)
        return proxylist

    def RegularPraser(self, response, parser):
        '''
        针对正则表达式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # 网站的类型一直不靠谱所以还是默认，之后会检测
                    type = 0
                    # if parser['postion']['protocol'] > 0:
                    # protocol = match[parser['postion']['protocol']]
                    # if protocol.lower().find('https')!=-1:
                    #         protocol = 1
                    #     else:
                    #         protocol = 0
                    # else:
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    # print(ip,port)
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue

                proxy = {'ip': ip, 'port': port, 'types': type, 'protocol': protocol, 'country': country, 'area': area,
                         'speed': 100}

                proxylist.append(proxy)
            return proxylist


    def CnproxyPraser(self, response, parser):
        proxylist = self.RegularPraser(response, parser)
        chardict = {'v': '3', 'm': '4', 'a': '2', 'l': '9', 'q': '0', 'b': '5', 'i': '7', 'w': '6', 'r': '8', 'c': '1'}

        for proxy in proxylist:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i] != '+':
                    new_port += chardict[port[i]]
            new_port = int(new_port)
            proxy['port'] = new_port
        return proxylist


    def proxy_listPraser(self, response, parser):
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs:
            for match in matchs:
                try:
                    ip_port = base64.b64decode(match.replace("Proxy('", "").replace("')", ""))
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    type = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    # print(ip,port)
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue
                proxy = {'ip': ip, 'port': int(port), 'types': type, 'protocol': protocol, 'country': country,
                         'area': area, 'speed': 100}
                proxylist.append(proxy)
            return proxylist
            
    def research(self, ith):
        if type(ith) is "<class 'bs4.element.Tag'>":
            ith = ith.get_text()
        if ith is "str" or ith is "buffer":
              import re
              ith = self.x2utf(ith)
              matchObj = re.search(r'>.*?</a', ith, re.M|re.I )
              if matchObj:
                  ith =  matchObj.group().split('>')[-1].split('</a')[-2]
              else:
                matchObj = re.search(r'>.*?</span', ith, re.M|re.I )
                if matchObj:
                  ith = matchObj.group().split('>')[-1].split('</span')[-2]
                else:
                  matchObj = re.search(r'>.*?</div', ith, re.M|re.I )
                  if matchObj:
                    ith = matchObj.group().split('>')[-1].split('</div')[-2]
                  else:
                    pass
                    ith = ""
                    #print "no match"
              return ith
        return ith

    def bs4html(self, r):
      r = r.decode('utf8');
      soup = BeautifulSoup(r, "html.parser");
      pzbox = soup.find("div", {"class":"pzbox"});
      conbox = pzbox.find("div", {"class":"conbox"});
      try:

        trs = conbox.findAll("tr");
        ths = conbox.findAll("th");
        tds = conbox.findAll("td");

        '''''
        for th in ths:
          print th
        '''
        # get the length of tds and  hs 
        #num = int(round(len(tds)/len(ths)))
        addicons = soup.findAll("div", {"class":"btn_delbar"});
        num = len(addicons)
        dl = soup.find("dl", {"class":"cont-dl"});
        ddlist = dl.findAll("dd")
        dddict = {}
        for dd in ddlist:
            print dd.find('data-key')
            print dd.get_text()
        outths = []
        for tr in trs:
          print '===new tr====='
          #print tr
          triths = tr.findAll('th')
          itds = tr.findAll('td')
          #for itd in itds:
          #    print itd
          thstr = ""
          for ith in triths:
                    #print str(ith)
              thstr = thstr + self.research(ith.get_text())
          #nprint thstr
#          print "======"
          import chardet
          outths.append("###".encode('utf-8'))      
          outths.append(thstr.encode('utf-8'))      
          print thstr
          for itd in itds:
              td_content = ""
              spans = itd.findAll('span')
              for span in spans:
                  classname = span.find(attrs={'class'})
                  if classname is not None:
                      print classname
                      td_content+=classname
              td_content+=itd.get_text() 
              outths.append(td_content)
              #print td_content
          print '--------------'


        #print len(tds), len(ths), len(tds)/len(ths), num
        fn = "qq.xls"
        self.wr2xls(outths,fn,num)
        '''''
        f = open('qq.csv','w+')
        ii = 0
        lines = ""
        for iout in outths:
            lines = iout + lines
            ii+=1
            if ii == num+2:
                ii = 0
                f.write(lines+"\n")
                lines == ""
                f.write("======")
         '''

      except:
        import traceback
        traceback.print_exc()
        pass
 
    def x2utf(self, inp):
        mtype = type(inp)
        #print inp,'type=', mtype
        if isinstance(inp, str):
            import chardet
            code = chardet.detect(inp)
            encode = code['encoding']
            if encode is not 'utf-8' and isinstance(encode, str):
                #print encode,code
                dec = inp.decode(encode)
                #enc = dec.encode('utf-8')
               # print 'enc', enc
                return dec
            print type(inp)
            ret = "参数 %s" % inp
            print ret
            print type(ret)
            _type = chardet.detect(ret)
            ret =self.x2utf(ret)
            return ret
        elif isinstance(inp, unicode):
            #enc = inp.encode('utf-8')
            #print 'unicode', enc
            return inp#'enc', enc
        else:
            print type(inp)
            print 'else', inp
            ret = ("参数",inp).encode('utf-8')
            print ret
            print type(ret)
            _type = chardet.detect(ret)
            return inp.decode(_type) 

    def x2uni(self, inp):
        mtype = type(inp)
        #print inp,'type=', mtype
        if isinstance(inp, str):
            import chardet
            code = chardet.detect(inp)
            encode = code['encoding']
            return inp.decode(encode) 
        return inp

    def wr2xls(self, ths, filename, num):
      cell = "cell"  
      import xlwt;
      import xlrd;
      from xlutils.copy import copy;
      fn = filename
      styleBoldRed = xlwt.easyxf('font: color-index red, bold on');


      headerStyle = styleBoldRed;
      wb = xlwt.Workbook(encoding = 'utf-8');
      import chardet
      #print chardet.detect(fn)

      #style = xlwt.XFStyle()
      #font = xlwt.Font()
      #font.name = 'SimSun' # 指定“宋体”
      #style.font = font


      ws = wb.add_sheet(fn, cell_overwrite_ok=True);#gConst['xls']['sheetName']);
      i = 0
      j = 0
      for th in ths:
          #txt= th.get_text()
          txt= th
          #print txt
          #@print txt
          tx = self.x2utf(txt)
          if th == "###":
            j+=1
            i=0
          #ws.write(i, j, tx);
          ws.write(j,i, tx, headerStyle);
          i+=1
#          print i,j,tx,th
          #print cur
      wb.save(fn);#gConst['xls']['fileName']);
      oldWb = xlrd.open_workbook(fn)#gConst['xls']['fileName'], formatting_info=True);
      print oldWb; #<xlrd.book.Book object at 0x000000000315C940>
      newWb = copy(oldWb);
      print newWb; #<xlwt.Workbook.Workbook object at 0x000000000315F470>
      newWs = newWb.get_sheet(0);
      i = 0  
      j = 0  
      for th in ths:
          #print td.string, " #" 
          if th == "###":
              i = 0
              j += 1
              #print "\n=========="
          tx = self.x2utf(th)
          newWs.write(j,i, tx, headerStyle);
#          print i,j,tx
          #print chardet.detect(td.string)
          #print row,col,td.string
          i+=1
      print "write new values ok";
      newWb.save(fn)#gConst['xls']['fileName']);
      print "save with same name ok";

if __name__=="__main__":
  print "main"
  import json
  #_Html_Parser = Html_Parser();
  import os
  import os.path
  import chardet
  rootdir = './'
  for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
      if filename.split('.')[-1]=='txt':
        f = open(filename)
        for line in f.readlines():
          print type(line)
          print chardet.detect(line)
          todict = json.loads(line.decode('GB2312'))
          for key in todict['result']['paramtypeitems']:
            for item in key['paramitems']:
              print item['name']
              #打印出所有的功能单项
              #为求解多元线性回归做准备
          import time
          time.sleep(10000)

#    _Html_Parser.bs4html(_Html_Parser.html)



