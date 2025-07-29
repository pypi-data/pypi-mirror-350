import amuesm
from os import system
def main():
	system('clear')
	print('Welcome to amuesm!\n')
	def selop():
		try:
			global opt
			opt = int(input('''Enter an Index Below:
1. Generate Password
2. Encode Text (amuesm-based)
3. Decode Text (amuesm-based)
^C. Exit
>> '''))
		except (TypeError, KeyboardInterrupt) as er:
			if er == 'TypeError':
				print('Not a Valid Index!')
				selop()
			else:
				system('clear')
				exit()
	selop()
	system('clear')
	if opt == 1:
		charset = str(input('''Enter All Characters to Support
>> '''))
		def selplen():
			global leng
			try:
				leng = int(input('''Enter Password Length
>> '''))
			except TypeError:
				print('Not a Valid Number!')
		selplen()
		print(amuesm.createpass(list(charset), leng))
	elif opt == 2:
		charset = str(input('''Enter All Characters to Support
>> '''))
		txt = str(input('''Enter Text to Encode
>> '''))
		print(amuesm.en(txt, list(charset)))
	else:
	        charset = str(input('''Enter All Characters to Support
>> '''))
	        txt = str(input('''Enter Text to Decode
>> '''))
	        print(amuesm.de(txt, list(charset)))
if __name__ == '__main__':
	main()
