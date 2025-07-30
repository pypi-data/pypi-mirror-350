class CPFUtil:

	def format( self, cpf ):
		return "%s.%s.%s-%s" % ( cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11] )

	def validate(self,cpf):
		cpf_invalidos = [11*str(i) for i in range(10)]
		if cpf in cpf_invalidos:
			return False
		if not cpf.isdigit():
			cpf = cpf.replace(".", "")
			cpf = cpf.replace("-", "")
		if len(cpf) < 11:
			return False
		if len(cpf) > 11:
			return False
		selfcpf = [int(x) for x in cpf]
		cpf = selfcpf[:9]
		while len(cpf) < 11:
			r =  sum([(len(cpf)+1-i)*v for i, v in [(x, cpf[x]) for x in range(len(cpf))]]) % 11
			if r > 1:
				f = 11 - r
			else:
				f = 0
			cpf.append(f)
			
		return bool(cpf == selfcpf)