#!/usr/bin/env python                                                                                  
# coding=utf-8

from numpy import *  

class PrintUtil(object):

  '''''init setflag
  '''
  def __init__(self):
    self.Bflag_print = False
      
  def setPrintEnable(self):
    self.Bflag_print = True

  def resetPrintEnable(self):
    self.Bflag_print = False

  def prt(self, content):
    if self.Bflag_print:
      if isinstance(content, str):
        print content
        
  def traceback(self):
    import traceback
    print traceback.print_exc()
    
if __name__ == '__main__':
  pass

