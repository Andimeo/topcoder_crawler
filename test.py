from urllib2 import urlopen
from re import compile

s = urlopen('http://community.topcoder.com/stat?c=problem_statement&pm=11934&rd=14734')
page = s.read()
s.close()

p = compile('<\!-- BEGIN BODY -->[\d\D]*?<\!-- END BODY -->')
print p.findall(page)
