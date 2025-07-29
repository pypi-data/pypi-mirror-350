g_MAPI_key = "eyJ1ciI6ImtqdzMzODciLCJwZyI6ImNpdmlsIiwiY24iOiJsd0ozVU43YlFnIn0.ece204694bd5d77ac5c3dd8d0323f409028d44bd3a2f31ebcecce44da5d5bf36"
g_base_uri = "moa-engineers.midasit.com"
g_base_port = "443"

import requests
from enum import Enum

class midas_util:
	@staticmethod
	def ERROR_DICT(prefix='', message='', postfix=''):
		return {"error": f"Error: {prefix} {message if message != '' else 'request is failed...'} {postfix}"}

	def is_json(text):
		text = text.strip()
		return text.startswith('{') and text.endswith('}') or text.startswith('[') and text.endswith(']')

	def response_handler(response):
		if (midas_util.is_json(response.text)):
			return response.json()
		else:
			return midas_util.ERROR_DICT(postfix=response.url)

	def get_base_url(product, country="KR"):
		return f"https://{g_base_uri}:{g_base_port}/civil"


	def get_MAPI_Key(product, country="KR"):
		return g_MAPI_key


	def post(url, headers, json):
		try:
			response = requests.post(url, headers=headers, json=json)
			return midas_util.response_handler(response)
		except requests.exceptions.RequestException as e:
			return midas_util.ERROR_DICT(postfix=url)


	def get(url, headers):
		try:
			response = requests.get(url, headers=headers)
			return midas_util.response_handler(response)
		except requests.exceptions.RequestException as e:
			return midas_util.ERROR_DICT(postfix=url)


	def put(url, headers, json):
		try:
			response = requests.put(url, headers=headers, json=json)
			return midas_util.response_handler(response)
		except requests.exceptions.RequestException as e:
			return midas_util.ERROR_DICT(postfix=url)


	def delete(url, headers):
		try:
			response = requests.delete(url, headers=headers)
			return midas_util.response_handler(response)
		except requests.exceptions.RequestException as e:
			return midas_util.ERROR_DICT(postfix=url)


class Product(Enum):
    CIVIL = 1,
    GEN = 2,
