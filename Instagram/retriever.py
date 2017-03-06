
"""
Content			Used abbr		link
profile page	@, /, /u/		/%s
tag search page #, /t/			/explore/tags/%s
place page		/l/				/explore/locations/%id/[%name]
post			/p/				/p/%id


"""

class Retriever(object):
	def __str__(self):
		return "??"

	stype='q'
	location=''
	search_page_type=''
	timeout=6

	instagram_pages={
		'ProfilePage':{'url':'/','entry_data':'ProfilePage','query':[r'@','/',r'u']},
		'LocationsPage':{'url':'/explore/locations/','entry_data':'LocationsPage','query':[r'l']},
		'TagPage':{'url':'/explore/tags/','entry_data':'TagPage','query':[r'#',r't']},
		'PostPage':{'url':'/p/','entry_data':'PostPage','query':[r'p']},
	}

	def __init__(self):
		self.re=__import__('re')
		self.time=__import__('time')
		self.json=__import__('json')
		self.httplib=__import__('httplib')

		## Generate regex string

		ls_alias = []
		ls_indicator = []
		for typ in self.instagram_pages:
			for q in self.instagram_pages[typ]['query']:
				re = ur"^(?P<word>\w*)$"
				m = self.re.search(re,q)
				if m: # if it's any letter(s)
					ls_alias.append(m.group('word'))
				else:
					ls_indicator.append(q)


		self.regex = ur"^\/?((?P<alias>"+"|".join(ls_alias)+ur")\/|(?P<indicator>"+"|".join(ls_indicator)+"))(?P<query>[a-zA-Z0-9]+)$"


	def parse_location_replace(self,matchobj):

		#print matchobj.groupdict(), matchobj.group(0)
		ind = matchobj.group('alias') or matchobj.group('indicator')
		#print "ind",ind

		for typ in self.instagram_pages:
			if ind in self.instagram_pages[typ]['query']:

				## Lookup and maybe parse known places 
				if typ=='LocationsPage':
					f2=open('assets/places.json','r')
					known_places = self.json.loads(f2.read())
					f2.close()
					if matchobj.group('query') in known_places:
						return self.instagram_pages[typ]['url']+known_places[matchobj.group('query')]+"/"


				return self.instagram_pages[typ]['url']+matchobj.group('query')+"/"
		return matchobj.group(0)

	def parse_location(self,loc):
		#regex = ur"^\/?((?P<alias>p|t|u|l)\/|(?P<indicator>\/|@|#))(?P<query>[a-zA-Z0-9]+)$"
		regex = self.regex
		return self.re.sub(regex,self.parse_location_replace,loc)

	def mine(self, location=None, args=None):
		if location==None:
			location=self.location

		if args==None:
			args=self.stype

		parsed_location=self.parse_location(location)
		print 'parsed:', parsed_location
		
		## HTTPS

		path = parsed_location
		user_agent='Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/47.0' # firefox 47 on win7
		conn = self.httplib.HTTPSConnection('www.instagram.com')
		conn.putrequest('GET',path)
		conn.putheader('user-agent',user_agent)
		conn.putheader('accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		conn.putheader('accept-language','en-GB,nl;q=0.8,ja;q=0.5,en;q=0.3')
		conn.putheader('referer','https://www.instagram.com/')
		conn.putheader('connection','keep-alive')
		conn.putheader('upgrade-insecure-requests','1')
		conn.endheaders()

		resp = conn.getresponse()
		try:
			assert resp.status==200, "Connection failure"
		except AssertionError:
			print path, resp.status, resp.reason
			s=str(resp.getheaders())
			data = resp.read()
			f=open('error','w')
			f.write(s+'\n\n\n'+data)
			f.close()
			return {"status":"error"}
		data = resp.read()

		# -----
		match = 'window._sharedData = '
		print data.count(match), len(data)

		try:
			assert data.count(match)==1, "Unknown data format"
		except AssertionError:
			print path, "unknown data format _sharedData (after download)"
			s=str(resp.getheaders())
			f=open('error','w')
			f.write(s+'\n\n\n'+data)
			f.close()
			return {"status":"error"}
		s1=data[data.find(match):]
		s2=s1[len(match):s1.find('</script>')-1]

		sharedData=self.json.loads(s2)#.decode('unicode-escape'))
		entry_data=sharedData['entry_data']

		f=open('tmp', 'w')
		f.write(self.json.dumps(entry_data,indent=2))
		f.close()

		return entry_data

	def match_location(self,test):
		regex = self.regex
		#regex = ur"^\/?((?P<alias>p|t|u|l)\/|(?P<indicator>\/|@|#))(?P<query>[a-zA-Z0-9]+)$"
		match=self.re.search(regex,test)
		if match:
			return True
		else:
			return False