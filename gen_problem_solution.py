from Topcoder import Topcoder
from database import init, close
from re import compile
from utils import remove_tag, unescape
from urllib2 import HTTPError
from MySQLdb import escape_string

problem_detail_url = 'http://community.topcoder.com/tc?module=ProblemDetail&rd=%d&pm=%d'
topcoder_site_url = 'http://community.topcoder.com'
update_template = 'update problem set %s="%s" where id=%d'

testcase_id = 0
testcase_crawled = False

def get_id_pair(cur):
	cur.execute('select c_id, p_id from contest_problem')
	id_pairs = cur.fetchall()
	return id_pairs

def gen_solution(cur, td, num, p_id):
#	import pdb
#	pdb.set_trace()
	global testcase_id
	global testcase_crawled

	if num == 0:
		column_name = 'java'
	elif num == 1:
		column_name = 'cpp'
	elif num == 2:
		column_name = 'csharp'
	else:
		column_name = 'VB'
	cur.execute('select %s from problem where id = %d' % (column_name, p_id))
	if cur.fetchall()[0][0] != None:
		return
	p = compile('"/stat\?c=problem_solution.*?"')
	l = p.findall(td)
	if len(l) == 1:
		url = topcoder_site_url + unescape(l[0][1:-1])
		try:
			page = topcoder.get_page(url)
		except Exception, e:
			print url, e
			return
		p = compile('<TD CLASS="problemText" COLSPAN="8" VALIGN="middle" ALIGN="left">[\d\D]*?</TD>')
		try:
			code = escape_string(p.findall(page)[0])
		except Exception, e:
			print 'No code found:',url,e
			return
		print p_id, column_name, url
		cur.execute(update_template % (column_name, code, p_id))
		
		if testcase_crawled:
			return
		p = compile('<!-- System Testing -->[\d\D]*?</TABLE>')
		try:
			test_block = p.findall(page)[0]
		except Exception, e:
			print 'No test case found:',url,e
			return
		p = compile('<TR valign="top">[\d\D]*?</TR>')
		trs = p.findall(test_block)
		for tr in trs:
			try:
				p = compile('<TD CLASS="statText" ALIGN="left">[\d\D]*?</TD>')
				test_argument = ''.join(remove_tag(p.findall(tr)[0]).split())
			except:
				p = compile('<TD BACKGROUND="/i/steel_blue_bg.gif" CLASS="statText" ALIGN="left">[\d\D]*?</TD>')
				test_argument = ''.join(remove_tag(p.findall(tr)[0]).split())
			try:	
				p = compile('<TD CLASS="statText" ALIGN="right">[\d\D]*?</TD>')
				expected_result = ''.join(remove_tag(p.findall(tr)[0]).split())
			except:
				p = compile('<TD BACKGROUND="/i/steel_blue_bg.gif" CLASS="statText" ALIGN="right">[\d\D]*?</TD>')
                                expected_result = ''.join(remove_tag(p.findall(tr)[0]).split())
			cur.execute('insert into testcase values(%d, "%s", "%s")'%(testcase_id,escape_string(test_argument), escape_string(expected_result)))
			cur.execute('insert into problem_testcase values(%d, %d)' %(p_id, testcase_id))
			testcase_id += 1
		testcase_crawled = True
		
def gen_href(cur, topcoder):
	global testcase_crawled
	id_pairs = get_id_pair(cur)
	c = 0
	for c_id, p_id in id_pairs:
		print c_id, p_id
		url = problem_detail_url % (c_id, p_id)
		c += 1
		if c % 50 == 0:
			topcoder.login()
		try:
			page = topcoder.get_page(url)
		except Exception, e:
			print c_id, p_id, e
			continue
		#import pdb
		#pdb.set_trace()
		p = compile('<td class="statText">Top Submission</td>[\d\D]*?</tr>')
		divs = p.findall(page)
		testcase_crawled = False
		for div in divs:
			p = compile('<td class="statText" align="right">[\d\D]*?</td>')
			tds = p.findall(div)
			for i in xrange(4):
				gen_solution(cur, tds[i], i, p_id)


if __name__ == '__main__':
	topcoder = Topcoder()
	topcoder.login()
	conn, cur = init()
	gen_href(cur, topcoder)
	close(conn)
