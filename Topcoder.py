import re
import urllib2
import cookielib
import urllib

class Topcoder:

	def login(self, url='https://community.topcoder.com/tc'):
		cj = cookielib.LWPCookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		username = 'Andimeo'
		password = '19885245201314'
	
		params = {'nextpage':'http://community.topcoder.com/tc', 'module':'Login', 'username':username, 'password':password, 'rem':'on'}
	
		self.url_data = urllib.urlencode(params)
	
		req = urllib2.Request(url, self.url_data)
	
		self.opener.open(req)
	
		#url = 'http://community.topcoder.com/stat?c=problem_statement&pm=11934&rd=14734'
		#req = urllib2.Request(url, url_data)
	
		#res = opener.open(req).read()
	
		#print res
	def get_page(self, url):
		req = urllib2.Request(url, self.url_data)
		return self.opener.open(req).read()
		
	def app_login(self, url='https://apps.topcoder.com/wiki/login.action'):
		cj = cookielib.LWPCookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		username = 'Andimeo'
		password = '19885245201314'
	
		params = {'os_username':'Andimeo', 'os_password':'19885245201314', 'login':'Log In', 'os_destination':'/display/tc/Algorithm+Problem+Set+Analysis'}
	
		self.url_data = urllib.urlencode(params)
	
		req = urllib2.Request(url, self.url_data)
	
		self.opener.open(req)



