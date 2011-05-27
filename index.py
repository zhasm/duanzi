#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#author:         rex
#blog:           http://iregex.org
#filename        weibo.py
#created:        2011-05-20 10:46

from fanfou import Fanfou
from misc import *
import re
from time import sleep

SLEEP_INTERVAL=15

fanfouname="tar_gz"
fanfoupwd="$tar_gz$"

def getSinceID():
    try:
        f=open('id.txt')
        lines=f.readlines()
        return lines[-1].strip()
    except:
        return ""

def getMessages(f, since_id=""):

    def _trim(msg):
        '''trim the reply part'''

        regex=re.compile(r"""^@\S+\s*""")
        return regex.sub('', msg)

    msgs=f.Replies(since_id=since_id)

    ids=[msg['id'] for msg in msgs]
    msgs= [ chinese(msg['text']) for msg in msgs]
    msgs= [ _trim(msg) for msg in msgs]

    msgs.reverse()
    ids.reverse()

    return (msgs, ids)


def saveIDs(ids):
    ids="\n".join(ids)

    try:
        f=open('id.txt', 'w')
        f.write(ids)
        f.close()

    except:
        writelog("Error: write to idfile error!")

def post(msgs, f):
    for msg in msgs:
        f.Update(msg)

def main():

    writelog("Entered Loop")
    f=Fanfou(fanfouname, fanfoupwd)

    while True:
        id=getSinceID()
        msgs, ids=getMessages(f, id)

        if ids:

            try:
                post(msgs, f)
                saveIDs(ids)
            except Exception, e:
                writelog("Error:"+str(e))

        else:
            writelog("No data")

        sleep(SLEEP_INTERVAL)

if __name__=="__main__":
    main()

