from urllib2 import urlopen
from re import compile
from database import init, close
from Topcoder import Topcoder
from MySQLdb import escape_string, IntegrityError

topcoder_site_url = 'http://community.topcoder.com'
insert_template = 'insert into problem (id, name, description, url) values(%s, "%s", "%s", "%s")'

def get_contest_list(cur):
	cur.execute('select id, url from contest')
	l = cur.fetchall()
	return l

def gen_problem(cur, topcoder):
	contest_list = get_contest_list(cur)
	c = 0
	for (c_id, url) in contest_list:
		print c_id, url
		c += 1
		if c % 50 == 0:
			topcoder.login()
		page = topcoder.get_page(url)
		
		p = compile('<a name="problem_stats"></a>[\d\D]*?</table>')
		divs = p.findall(page)
		for i in xrange(len(divs)):
			div = divs[i]
			p = compile('<tr>[\d\D]*?</tr>')
			trs = p.findall(div)
			for tr in trs:
				if tr.find('/stat?c=problem_statement&pm=') == -1:
					continue
				p = compile('/stat\?c=problem_statement&pm=[0-9]*&rd=[0-9]*')
				url = topcoder_site_url + p.findall(tr)[0]
				p = compile('pm=[0-9]*')
				p_id = p.findall(url)[0][3:]

				p = compile('>.*?<')
				name = p.findall(tr)[2][1:-1]
				print p_id, url, name
				page = topcoder.get_page(url)
				p = compile('<\!-- BEGIN BODY -->[\d\D]*?<\!-- END BODY -->')
				description = p.findall(page)[0]
				
				try:
					cur.execute(insert_template % (p_id, name, escape_string(description), url))					
				except IntegrityError:
					print p_id, 'Duplicate!'
		print
			
def test(url):
	import pdb
	pdb.set_trace()
	page = topcoder.get_page(url)
	p = compile('<a name="problem_stats"></a>[\d\D]*?</table>')
	divs = p.findall(page)
	for i in xrange(len(divs)):
		div = divs[i]
		p = compile('<tr>[\d\D]*?</tr>')
		trs = p.findall(div)
		for tr in trs:
			if tr.find('/stat?c=problem_statement&pm=') == -1:
				continue
			p = compile('/stat\?c=problem_statement&pm=[0-9]*&rd=[0-9]*')
			url = topcoder_site_url + p.findall(tr)[0]
			p = compile('pm=[0-9]*')
			p_id = p.findall(url)[0][3:]

			p = compile('>.*?<')
			name = p.findall(tr)[2][1:-1]
			print p_id, url, name
			page = topcoder.get_page(url)
			p = compile('<\!-- BEGIN BODY -->[\d\D]*?<\!-- END BODY -->')
			description = p.findall(page)[0]
			
			try:
				cur.execute(insert_template % (p_id, name, escape_string(description), url))					
			except IntegrityError:
				print p_id, 'Duplicate!'
	print
	
if __name__ == '__main__':
	topcoder = Topcoder()
	topcoder.login()
	conn, cur = init()
	gen_problem(cur, topcoder)
	#test("http://community.topcoder.com/stat?c=round_overview&er=5&rd=14734");
	close(conn)
