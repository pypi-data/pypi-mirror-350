class StringUtil(object):
  
	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

	def get_encoded_value(self, value):
		return str(value).decode('cp1252').encode('utf-8')

	def custom_serializer(self, obj):
		if isinstance(obj, ImportModel):
			return obj.__dict__
		else:
			return None

	def to_dict(self, input_ordered_dict):
		return loads(dumps(input_ordered_dict, default=self.custom_serializer))
	
	def str2bool(self, value):
		return str(value).lower() in ("yes", "true", "t", "1")
	
	def isBoolValue(self, value):
		return str(value).lower() in ("yes", "false", "true", "t", "f", "1", "0")

	def convert_aba_track_to_serial(self, aba_track_code):
		return hex(aba_track_code)

	def convert_serial_to_wiegand(self, serial_code):
		# separando os bytes
		_p1 = serial_code[-4:]
		_p2 = serial_code[:(len(serial_code)-4)][-4:]
		# convertendo os bytes p/ decimal
		_p1int = int(_p1, 16)
		_p2int = int(_p2, 16)    
		# formatando a saida
		_p2str = f'{_p2int:03}'
		wiegand_code = '{b2}-{b1}'.format(b1=_p1int, b2=_p2str)
		return wiegand_code

	def convert_wiegand_to_serial(self, wiegand_code):
		_wiegand_code = str(wiegand_code).split('-')
		
		_b1_hex = hex(int(_wiegand_code[0]))
		_b2_hex = hex(int(_wiegand_code[1]))[-4:]

		return '{b1}{b2}'.format(b1=_b1_hex, b2=_b2_hex)

	def convert_decimal_to_wiegand(self, decimal_code):
		return self.convert_serial_to_wiegand(hex(decimal_code))

	def reverse_decimal_from_hexcode(self, decimal_code):
		hex_code = hex(int(decimal_code)).replace('0x', '')
		p1 = hex_code[0:2]
		p2 = hex_code[2:4]
		p3 = hex_code[4:6]
		p4 = hex_code[6:8]
		inverse_hex_code = '{p4}{p3}{p2}{p1}'.format(p4=p4, p3=p3, p2=p2, p1=p1)
		inverse_dec_code = int(inverse_hex_code, 16)
		return inverse_dec_code