# default Setting
g_MAPI_key = ""
g_base_uri = "moa-engineers.midasit.com"
g_base_port = "443"

# from web FE, Set & Get
def set_g_values(g_values):
	_g_values = json.loads(g_values)
	global g_MAPI_key
	global g_base_uri
	global g_base_port
	g_MAPI_key = _g_values['g_mapi_key']
	g_base_uri = _g_values['g_base_uri']
	g_base_port = _g_values['g_base_port']
  
def get_g_values():
  return json.dumps({
		'g_mapi_key': g_MAPI_key,
		'g_base_uri': g_base_uri,
		'g_base_port': g_base_port
	})
  
# from javascript import globalThis
# fetch = globalThis.fetch
# JSON = globalThis.JSON
from js import fetch, JSON, XMLHttpRequest
import json
import numpy as np

class utils:
    @staticmethod
    def ERROR_DICT(prefix = '', message = '', postfix = ''):
      return { "error": f"Error: {prefix} {message if message != '' else 'request is failed...'} {postfix}" }

    def is_json(text):
      text = text.strip()
      return text.startswith('{') and text.endswith('}') or text.startswith('[') and text.endswith(']')
            
    def response_handler(xhr):
      if (utils.is_json(xhr.responseText)):
        return json.loads(xhr.responseText)
      else: 
        return utils.ERROR_DICT(postfix=xhr.responseURL)

class requests_json:
    @staticmethod
    def post(url, headers, jsonObj):
      try:
        xhr = XMLHttpRequest.new()
        xhr.open("POST", url, False)
        for key, value in headers.items():
            xhr.setRequestHeader(key, value)
        xhr.send(json.dumps(jsonObj))
        return utils.response_handler(xhr)
      except:
        return utils.ERROR_DICT(postfix=url)

    def get(url, headers):
      try:
        xhr = XMLHttpRequest.new()
        xhr.open("GET", url, False)
        for key, value in headers.items():
            xhr.setRequestHeader(key, value)
        xhr.send()
        return utils.response_handler(xhr)
      except:
        return utils.ERROR_DICT(postfix=url)
    
    def put(url, headers, jsonObj):
      try:
        xhr = XMLHttpRequest.new()
        xhr.open("PUT", url, False)
        for key, value in headers.items():
            xhr.setRequestHeader(key, value)
        xhr.send(json.dumps(jsonObj))
        return utils.response_handler(xhr)
      except:
        return utils.ERROR_DICT(postfix=url)
    
    def delete(url, headers):
      try:
        xhr = XMLHttpRequest.new()
        xhr.open("DELETE", url, False)
        for key, value in headers.items():
            xhr.setRequestHeader(key, value)
        xhr.send()
        return utils.response_handler(xhr)
      except:
        return utils.ERROR_DICT(postfix=url)

class Product:
    CIVIL = 1,
    GEN = 2,

def get_base_url(product, country="KR"):
    country_code = country.upper()
    base_url = ""
    if(product == Product.CIVIL):
        base_uri = g_base_uri
        base_port = g_base_port
        base_url = f"https://{base_uri}:{base_port}/civil"
    elif(product == Product.GEN):
        base_uri = g_base_uri
        base_port = g_base_port
        base_url = f"https://{base_uri}:{base_port}/gen"
    else:
        print(f"Error: Unable to find the registry key or value for {product}")
    return base_url

def get_MAPI_Key(product, country="KR"):
    country_code = country.upper()
    mapikey = ""
    if(product == Product.CIVIL):
        mapikey = g_MAPI_key
    elif(product == Product.GEN):
        mapikey = g_MAPI_key
    else:
        print(f"Error: Unable to find the registry key or value for {product}")
    return mapikey
