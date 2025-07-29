from random import choice
if not __name__ == '__main__':
	amuesmmodule = []
	amuesmmodule2 = []
	amuesmmodule3 = ['']
	def createpass(charset, len):
		amuesmmodule.clear()
		for _ in range(len):
			amuesmmodule.append(choice(charset))
		return ''.join(amuesmmodule)
		amuesmmodule.clear()
	def en(str, charset):
		amuesmmodule.clear()
		amuesmmodule2.clear()
		for char in str:
			for _ in range(charset.index(char) + 1):
				amuesmmodule2.append('-')
			amuesmmodule.append(''.join(amuesmmodule2))
			amuesmmodule2.clear()
		return ' '.join(amuesmmodule)
		amuesmmodule.clear()
	def de(str, charset):
		amuesmmodule.clear()
		global amuesmmodule3
		amuesmmodule3.clear()
		amuesmmodule3 = str.split(' ')
		for encline in amuesmmodule3:
			amuesmmodule.append(charset[len(encline) - 1])
		amuesmmodule3.clear()
		return ''.join(amuesmmodule)
		amuesmmodule.clear()
	def amuesmcredits():
		print('Created with amuesm Developed by AnniePrograms! Download at https://pypi.org/project/amuesm/')
