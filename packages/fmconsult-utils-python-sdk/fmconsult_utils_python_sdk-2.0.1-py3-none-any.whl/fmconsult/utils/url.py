from urllib.parse import parse_qs

class UrlUtil(object):
	def make_url(self, base_url, paths):
		url = base_url
		for path in paths:
			url = url +'/'+ str(path)
		return url

	def url_parse(self, query_string):
		url_params = {}
		url_params['params'] = parse_qs(query_string)

		params = url_params.copy()

		for key, value in url_params['params'].items():
			if key == 'offset':
				params['offset'] = int(value[0])
			elif key == 'limit':
				params['limit'] = int(value[0])
			else:
				params['params'][key] = value[0]

		if 'offset' in params['params']:
			del params['params']['offset']
		
		if 'limit' in params['params']:
			del params['params']['limit']

		return params