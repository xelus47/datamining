class Instaclass():
	version='1.0--b-w27-d7'
	#
	# options (do not change during __init__)
	#
	imagedl=False
	nocache=True
	complete=False

	#
	# "memory" (do not touch pls)
	#
	imgLoop=0
	pageData={}
	tmpData={}
	workingData={}
	pageType='Unknown'
	destination='error'
	safeSpace=''
	keywords_ignore=[]
	def __UTF8(self,d):
		return d.decode('unicode-escape').encode('utf8','replace')

	def _open_UTF8(self,file):
		return file.read().decode('utf8').encode('unicode-escape')

	def __type(self,i):
		if type(i) is str:
			if i.startswith('/explore/'):
				if '/locations/' in i:
					return 'LocationsPage' # TODO: prove this
				elif '/tags/' in i:
					return 'TagsPage'
				else:
					return 'Unknown'
			elif i.startswith('/p/'):
				return 'PostPage'
			elif i.count('/')<=2:
				return 'ProfilePage'
			else:
				return "Unknown"
		elif type(i) is dict:
			if 'entry_data' in i:
				for t in i['entry_data']:
					return t # which returns the first (and only) index in dict
			else:
				return 'Unknown'
		else:
			return 'Unknown'

	def __grabData(self,connectResponse,useTemp=False):
		match = '_sharedData = '
		data = connectResponse.read().decode('utf-8').encode('unicode-escape','replace')
		if not bool(data.count(match)):
			#print "Error: could not find <%s>" % match
			if not useTemp:
				self.pageData={}
				return False
			else:
				return {}
		else:
			s1=data[data.find(match):]
			s2=s1[len(match):s1.find('</script>')-1]
			sharedData=self.__json.loads(s2.decode('unicode-escape'))
			if self.__type(sharedData)=='Unknown':
				if not useTemp:
					self.pageData={}
					return False
				else:
					return {}
			else:
				#
				# save <sharedData>
				#
				pageType=self.__type(sharedData)
				if not useTemp:
					self.pageData=sharedData['entry_data'][pageType][0]
					self.pageType=pageType

					if not self.nocache:
						f=open('tmp.txt','w')
						f.write(self.__UTF8(self.__json.dumps(self.pageData,indent=4)))
						#f.write(self.__json.dumps(self.pageData,indent=4))
						f.close()
						
					del sharedData
					return True
				else:
					return sharedData['entry_data'][pageType][0]

	def __init__(self,user_agent='Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/47.0'): # firefox 47 on win7
		self.__json=__import__('json')
		self.__time=__import__('time')
		self.__datetime=__import__('datetime')
		self.__urllib=__import__('urllib')
		self.__os=__import__('os')
		import httplib, datetime
		self.connection = httplib.HTTPSConnection('www.instagram.com')
		self.user_agent = user_agent
		self.today = str(datetime.date.today())

		if self.__os.path.exists('keywords-ignore.txt'):
			f=open('keywords-ignore.txt','r')
			s=f.read()
			f.close()
			s=s.replace('\n',',').replace(' ','')
			self.keywords_ignore+=[m.lower() for m in s.split(',')]

	def download(self,url,name):
		url = url.split('?')[0] # get rid of junk
		ext = self.__os.path.splitext(url)[1]
		saveAs=self.safeSpace+'/'+name+ext
		if not self.__os.path.exists(saveAs):
			self.__urllib.urlretrieve(url,saveAs)
		return name+ext

	def mySafeSpace(self):
		if self.pageType!='Unknown':
			os = self.__os
			name = self.destination[1:-1].replace('/','_')
			saveAs='saves/%s/%s' % (self.pageType,name)

			saveStr=''
			for folder in saveAs.split('/'):
				if saveStr=='':
					saveStr=folder
				else:
					saveStr+=('/%s' % folder)
				
				if not os.path.exists(saveStr):
					os.mkdir(saveStr)

			self.safeSpace=saveAs

	def sortKeys(self,update={},cutoff=2):
		newObj={}
		maximum=1
		for key in update:
			#if update[key]>maximum:
			#	maximum=update[key]
			if update[key]>=cutoff:
				keyStr=str(update[key])
				if not keyStr in newObj:
					newObj[keyStr]=[key]
				else:
					newObj[keyStr].append(key)
		return newObj


	def addKeywords(self,string='',update={}):
		words=string.split(' ')
		for word in words:
			if not word=='' and not self.stripSpecial(word.lower()) in self.keywords_ignore: # if not empty and not ignored
				if word in update:
					update[word]+=1
				else:
					update[word]=1

		return update

	def stripSpecial(self,word):
		exceptions='#@'
		assembled=''
		for letter in word:
			if ord(letter)>=ord('1') and ord(letter)<=ord('z') or letter in exceptions:
				assembled+=letter
		return assembled

	def connect(self,path):
		self.connection.close()
		self.connection.putrequest('GET',path)
		self.connection.putheader('User-agent',self.user_agent)
		#self.connection.putheader('Accept-Charset','ascii')
		self.connection.endheaders()
		return self.connection.getresponse()


	def test(self,testpath=''):
		if testpath=='':
			testpath='/guusvogel/'

		self.destination=testpath

		response = self.connect(testpath)
		headers = response.getheaders()
		status = '%s %s' % (response.status,response.reason)
		styledHeaders = self.__json.dumps(headers, indent=4)
		if not self.nocache:
			f=open('request.txt','w')
			f.write('GET '+testpath+'\n'+status+'\n'+styledHeaders)
			f.close()

		found = self.__grabData(response)

		self.connection.close()

		return {
			"hacked":found,
			"http":(response.status,response.reason),
			"url":testpath
		}

	def bash(self,destination):
		self.destination=destination
		result = self.test(destination)
		if result['http'][0]!=200 or not result['hacked']:
			print "HTTPError %s\nFailed to bash <%s>" % (result['http'][0], result['url'])
			return 0
		else: # http 200 + hacked
			if self.destination.count('?')>0:
				self.destination=self.destination.split('?')[0]

			print '%s %s %s' % (result['http'][0],result['http'][1],result['url'])
			if not self.pageType=='ProfilePage':
				print "Type <%s> not supported" % pageType
			#
			# ProfilePage
			#
			else: # elif pageType=='ProfilePage':
				self.mySafeSpace()
				user = self.pageData['user']
				if not 'id' in self.workingData: # if not initiated:
					self.workingData={'keywords':{},'locations':{},'id':'','full_name':'','connections':{},'is_private':False}

					self.workingData['_appVer']=self.version
					self.workingData['username']=user['username']
					self.workingData['is_private']=user['is_private']
					self.workingData['full_name']=user['full_name']
					self.workingData['id']=user['id']

					if 'profile_pic_url_hd' in user:
						self.download(url=user['profile_pic_url_hd'],name='profile_pic_hd')
					else:
						self.download(url=user['profile_pic_url'],name='profile_pic')
					
					self.workingData['keywords']=self.addKeywords(string=user['biography'],update=self.workingData['keywords'])

				nodes = user['media']['nodes']

				for node in nodes:
					# TODO: find a way to get comments?
					date = str(self.__datetime.datetime.fromtimestamp(node['date']).strftime('%Y-%m-%d')).strip('-')
					if self.imagedl:
						self.imgLoop+=1
						if not self.__os.path.exists(self.safeSpace+'/gallery'):
							self.__os.mkdir(self.safeSpace+'/gallery')
						name = 'gallery/%s-%s' % (date,node['code'])
						url=node['display_src'].split('?')[0]
						ext=self.__os.path.splitext(url)[1]
						#print node['code']
						print self.download(url=node['display_src'],name=name) + ('(%s/%s)' % (self.imgLoop,user['media']['count']))

					if 'caption' in node: # some posts don't have captions
						self.workingData['keywords']=self.addKeywords(string=node['caption'],update=self.workingData['keywords'])


				if user['media']['page_info']['has_next_page'] and self.complete:
					if self.imagedl:
						print "Pausing..."
						self.__time.sleep(2)
					self.bash(self.destination+'?max_id='+user['media']['page_info']['end_cursor'])


				else:
					self.workingData['keywords']=self.sortKeys(self.workingData['keywords'])

					saveData=self.__json.dumps(self.workingData,indent=2,sort_keys=True)

					file=open(self.safeSpace+'/data.json', 'w')
					file.write(user['username']+'_bashed='+saveData)
					file.close()


					#
					# check against previous save file (if it exists)
					#
					if False:
						f=open(self.safeSpace+'/data.json','r')

						self.workingData=self._open_UTF8(f)
						f.close()

						#
						# if conflict, add it to log, print it to console and save the new data to data_%timestamp%.json
						#
					print 'Jobs finished'

