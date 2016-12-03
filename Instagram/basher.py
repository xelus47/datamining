#!/usr/bin/env python2

#E:\ggearoce\client side data mining\instagram people by location\hack\saved
from instaclass import Instaclass
from time import strftime, gmtime
import urllib,json,argparse,os, sys


from retrieve import *


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Instagram miner')
	parser.add_argument('destination', help='/{username}/ or /explore/tags/{tag}/ or /p/{id} or /explore/location/{location id}',type=str,default='/nederland/')
	parser.add_argument('--debug',help='Show a lot more stuff in terminal',type=int, default=0)
	parser.add_argument('-d','--depth',help='The "depth" of mining (default=0)',type=int, default=0)
	parser.add_argument('-w','--width',help='Will fully mine up until this depth level (default=0)',type=int, default=0)
	parser.add_argument('-dw','--depthwidth',help='Depth and width in one arg (default=0,0)',type=str, default="0,0")
	parser.add_argument('-n','--nodes',help='Number of nodes to save if this level is mined (default=-1 (all))',type=int, default=-1)
	args = parser.parse_args()

	pageDat = downloadPage(args.destination) # returns unprocessed JSON object

	pageJSON = parsePage(pageDat) # convert raw JSON into properly formatted JSON with useful info

	print pageJSON.type # print what type of page it is (user, hashtag, location, post)
	print pageJSON.summary()



	sys.exit()

