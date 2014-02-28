def remove_tag(s):
	left = s.find('<')
	if left == -1:
		return s
	right = s.find('>')
	if right == -1:
		return s
	return remove_tag(s[:left]+s[right+1:])

import htmllib

def unescape(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()
