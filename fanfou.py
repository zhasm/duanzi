#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        test.py
#created:        2010-12-18 22:42
import re
import pycurl
import json
import urllib
import StringIO
import time
#necessary to force chinese encoding(utf8)
import sys
from message import Msg

path="/home/zhasm/cron/duanzi"

idfile="%s/id.txt" % path
logfile="%s/log.txt" % path


'''force utf-8 encoding system'''
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def unicode2utf8(ustr):
    '''print raw of "\u996d\u51c9\u4e86\u5426" unicode'''
    return eval("""u'''%s'''""" % ustr)

api={
    'exists':'http://api.fanfou.com/friendships/exists.json',
    'friends':'http://api.fanfou.com/friends/ids.json',
    'followers':'http://api.fanfou.com/followers/ids.json',
    "reply": "http://api.fanfou.com/statuses/replies.json",
    "show": "http://api.fanfou.com/users/show.json",
    "test": "http://api.fanfou.com/help/test.json",
    "timeline": "http://api.fanfou.com/statuses/user_timeline.json",
    "update": "http://api.fanfou.com/statuses/update.json",
    "verify": "http://api.fanfou.com/account/verify_credentials.json",
}

class Fanfou:
    def __init__(self, id="", sn=""):
        self.id=id
        self.sn=sn
        self.output = StringIO.StringIO()
            #getvalue()
        self.init_curl()

    def __del__(self):
        try:
            self.curl.close()
            self.output.close()
        except:
            pass
    def init_curl(self):
        c=pycurl.Curl()
        userpwd=""
        if self.sn:
            userpwd= "%s:%s" % (self.id,self.sn)
            c.setopt(c.USERPWD,userpwd)

        c.setopt(c.URL, api['test'])
#        c.setopt(c.VERBOSE, 1)
        self.output.truncate(0)
        c.setopt(c.WRITEFUNCTION, self.output.write)
        c.perform()
        if not self.get()=='ok':
            print self.get()
            print "Error Init Fanfou CURL "
            exit()
        self.curl=c

    def get(self):
        value=self.output.getvalue()
        value=value.replace("false", "False")
        value=value.replace("true", "True")
        value=re.sub(r"(?<=\])[^\]]+$", '', value)
        return eval(value)

    def get_friends(self, api_type="friends"):
        c=self.curl
        url=api[api_type]
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get()

    def get_msg(self, msg_type, count=20, since_id="", max_id="", page=1, extra=""):
        c=self.curl
        data={
            "count":count,
            "since_id": since_id,
            "max_id": max_id,
            "page": page,
        }
        url=api[msg_type]+"?"+urllib.urlencode(data)+extra
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get()

    def show(self, id):
        c=self.curl
        data={
            "id":id,
        }
        url=api['show']+"?"+urllib.urlencode(data)
        c.setopt(c.URL, url)
        self.output.truncate(0)
        c.perform()
        return self.get()

    def update(self, data):

        url=api['update']
        c=self.curl
        c.setopt(pycurl.POST,True)
        data=urllib.urlencode(data)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.URL, url)
        self.output.truncate(0)
        c.perform()

    def reply(self, m):
        '''msg is a Msg object'''
        url=api['reply']
        data={
            'status':"%s --@%s" % (m['text'], m['name']),
            'in_reply_to_status_id':m['id'],
            'source':'shenliutang',
        }
        self.update(data)
def loadID():
    '''load the last id'''
    try:
        id=open(idfile, 'r').readlines()[0].strip()
        return id
    except:
        return ""

def saveID(id):
    try:
        f=open(idfile, "w")
        f.write(id.strip())
    except:
        pass

def log(s):
    f=open(logfile, "wa")
    f.write(s+"\n")
    f.close()

def main():

    fanfou=Fanfou("tar_gz", "$tar_gz$")
#    fanfou=Fanfou("debug", "debug")
    id=loadID()
    saved=0
    page=1
    result={}

    while 1:
        msgs=fanfou.get_msg("reply", since_id=id, page=page)
        page+=1
        if not msgs:
            print 'finished'
            break
        for m in msgs:
            m=Msg(m)
            m=m.get_msg()
            result[m['id']]=m

            if not saved:
                saveID(m['id'])
                print "id saved as ", m['id']
                saved=1 

    for k,v  in result.items():
        fanfou.reply(v)

main()
