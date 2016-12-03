#!/usr/bin/env python2

#E:\ggearoce\client side data mining\instagram people by location\hack\saved
from instaclass import Instaclass
from time import strftime, gmtime
import urllib,json,argparse,os

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='InstaPwn/Bash an instagram user')
	parser.add_argument('destination', help='/username/ or /explore/tags/tag/ or /p/id or (...)')
	parser.add_argument('-t','--test',help='test the destination and connection',action='count')
	parser.add_argument('--cache',help='disables nocache mode (lighter load)',action='count')
	parser.add_argument('--download',help='if enabled, will download images it encounters',action='count')
	parser.add_argument('--complete',help='will keep looping until not "has_next_page"',action='count')
	#parser.add_argument('-o','--output',help='Name the output file (defaults to <filename>.com)')
	args = parser.parse_args()

	insta=Instaclass()
	#insta.nocache=bool(args.nocache)
	insta.imagedl=bool(args.download)
	insta.complete=bool(args.complete)
	if not insta.complete:
		insta.nocache=not bool(args.cache)
	destination=args.destination
	if destination=='@d':
		destination='/guusvogel/'

	if bool(args.test):
		result = insta.test(destination)
		print result['http'],result['hacked']
	else:
		insta.bash(destination)
