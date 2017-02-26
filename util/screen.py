class PrintStyle:
	blue = { 'b': '\033[1;34m','e': '\033[1;m'}
	magenta = { 'b': '\033[1;35m', 'e': '\033[1;m'}
	cyan = { 'b': '\033[1;36m','e': '\033[1;m'}
	red = { 'b': '\033[1;31m','e': '\033[1;m'}
	yellow = { 'b': '\033[1;33m','e': '\033[1;m'}
	def colorWithBlue(c):
		print '{0}{1}{2}'.format(self.blue['b'], c, self.blue['e'])

	def colorWithYellow(c):
		print '{0}{1}{2}'.format(self.yellow['b'], c, self.yellow['e'])

prompts = {}

def logo():
	print "\033[1;34m       __                                           \033[1;m"
	print "\033[1;34m  ____/ /___   ___   ____   \033[1;32m_____ _____ ____ _ ____ \033[1;m"
	print "\033[1;34m / __  // _ \ / _ \ / __ \ \033[1;32m/ ___// ___// __ `// __ \\\033[1;m"
	print "\033[1;34m/ /_/ //  __//  __// /_/ /\033[1;32m(__  )/ /__ / /_/ // / / /\033[1;m"
	print "\033[1;34m\__,_/ \___/ \___// .___/\033[1;32m/____/ \___/ \__,_//_/ /_/ \033[1;m"
	print "\033[1;34m                 /_/                                \033[1;m"

def greeting():
	logo()
	printWithCondiment("Welcome to Deepscan, please answer the following questions in order to proceed:", PrintStyle.red)

def printWithCondiment(content, style):
	print '{0}{1}{2}'.format(content, style['b'], style['e'])
