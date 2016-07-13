#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import psycopg2 as pg2
import sys

def getarticle(filename):
    f = open(filename,'r')
    flist = f.readlines()
    article = ''
    for i in flist:
        article = article+i
    article = article.decode('gbk').encode('utf8')
    return article
def ismatch(keyword,article):
    y = 2
    er = 'wrong'
    word_list = keyword.split()
    for word in word_list:
        if re.search(word,article):
            y = 1
        else:
            y = 0
            break
    if y == 1:
        return True
    elif y == 0:
        return False
    else:
        return er

article = getarticle('a.txt')

conn = pg2.connect(
    database = 'yun',
    user = 'qiuchen',
    password = '123456',
    host = '192.168.2.128',
    port = '5432')
cur = conn.cursor()
sql = r"select kid,word from spam_keyword where filter_pos in (1,2) and word ~ '^(?!.*?\+).*$'"
cur.execute(sql)
output = cur.fetchall()

kids = []
for a in output:
    if ismatch(a[1],article):
        print a[0],a[1].decode('utf8')
        kids.append(a[0])
    else:
        pass

print kids
conn.close()

start = raw_input('******')
sys.exit()
