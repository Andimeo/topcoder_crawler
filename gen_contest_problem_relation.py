from Topcoder import Topcoder
from database import init, close
from re import compile
from utils import remove_tag
from urllib2 import HTTPError

topcoder_site_url = 'http://community.topcoder.com'

def get_urls(cur):
	cur.execute('select description from problem')
	description = cur.fetchall()
	urls = []
	for des in description:
		p = compile('/tc\?module=ProblemDetail&rd=[0-9]*&pm=[0-9]*')
		t_t_urls = list(set(p.findall(des[0])))
		for t_t_t_url in t_t_urls:
			t_urls = topcoder_site_url + t_t_t_url
			urls.append(t_urls)
	return urls

insert_template1 = 'insert into contest_problem values(%s, %s, %d, %d, %s, %s, %s, "%s", "%s", "%s")'
insert_template2 = 'update problem set categary="%s", writer="%s", tester="%s" where id=%s'
def gen_relation(cur, topcoder):
	urls = get_urls(cur)
	c = 0
	for url in urls:
		p = compile('[0-9]+')
#		import pdb
#		pdb.set_trace()
		c_id, p_id = p.findall(url)
		c += 1		
		if c % 50 == 0:
			topcoder.login()
		try:
			page = topcoder.get_page(url)
		except HTTPError, e:
			print url,e
			continue
		p = compile('<!-- BEGIN BODY -->[\d\D]*<!-- END BODY -->')
		page = p.findall(page)[0]
		p = compile('<table[\d\D]*?</table>')
		tables = p.findall(page)
		p = compile('<tr>[\d\D]*?</tr>')
		trs = p.findall(tables[1])
		div = []
		level = []
		l = remove_tag(trs[2]).split('\n')
		for ll in l:
			if ll.strip().startswith('D'):
				t_l = ll.split()
				if t_l[1] == 'I':
					div.append(1)
				else:
					div.append(2)
				if t_l[3].lower() == 'one':
					level.append(1)
				elif t_l[3].lower() == 'two':
					level.append(2)
				else:	
					level.append(3)
		categary = ' '.join(remove_tag(trs[3]).split()[1:])
		writer = ' '.join(remove_tag(trs[4]).split()[1:])
		tester = ' '.join(remove_tag(trs[5]).split()[1:])
		trs = p.findall(tables[2])
		value = remove_tag(trs[1]).split()[2:]
		competitor = remove_tag(trs[2]).split()[1:]
		opens = remove_tag(trs[3]).split()[1:]
		percent_open = remove_tag(trs[4]).split()[2:]
		percent_submit = remove_tag(trs[5]).split()[2:]
		overall_accuracy = remove_tag(trs[6]).split()[2:]
		
		try:
			for i in xrange(len(div)):
				cur.execute(insert_template1 % (c_id, p_id, div[i], level[i], value[i], competitor[i], opens[i], percent_open[i], percent_submit[i], overall_accuracy[i]))
				print c_id, p_id, div[i], level[i], value[i], competitor[i], opens[i], percent_open[i], percent_submit[i], overall_accuracy[i]
		except:
			print c_id, p_id, ' not found details!'
		cur.execute(insert_template2 % (categary, writer, tester, p_id))
		print categary, writer, tester, p_id

if __name__ == '__main__':
	topcoder = Topcoder()
	topcoder.login()
	conn, cur = init()
	gen_relation(cur, topcoder)
	close(conn)	
