#!/usr/bin/env python2

from time import strftime, gmtime
import urllib,json,argparse,os,sys,cmd,signal,time

from instaminer import InstaMiner

try:
	import colorama
	from colorama import Fore, Back, Style
except ImportError:
	print "Please install colorama for python before continuing."
	print "Official link: https://pypi.python.org/pypi/colorama"
	sys.exit(0)

colorama.init(autoreset=True)

class Console(cmd.Cmd,object):

	""" SCREEN BUFFER """

	def _buffer_start(self):
		print "\033[?1049h\033[H"
	def _buffer_quit(self):
		print "\033[?1049l"


	""" INITIALISATION """

	intro='hOI'
	#outro="\033[1A\033[8GBye ;)\033[1A"
	outro="\033[2A\033[2K\033[1A"

	def start(self):

		### IMPORTS

		self.instaminer = InstaMiner()
		self.time=__import__('time')
		self.json=__import__('json')
		self.re=__import__('re')


		### INTRO ART

		rows, columns = os.popen('stty size', 'r').read().split()

		asci = ""
		f = open('assets/logo.txt','r')
		logoArt = f.read()
		f.close()
		for line in logoArt.split('\n'):
			#asci=asci+'\n'+' '*(int(0.5*int(columns) )-int(0.5*len(line)))+line
			asci=asci+'\n'+Fore.YELLOW+' '*24+line
		asci+='\n'
		asci+='\n'+' '*(int(0.5*int(columns) )-int(0.5*len('InstaMiner')))+'InstaMiner'
		asci+='\n'+' '*(int(0.5*int(columns) )-int(0.5*len('v'+self.instaminer.v)))+'v'+self.instaminer.v
		asci+='\n\n'+' '*(int(0.5*int(columns) )-int(0.5*len('Type "help" for help')))+'Type "help" for help'

		self.intro=asci

		### INIT

		self._buffer_start()
		self.cmdloop()

	""" CMD HOOKS """

	def emptyline(self):
		pass

	def precmd(self, line):
		ls = line.split(';')
		self.cmdqueue+=ls[1:]
		line=ls[0]

		while line.startswith(' '):
			line=line[1:]

		alias_parsed = self.parse_alias(line)
		return alias_parsed

	def postcmd(self,stop,line):
		## Method for printing to the terminal or piping to the next function
		# TODO
		return stop

	""" COMMANDS """

	def do_echo(self,arg):
		print arg
		return 0

	def do_clear(self,arg):
		print "\033[2J"

	def do_regex(self,arg):
		print self.instaminer.regex

	def do_exit(self):
		sys.exit()

	def do_mine(self, arg):
		if arg=='':
			try:
				assert self.instaminer.location!='','location not set'
			except AssertionError:
				print "Error: missing argument <location>"
				return 0
		args=arg.split(' ')
		try:
			assert len(args)<=2
		except AssertionError:
			print "Error: too many arguments"
			return 0
		for argi in args:
			if self.instaminer.match_location(argi): # if it is in the format of /letter/word
				self.instaminer.location=argi
			elif "/" in argi or '@' in argi or '#' in argi:
				print "Error: incorrect location format"
				return 0
			else:
				self.instaminer.stype=argi

		## From here on out we assume all inputs to have been properly processed and deemed correct

		try:
			result = self.instaminer.mine()
		except KeyboardInterrupt:
			print "Mining operation canceled"

		print "Job stopped"


	""" ALIASES """

	aliases = {'e':'echo','m':'mine','q':'exit'}

	def alias_replace(self,matchobj):
		if matchobj.group('alias') is not None:
			try:
				return self.aliases[matchobj.group('alias')]+" "+matchobj.group('arg')
			except IndexError:
				return matchobj.group(0)
		else:
			return matchobj.group(0)

	def parse_alias(self,line):
		ls = []
		for a in self.aliases:
			ls.append(a)

		aa = "|".join(ls)
		regex = ur"^(?P<alias>"+aa+ur")(\s(?P<arg>.*))?$" #starts and ends with alias, or starts with alias followed by space then arg
		match = self.re.search(regex,line)
		if match:
			line = self.re.sub(regex, self.alias_replace, line)
		else:
			pass

		return line



if __name__=='__main__':
	console=Console()
	try:
		console.start()
	except KeyboardInterrupt, SystemExit:
		pass
	finally:
		console._buffer_quit()
		print console.outro
		#time.sleep(1)
		sys.exit(0)


