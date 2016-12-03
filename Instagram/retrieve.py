import httplib # used for connections
import json

class dataObject(object):
	type='Unknown'
	def __init__(self):
		pass

	def summary(self):
		print "Summary:"


def parsePage(dumbJson):

	#f1 = open('tmp','w')
	#f1.write(json.dumps(dumbJson['entry_data'],indent=4,sort_keys=True))
	#f1.close()

	assert len(dumbJson['entry_data'].keys())==1, "Unknown data format"

	data=dataObject()
	data.type=dumbJson['entry_data'].keys()[0].encode('ascii')
	return data

def downloadPage(path):
	user_agent='Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/47.0' # firefox 47 on win7
	conn = httplib.HTTPSConnection('www.instagram.com')
	conn.putrequest('GET',path)
	conn.putheader('User-agent',user_agent)
	conn.endheaders()

	resp = conn.getresponse()
	assert resp.status==200, "Connection failure"
	data = resp.read()

	# -----
	match = '_sharedData = '
	assert data.count(match)==1, "Unknown data format"
	s1=data[data.find(match):]
	s2=s1[len(match):s1.find('</script>')-1]

	#f1 = open('tmp','w')
	#f1.write(s2)
	#f1.close()



	sharedData=json.loads(s2)#.decode('unicode-escape'))
	return sharedData