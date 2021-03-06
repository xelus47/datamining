#!/usr/bin/env python2

import httplib, json, urllib, re

def sendRequest(method='GET',params="", path="/osistu_ospr/OnderwijsCatalogusZoekCursus.do",  HTTPS=True, cookie="",conn=None):
	user_agent='Mozilla/5.0 (Windows NT 6.1) Gecko/20100101 Firefox/47.0'
	if conn is None:
		conn = httplib.HTTPSConnection("www.osiris.universiteitutrecht.nl")
	path = "/osistu_ospr/OnderwijsCatalogusZoekCursus.do"

	conn.putrequest(method,path,params)
	conn.putheader("Host","www.osiris.universiteitutrecht.nl")
	conn.putheader('Cookie',cookie)
	conn.putheader('Referer','https://www.osiris.universiteitutrecht.nl/osistu_ospr/OnderwijsCatalogusZoekCursus.do')
	conn.putheader('User-agent',user_agent)
	conn.putheader('Connection','keep-alive')
	conn.putheader('Accept-Language','en-US,en;q=0.5')
	conn.putheader('Upgrade-Insecure-Requests','1')
	conn.endheaders()
	resp = conn.getresponse()

	return resp

def getAuth(conn = None):
	r = sendRequest(conn = conn)
	cookie = r.getheader('set-cookie')
	if r.status!=200:
		r.close()
		return ('failure',cookie)
	else:
		htmldata=r.read()
		r.close()

		regex = ur"requestToken=[a-zA-Z0-9]+"

		m = re.findall(regex, htmldata)
		if len(m)>0:
			requestToken = m[0].replace('requestToken=','')
		else:
			requestToken = "iamrequesttokenyes?"

		return (requestToken,cookie)




def mineSucces(rawPageData):
	""" str -> bool """
	return 0 < rawPageData.find('Klik op de cursus om de cursusinformatie te tonen.')





if __name__=='__main__':
	# POST: startUrl=StartPagina.do&inPortal=&callDirect=&requestToken=647ec1ae221e33bd7c33e1e2af58d110d1df3291&jaar_1=2016&zoek=&toon=&aanvangs_blok=&timeslot=geenVoorkeur&categorie=geenVoorkeur&cursustype=geenVoorkeur&faculteit=geenVoorkeur&organisatieonderdeel=geenVoorkeur&docent=&bijvakker=geenVoorkeur&voertaal=geenVoorkeur&event=zoeken&source=timeslot

	# startUrl=StartPagina.do&inPortal=&callDirect=&requestToken=afc13207c33d57b4c9329d4518e892f726947ead&jaar_1=2016&zoek=infi&toon=&aanvangs_blok=&
	# timeslot=geenVoorkeur&categorie=geenVoorkeur&cursustype=geenVoorkeur&faculteit=geenVoorkeur&organisatieonderdeel=geenVoorkeur&
	# docent=&bijvakker=geenVoorkeur&voertaal=geenVoorkeur&event=zoeken&source=&cursuscode=&korteNaamCursus=&collegejaar=&faculteitCursus=&aanvangsblok=


	requestParams = {
		'startUrl':'StartPagina.do',
		'inPortal':'',
		'callDirect':'',
		'requestToken':'iamrequesttokenyes?',
		'jaar_1':'2016',
		'zoek':'',
		'zoek_uitgebreid':'J',
		'toon':'',
		'toon':'Cursus',
		'toon':'Toetsen',
		'aanvangs_blok':'',
		'timeslot':'geenVoorkeur',
		'categorie':'geenVoorkeur',
		'cursustype':'geenVoorkeur',
		'faculteit':'geenVoorkeur',
		'organisatieonderdeel':'geenVoorkeur',
		'docent':'',
		'bijvakker':'geenVoorkeur',
		'voertaal':'geenVoorkeur',
		'event':'zoeken',
		'source':'',
		'cursuscode':'',
		'korteNaamCursus':'',
		'collegejaar':'',
		'faculteitCursus':'',
		'aanvangsblok':'',
	}



	# event=goto&source=OnderwijsZoekCursus&value=0&size=200


	connection  = httplib.HTTPSConnection("www.osiris.universiteitutrecht.nl")


	token,cookies = getAuth(conn = connection)
	print 'requestToken:', token
	#print 'cookie:', cookies

	requestParams['requestToken']=token
	#print urllib.urlencode(requestParams)

	minedSuccesfully=False

	i=0
	while i<5 and not minedSuccesfully:
		print ""
		print "Attempt:",i+1

		resp = sendRequest('POST',params=urllib.urlencode(requestParams),cookie=cookies, conn = connection)
		data = resp.read()

		if resp.status!=200:
			print resp.status,resp.reason
			print resp.getheaders()
		else:
			print 'received',str(len(data)),"bytes"

		resp.close()

		minedSuccesfully=mineSucces(data)
		i+=1
		print "Succes:",minedSuccesfully


	#f1 = open('tmp2','w')
	#f1.write(data)
	#f1.close()