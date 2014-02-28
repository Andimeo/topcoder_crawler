from re import compile
from database import init, close
from Topcoder import Topcoder
from MySQLdb import escape_string
from urllib2 import urlopen
from utils import remove_tag
from pickle import dump, load
from os.path import exists

editorial_root_url = 'http://apps.topcoder.com/wiki/display/tc/Algorithm+Problem+Set+Analysis'
url_set = None

def gen_editorial_urls():
	global url_set
	if exists('unfinished_url'):
		f = open('unfinished_url', 'rb')
		url_set = load(f)
		f.close()
		return list(url_set)
	page = urlopen(editorial_root_url).read()
	p0 = compile('<A href="http://apps.topcoder.com/wiki/display/tc/.*?">Problem Set & Analysis</A>')
	p1 = compile('<A href="http://www.topcoder.com/tc\?module=Static&d1=match_editorials&d2=.*?">Problem Set & Analysis</A>')
	urls0 = p0.findall(page)
	urls1 = p1.findall(page)
	p = compile('".*?"')
	urls = [p.findall(x)[0][1:-1] for x in urls0] + [p.findall(x)[0][1:-1] for x in urls1]
	url_set = set(urls)
	return urls

rules = ['<span class="bigTitle">Match summary</span>[\d\D]*?<.*?>TopCoder Member<.*?>',
'<h2>Match summary</h2>[\d\D]*?<.*?>TopCoder Member</.*?>', 
'<H2>Match summary</H2>[\d\D]*?<.*?>TopCoder Member</.*?>', 
'<h1>.*?</h2>[\d\D]*?<.*?>TopCoder Member</.*?>', 
'<H1>[\d\D]*?</H1>[\d\D]*?<.*?>TopCoder Member<.*?>',
'<h2>Match summary</h2>[\d\D]*?<.*?>TopCoder Members</.*?>', 
'<H2>Match summary</H2>[\d\D]*?<.*?>TopCoder Members</.*?>',
'<H2>Match summary</H2>[\d\D]*?without precomputing</A>).</P>',
'<h1>[\d\D]*?</h1>[\d\D]*?<.*?>TopCoder Member<.*?>',
'<h2>Match summary</h2>[\d\D]*?solution</a> during the match.',
'<H2>Match summary</H2>[\d\D]*?</TBODY></TABLE></BLOCKQUOTE>',
'<h2>Match summary</h2>[\d\D]*?### PROBLEM WRITEUP GOES HERE', 
'<h2>Match summary</h2>[\d\D]*?<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"', 
'<span class="bodySubtitle">SRM 282</span><br>Tuesday, January 10, 200[\d\D]*?<.*?>TopCoder Member</.*?>', 
'<h2>Match summary</h2>[\d\D]*?for an implementation of pretty similar approach.'] 

def parse(cur, url):
	page = urlopen(url).read()
	name = url.split('/')[-1].replace('+',' ').replace('_', ' ')
	if name.startswith('tc?'):
		name = url.split('=')[-1]
	content = None
	for rule in rules:
		try:
			content_p = compile(rule)
			content = content_p.findall(page)[0]
			break
		except:
			continue
	if content == None:
		print name, url, 'failed'
		f = open('unfinished_url', 'wb')
		dump(url_set, f)
		f.close()
	cur.execute('insert into editorial values("%s", "%s")' % (name, escape_string(content)))
	print name

if __name__ == '__main__':
	urls = gen_editorial_urls()
	conn, cur = init()
	for url in urls:
		parse(cur, url)
		url_set = url_set - set([url])
	close(conn)

