import urllib2
import re
import mysql.connector


def gettopbooks(start):
    cursor = conn.cursor()
    url = 'https://book.douban.com/top250?start=' + str(start)
    pattern = re.compile('<a class="nbg" href.*?subject/(.*?)/".*?\{i:\'(.*?)\'.*?src="(.*?)".*?title="(.*?)".*?class="pl">(.*?)</p>', re.S)
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    items = re.findall(pattern, content)
    for item in items:
        print item[0], start + int(item[1])+1, item[2], item[3], item[4]
        cursor.execute('insert into think_topbook (bookid, topnum,imgsrc,title,description) '
                       'values (%s, %s, %s, %s, %s)',
                       [item[0], start +int(item[1])+1, item[2], item[3], item[4]])

    conn.commit()
    cursor.close()


def gettopchartbooks():
    cursor = conn.cursor()
    url = 'https://book.douban.com/chart?subcat=I'
    pattern = re.compile('num-box">(.*?)</.*?subject/(.*?)/">.*?src="(.*?)"/>.*?\d/">(.*?)</a>.*?gray">(.*?)<', re.S)
    response = urllib2.urlopen(url)
    content = response.read().decode('utf-8')
    items = re.findall(pattern, content)
    for item in items:
        cursor.execute('insert into think_chartbook (chartnum,bookid,imgsrc,title,description) '
                       'values (%s,%s,%s,%s,%s)',
                       [item[0], item[1], item[2], item[3].strip(), item[4].strip()])
        print item[0], item[1], item[2], item[3].strip(), item[4].strip()
    conn.commit()
    cursor.close()


conn = mysql.connector.connect(user='root', password='', database='doubanbook')
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
