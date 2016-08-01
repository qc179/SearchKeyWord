#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import psycopg2 as pg2
import sys

def getarticle(filename):
    f = open(filename,'r')
    flist = f.readlines()
    title = flist[0].decode('gbk').encode('utf8')
    content = ''
    article = ''
    for i in flist[1:]:
        content = content+i
    content = content.decode('gbk').encode('utf8')
    for i in flist:
        article = article+i
    article = article.decode('gbk').encode('utf8')
    art = {'title':title,'content':content,'article':article}
    return art

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

sql1 = r"select kid,word from spam_keyword where filter_pos=0 and word ~ '^(?!.*\+)(?!.*?\))(?!.*?\().*$'"
cur1 = conn.cursor()
cur1.execute(sql1)
output1 = cur1.fetchall()
print ' filter_pos=0 keyword:',len(output1)

sql2 = r"select kid,word from spam_keyword where filter_pos=1 and word ~ '^(?!.*\+)(?!.*?\))(?!.*?\().*$'"
cur2 = conn.cursor()
cur2.execute(sql2)
output2 = cur2.fetchall()
print ' filter_pos=1 keyword:',len(output2)

sql3 = r"select kid,word from spam_keyword where filter_pos=2 and word ~ '^(?!.*\+)(?!.*?\))(?!.*?\().*$'"
cur3 = conn.cursor()
cur3.execute(sql3)
output3 = cur3.fetchall()
print ' filter_pos=2 keyword:',len(output3)
print ' All key words are not included such as + ( )','\n'

print ' Title length:',len(article['title'].decode('utf8'))
print ' Content length:',len(article['content'].decode('utf8'))
print ' Article length:',len(article['article'].decode('utf8')),'\n'

kids = []
print ' Search title ...'
for a1 in output1:
    if ismatch(a1[1],article['title']):
        print '',a1[0],a1[1].decode('utf8')
        kids.append(a1[0])
    else:
        pass
print ' Title match kids:',kids,'\n'

kids = []
print ' Search content ...'
for a2 in output2:
    if ismatch(a2[1],article['content']):
        print '',a2[0],a2[1].decode('utf8')
        kids.append(a2[0])
    else:
        pass
print ' Content match kids:',kids,'\n'

kids = []
print ' Search article ...'
for a3 in output3:
    if ismatch(a3[1],article['article']):
        print '',a3[0],a3[1].decode('utf8')
        kids.append(a3[0])
    else:
        pass
print ' Article match kids:',kids,'\n'

conn.close()
start = raw_input('********************************************************')
sys.exit()
