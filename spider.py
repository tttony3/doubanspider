import urllib2
import re
import mysql.connector


def gettopbooks(start):
    cursor = conn.cursor()
    url = 'https://book.douban.com/top250?start=' + str(start)
    pattern = re.compile('<a class="nbg".*?subject/(.*?)/".*?{i:\'(.*?)\'.*?>', re.S)
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    items = re.findall(pattern, content)
    for item in items:
       cursor.execute('insert into think_topbook (bookid, topnum) values (%s, %s)', [item[0], start +int(item[1])+1])
       print item[0], start +int(item[1])+1
    conn.commit()
    cursor.close()


def gettopchartbooks():
    cursor = conn.cursor()
    url = 'https://book.douban.com/'
    pattern = re.compile('<a onclick="more.*?subject/(\d{8})/?(.*?)topchart-subject">', re.S)
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    items = re.findall(pattern, content)
    l = set([])
    for item in items:
        l.add(item[0])
    for item in l:
        cursor.execute('insert into think_chartbook (bookid) values (%s)', [item])
        print item
    conn.commit()
    cursor.close()


conn = mysql.connector.connect(user='root', password='password', database='doubanbook')
cursor = conn.cursor()
cursor.execute('delete from think_topbook')
cursor.execute('delete from think_chartbook')
conn.commit()
start =0
print 'gettopbooks'
while start <= 225:
    gettopbooks(start)
    start =start+25
print 'gettopchartbooks'
gettopchartbooks()
conn.close()


