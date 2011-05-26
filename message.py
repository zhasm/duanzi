'''parse raw fanfou message and only return important items'''
from time import *
import time
import json
import re

ISOTIMEFORMAT='%Y-%m-%d %X'
TIMEFORMAT="%a %b %d %X +0000 %Y"

def unicode2utf8(ustr):
    '''print raw of "\u996d\u51c9\u4e86\u5426" unicode'''
    return eval("""u'''%s'''""" % ustr)

def epoch2str( x ):
    '''Convert unix epoch to string'''
    return strftime( "%Y-%m-%d %H:%M:%S", gmtime(x+3600*8) )

def time_from_0_to_8(timestr, timezone=8):

    #Sat Jan 03 23:08:54 +0000 2009
    x=time.strptime(timestr, TIMEFORMAT)
    m=time.mktime(x)+60*60*timezone
#    p=time.strftime(ISOTIMEFORMAT,time.localtime(m))
    return int(m)

def unescape(s):
    s=s.replace("&lt;","<")
    s=s.replace("&gt;",">")
    s=s.replace("&quot;",'"')
    s=s.replace("&apos;","'")
    s=s.replace("&amp;","&")
    s=s.replace("\\","")
    return s

class Msg:
    def __init__(self, msg):
        #self.created_at=time_from_0_to_8(msg['created_at'])
        try:
            self.id=msg['id']
            self.at=time_from_0_to_8(msg['created_at'])
            self.userid=unicode2utf8(msg['user']['id'])
            self.username=unicode2utf8(msg['user']['screen_name'])
            self.text=unicode2utf8(msg['text'])
            self.text=unescape(self.text)
        except:
            print json.dumps(msg, indent=3)

    def get_msg(self):
        try:
            return {
                'id':self.id,
                'userid':self.userid,
                'text':self.text.split(" ", 1)[1],
                'at':self.at,
                'name':self.username,
            }
        except:
            return None

    def show(self):
        try:
            print "{\n\tmsgID:\t", self.id
            print "\tAt:\t", epoch2str(self.at)
            print "\tFrom:\t", self.username
            print "\tMsg:\t", self.text
            print "}\n"
        except:
            pass
    def parse(self):
        msg=self.text

