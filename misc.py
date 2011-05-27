#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        misc.py
#created:        2011-05-20 17:13

import time
import re

def writelog(log):
    logfile='/var/log/duanzi.log'
    f=open(logfile, 'a')
    f.write(timestr()+log+"\n")
    f.close()


def chinese(text):
    text=eval("""u'''%s'''""" % text)
    text=unescape(text)
#    text=UnShortenAll(text)
    return text

def timestr():
    return time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())

def unescape(s):

    if not s:
        return ''

    s=s.encode('utf8')
    s=s.replace("&lt;","<")
    s=s.replace("&gt;",">")
    s=s.replace("&quot;",'"')
    s=s.replace("&apos;","'")
    s=s.replace("&amp;","&")
    s=s.replace("\\","")

    return s


from os.path import dirname as dirname
from os.path import join as pathjoin

def getPath(sufix=""):
    '''get absolute path of the current dir'''
    path = dirname(__file__)
    try:
        index=path.index("..")
        if index!=-1:
            path=path[:index]
    except:
        pass
    return pathjoin(path, sufix).replace('\\','/')

