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
sys.path.append('..')
import db.MongoHelper as MongoHelper
import util
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

    def store_data_to_mongo(self, itemdict):
      mongohelper=MongoHelper.MongoHelper("autohome", "config")
      mongohelper.select_colletion("config")
      mongohelper.insert(itemdict)

    def convertType(self, input, type):
      if isinstance(input, str):
        import chardet
        encodetype = chardet.detect(input)['encoding']
        #print encodetype
        if type == "unicode":
          return input.decode(encodetype)
        return input.decode(encodetype).encode(type)
      
    def counterAnti(self, line):
      import re
      line = re.sub("<span class='hs_kw8_configpl'></span>", u'导', line)
      line = re.sub("<span class='hs_kw9_configpl'></span>", u'价', line)
      line = re.sub("<span class='hs_kw10_configpl'></span>", u'10', line)
      line = re.sub("<span class='hs_kw11_configpl'></span>", u'万', line)
      line = re.sub("<span class='hs_kw7_configpl'></span>", u'指', line)
      line = re.sub("<span class='hs_kw0_configpl'></span>", u'0', line)
      line = re.sub("<span class='hs_kw1_configpl'></span>", u'车辆型号', line)
      line = re.sub("<span class='hs_kw2_configpl'></span>", u'东风', line)
      line = re.sub("<span class='hs_kw6_configpl'></span>", u'商', line)      
      line = re.sub("<span class='hs_kw12_configpl'></span>", u'微面', line)
      line = re.sub("<span class='hs_kw13_configpl'></span>", u'综合', line)
      line = re.sub("<span class='hs_kw14_configpl'></span>", u'油耗', line)
      line = re.sub("<span class='hs_kw15_configpl'></span>", u'质保', line)
      line = re.sub("<span class='hs_kw16_configpl'></span>", u'长度', line)
      line = re.sub("<span class='hs_kw17_configpl'></span>", u'宽度', line)
      line = re.sub("<span class='hs_kw18_configpl'></span>", u'高度', line)
      line = re.sub("<span class='hs_kw19_configpl'></span>", u'轴距', line)
      line = re.sub("<span class='hs_kw20_configpl'></span>", u'前', line)
      line = re.sub("<span class='hs_kw22_configpl'></span>", u'后轮距', line)
      line = re.sub("<span class='hs_kw23_configpl'></span>", u'离地间隙', line)
      line = re.sub("<span class='hs_kw24_configpl'></span>", u'整备', line)
      line = re.sub("<span class='hs_kw25_configpl'></span>", u'质量', line)
      line = re.sub("<span class='hs_kw26_configpl'></span>", u'车门数', line)
      line = re.sub("<span class='hs_kw27_configpl'></span>", u'后排', line)
      line = re.sub("<span class='hs_kw28_configpl'></span>", u'油箱', line)
      line = re.sub("<span class='hs_kw29_configpl'></span>", u'容积', line)
      line = re.sub("<span class='hs_kw30_configpl'></span>", u'最大', line)
      line = re.sub("<span class='hs_kw31_configpl'></span>", u'31', line)
      line = re.sub("<span class='hs_kw32_configpl'></span>", u'后驱', line)
      line = re.sub("<span class='hs_kw33_configpl'></span>", u'33', line)
      line = re.sub("<span class='hs_kw34_configpl'></span>", u'悬架', line)
      line = re.sub("<span class='hs_kw40_configpl'></span>", u'助力', line)
      line = re.sub("<span class='hs_kw50_configpl'></span>", u'排量', line)
      line = re.sub("<span class='hs_kw54_configpl'></span>", u'气缸', line)
      line = re.sub("<span class='hs_kw55_configpl'></span>", u'排列', line)
      line = re.sub("<span class='hs_kw56_configpl'></span>", u'气门', line)
      line = re.sub("<span class='hs_kw35_configpl'></span>", u'麦迪逊', line)
      line = re.sub("<span class='hs_kw36_configpl'></span>", u'独立', line)
      line = re.sub("<span class='hs_kw37_configpl'></span>", u'37', line)
      line = re.sub("<span class='hs_kw38_configpl'></span>", u'钢板', line)
      line = re.sub("<span class='hs_kw39_configpl'></span>", u'弹簧', line)
      line = re.sub("<span class='hs_kw41_configpl'></span>", u'承载式', line)
      line = re.sub("<span class='hs_kw42_configpl'></span>", u'42', line)
      line = re.sub("<span class='hs_kw43_configpl'></span>", u'盘式', line)
      line = re.sub("<span class='hs_kw44_configpl'></span>", u'后制动器', line)
      line = re.sub("<span class='hs_kw45_configpl'></span>", u'鼓式', line)
      line = re.sub("<span class='hs_kw46_configpl'></span>", u'46', line)
      line = re.sub("<span class='hs_kw47_configpl'></span>", u'规格', line)
      line = re.sub("<span class='hs_kw48_configpl'></span>", u'轮胎', line)
      line = re.sub("<span class='hs_kw49_configpl'></span>", u'号', line)
      line = re.sub("<span class='hs_kw51_configpl'></span>", u'进气', line)
      line = re.sub("<span class='hs_kw52_configpl'></span>", u'自然', line)
      line = re.sub("<span class='hs_kw53_configpl'></span>", u'吸气', line)
      line = re.sub("<span class='hs_kw57_configpl'></span>", u'压缩比', line)
      line = re.sub("<span class='hs_kw58_configpl'></span>", u'配气', line)
      line = re.sub("<span class='hs_kw59_configpl'></span>", u'机构', line)
      line = re.sub("<span class='hs_kw60_configpl'></span>", u'缸径', line)
      line = re.sub("<span class='hs_kw61_configpl'></span>", u'行程', line)
      line = re.sub("<span class='hs_kw62_configpl'></span>", u'功率', line)
      line = re.sub("<span class='hs_kw63_configpl'></span>", u'转速', line)
      line = re.sub("<span class='hs_kw64_configpl'></span>", u'扭矩', line)
      line = re.sub("<span class='hs_kw65_configpl'></span>", u'燃油', line)
      line = re.sub("<span class='hs_kw66_configpl'></span>", u'京', line)
      line = re.sub("<span class='hs_kw67_configpl'></span>", u'供油', line)
      line = re.sub("<span class='hs_kw68_configpl'></span>", u'多点', line)
      line = re.sub("<span class='hs_kw69_configpl'></span>", u'电喷', line)
      line = re.sub("<span class='hs_kw70_configpl'></span>", u'缸盖', line)
      line = re.sub("<span class='hs_kw71_configpl'></span>", u'缸体', line)
      line = re.sub("<span class='hs_kw72_configpl'></span>", u'环保', line)
      line = re.sub("<span class='hs_kw73_configpl'></span>", u'标准', line)
      line = re.sub("<span class='hs_kw74_configpl'></span>", u'国', line)
      line = re.sub("<span class='hs_kw75_configpl'></span>", u'电池', line)
      line = re.sub("<span class='hs_kw76_configpl'></span>", u'容量', line)
      line = re.sub("<span class='hs_kw77_configpl'></span>", u'充电', line)
      line = re.sub("<span class='hs_kw78_configpl'></span>", u'时间', line)
      line = re.sub("<span class='hs_kw79_configpl'></span>", u'79', line)
      return line
    
    def jsonDump(self, input):
      import json
      return json.dumps(input, ensure_ascii=False, encoding='utf-8')

if __name__=="__main__":
  print "main"
  import json
  _Html_Parser = Html_Parser();
  import os
  import os.path
  import chardet
  rootdir = '../output/'
  for parent,dirnames,filenames in os.walk(rootdir):
    for filename in filenames:
      print filename 
      if filename.split('.')[-1]=='txt':
        f = open(os.path.join(rootdir, filename))
        for line in f.readlines():
          #line = _Html_Parser.counterAnti(line)
          line = line
          
          #print type(line)
          typecode = chardet.detect(line)
          #print typecode
          #print line
          todict = json.loads(line.decode(typecode['encoding']).encode('utf-8'))
          #todict = json.loads(line)
          saveitem = {}
          for key in todict['result']['paramtypeitems']:
            dictitem = {}
            for paraitem in key['paramitems']:
              listitem = []
              for valitem in paraitem['valueitems']:
                  listitem.append(_Html_Parser.counterAnti(valitem['value']))
                  print _Html_Parser.counterAnti(paraitem['name'])
                  print _Html_Parser.counterAnti(valitem['value'])
              dictitem[_Html_Parser.counterAnti(paraitem['name'])] =  listitem
            fdjxh = -1
            for key in dictitem.keys():
              if fdjxh < len(dictitem[key]):
                fdjxh = len(dictitem[key])
            #print chardet.detect(fdjxh)
            leng = fdjxh
            for i in range (0, leng):
              for key in dictitem.keys():
                saveitem[key] = dictitem[key][i]
          _Html_Parser.store_data_to_mongo(saveitem)
#                  dictitem[paraitem['name']] = valitem['value']
#                  print dictitem
#                  dumpsitem = _Html_Parser.jsonDump(dictitem)
#                  print dumpsitem
#                  dumpsitem = _Html_Parser.counterAnti(dumpsitem)
#                  print dumpsitem

              #打印出所有的功能单项
              #为求解多元线性回归做准备

#    _Html_Parser.bs4html(_Html_Parser.html)


