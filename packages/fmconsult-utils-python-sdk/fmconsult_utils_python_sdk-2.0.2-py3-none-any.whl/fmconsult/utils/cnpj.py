import re

class CNPJUtil:
	def __init__( self ):
		pass

	def validate(self, cnpj):
		cnpj = ''.join(re.findall('\d', str(cnpj)))

		if (not cnpj) or (len(cnpj) < 14):
			return False

		inteiros = map(int, cnpj)
		novo = inteiros[:12]
		prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

		while len(novo) < 14:
			r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
			if r > 1:
				f = 11 - r
			else:
				f = 0
				novo.append(f)
				prod.insert(0, 6)

		if novo == inteiros:
			return cnpj

		return False