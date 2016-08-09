#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import psycopg2 as pg2
import sys

def getcfg(filename):
    try:
        with open(filename,'rb') as cfg:
            cfglist = cfg.readlines()
            a = []
            for i in range(len(cfglist)):
                if cfglist[i] == '\r\n':
                    pass
                elif cfglist[i] == '\n':
                    pass
                elif cfglist[i] == '\r':
                    pass
                else:
                    cfglist[i] = cfglist[i].replace('\r','')
                    cfglist[i] = cfglist[i].replace('\n','')
                    cfglist[i] = cfglist[i].replace(' ','')
                    cfglist[i] = cfglist[i].split('=')
                    a.append((cfglist[i][0],cfglist[i][1]))
        a = dict(a)
    except Exception,e:
        print e
        print 'Please check checkboard.cfg,looks like something configured wrong.'
        anyenter = raw_input('Press ENTER to confirm.')
    return a

def selectarticle(aid,kind,db,us,pwd,hst,pt):
    aid = int(aid)
    if kind == 1:
        sql = 'select title,content from spam_article where aid=%s' % (aid)
    else:
        sql = 'select a.title,ac.content from article a,article_content ac where aid=%s and a.guid=ac.guid' % (aid)
    con = pg2.connect(
        database=db,
        user=us,
        password=pwd,
        host=hst,
        port=pt)
    cur = con.cursor()
    cur.execute(sql)
    output = cur.fetchall()
    con.close()
    both = output[0][0]+output[0][1]
    art = {'title':output[0][0],'content':output[0][1],'both':both}
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

cfg = getcfg('SearchKeyWord.cfg.txt')

conn = pg2.connect(
    database=cfg['database'],
    user=cfg['user'],
    password=cfg['password'],
    host=cfg['host'],
    port=cfg['port'])

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
print ' All key words are not included such as + ( )'
print '*'*78

conn.close()

if __name__=='__main__':
    while True:
        aid = raw_input(' Aid:')
        aid = aid.replace(' ','')

        if aid == 'q':
            break
        else:
            pass

        isspam = cfg['isspam']

        if isspam == '1':
            kind = 1
        else:
            kind = 0

        article = selectarticle(aid,kind,cfg['database'],cfg['user'],cfg['password'],cfg['host'],cfg['port'])

        with open('aa.txt','w') as aa:
            aa.write('-'*30+'Title'+'-'*30+'\n')
            aa.write(article['title'])
        #    aa.write(article['title'].decode('utf8').encode('gbk'))
            aa.write('\n\n')
            aa.write('-'*30+'Content'+'-'*30+'\n')
            aa.write(article['content'])
        #    aa.write(article['content'].decode('utf8').encode('gbk'))
            aa.write('\n\n')
            aa.write('-'*30+'Both'+'-'*30+'\n')
            aa.write(article['both'])
        #    aa.write(article['both'].decode('utf8').encode('gbk'))

        print ' '
        print ' Title length:',len(article['title'].decode('utf8'))
        print ' Content length:',len(article['content'].decode('utf8')),'\n'

        kids = []
        print ' Search title ...'
        for a1 in output1:
            if ismatch(a1[1],article['title']):
                print '',a1[0],'---> ',a1[1].decode('utf8')
                kids.append(int(a1[0]))
            else:
                pass
        print ' Title match kids:',kids,'\n'

        kids = []
        print ' Search content ...'
        for a2 in output2:
            if ismatch(a2[1],article['content']):
                print '',a2[0],'---> ',a2[1].decode('utf8')
                kids.append(int(a2[0]))
            else:
                pass
        print ' Content match kids:',kids,'\n'

        kids = []
        print ' Search both ...'
        for a3 in output3:
            if ismatch(a3[1],article['both']):
                print '',a3[0],'---> ',a3[1].decode('utf8')
                kids.append(int(a3[0]))
            else:
                pass
        print ' Article match kids:',kids,'\n'
        print '*'*78

sys.exit()
