from urllib2 import urlopen
from re import compile
from MySQLdb import connect
from database import init, close

topcoder_site_url = 'http://community.topcoder.com'
archive_url = 'http://community.topcoder.com/tc?module=MatchList&sc=&sd=&nr=200&sr=%d'
insert_template = 'insert into contest values(%s,"%s","%s","%s","%s")'

def gen_contest(cur):
	for start in [1, 201, 401, 601]:
		resp = urlopen(archive_url % start)
		page = resp.read()
		resp.close()
		
		p1 = compile('<td class="value" nowrap="nowrap">.*?</td>')
		p2 = compile('<td class="valueC">.*?</td>')
		
		l1 = p1.findall(page)
		l2 = p2.findall(page)
		for i in xrange(len(l1)):
			p3 = compile('".*?"')
			url = topcoder_site_url + p3.findall(l1[i])[2][1:-1]
			p3 = compile('rd=[0-9]*')
			c_id = p3.findall(url)[0][3:]
			p3 = compile('>.*?<')
			name = p3.findall(l1[i])[1][1:-1]
			l = name.split()
			if l[1].startswith('&#'):
				l = l[:1] + l[2:]
			name = ' '.join(l)
			p3 = compile('[0-9]*?\.[0-9]*?\.[0-9]*')
			date = p3.findall(l2[i*2])[0]
			l = date.split('.')
			l = [l[2]] + l[:2]
			date = '.'.join(l)
			p3 = compile('http://.*forumID=[0-9]*')
			discuss_url = p3.findall(l2[i*2+1])[0]
			print url, c_id, name, date, discuss_url
			cur.execute(insert_template % (c_id, name, url, date, discuss_url))
if __name__ == '__main__':
	conn,cur = init()
	gen_contest(cur)
	close(conn)			
			
				
