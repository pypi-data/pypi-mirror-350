import os
import asyncio
import aiohttp
from aiohttp import FormData
import json
from appPublic.myTE import MyTemplateEngine
import re
from appPublic.log import info, debug, warning, error, exception, critical
from urllib.parse import urlparse
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

def get_domain(url):
	# Prepend 'http://' if the URL lacks a scheme
	if not url.startswith(('http://', 'https://')):
		url = 'http://' + url
	parsed_url = urlparse(url)
	netloc = parsed_url.netloc
	domain = netloc.split(':')[0]
	return domain

RESPONSE_BIN = 0
RESPONSE_TEXT = 1
RESPONSE_JSON = 2
RESPONSE_FILE = 3
RESPONSE_STREAM = 4

class HttpError(Exception):
	def __init__(self, code, msg, *args, **kw):
		super().__init__(*msg, **kw)
		self.code = code
		self.msg = msg
	def __str__(self):
		return f"Error Code:{self.code}, {self.msg}"
	
	def __expr__(self):
		return str(self)
	
class HttpClient:
	def __init__(self,coding='utf-8', socks5_proxy_url=None):
		self.coding = coding
		self.session = None
		self.cookies = {}
		self.proxy_connector = None
		self.socks5_proxy_url = socks5_proxy_url
		self.blocked_domains = set()
		self.load_cache()

	def save_cache(self):
		home_dir = os.path.expanduser('~')
		cache_file = os.path.join(home_dir, '.proxytarget')
		with open(cache_file, 'w') as f:
			for d in self.blocked_domains:
				f.write(f'{d}\n')

	def load_cache(self):
		# 初始化缓存文件
		home_dir = os.path.expanduser('~')
		cache_file = os.path.join(home_dir, '.proxytarget')
		
		try:
			with open(cache_file, 'r') as f:
				for line in f:
					domain = line.strip()
					if domain:
						self.blocked_domains.add(domain)
		except FileNotFoundError:
			# 创建空文件
			with open(cache_file, 'w') as f:
				pass

	async def close(self):
		if self.session:
			await self.session.close()
			self.session = None

	def setCookie(self,url,cookies):
		name = get_domain(url)
		self.cookies[name] = cookies

	def getCookies(self,url):
		name = get_domain(url)
		return self.cookies.get(name,None)

	def getsession(self,url):
		if self.session is None:
			jar = aiohttp.CookieJar(unsafe=True)
			self.session = aiohttp.ClientSession(cookie_jar=jar)
		return self.session
				
	async def handleResp(self,url,resp,resp_type, stream_func=None):
		if resp.cookies is not None:
			self.setCookie(url,resp.cookies)

		if resp_type == RESPONSE_BIN:
			return await resp.read()
		if resp_type == RESPONSE_JSON:
			return await resp.json()
		if resp_type == RESPONSE_TEXT:
			return await resp.text(self.coding)
		async for chunk in resp.content.iter_chunked(1024):
			if stream_func:
				await stream_func(chunk)

	def grapCookie(self,url):
		session = self.getsession(url)
		domain = get_domain(url)
		filtered = session.cookie_jar.filter_cookies(domain)
		return filtered

	async def make_request(self, url, method='GET', 
							response_type=RESPONSE_TEXT,
							params=None, 
							data=None,
							jd=None,
							stream_func=None,
							headers=None, 
							use_proxy=False
							):
		connector = None
		if use_proxy:
			connector = ProxyConnector.from_url(self.socks5_proxy_url)
		async with aiohttp.ClientSession(connector=connector) as session:
			if params == {}:
				params = None
			if data == {}:
				data = None
			if jd == {}:
				jd = None

			if headers == {}:
				headers = None

			resp = await session.request(method, url, 
						params=params,
						data=data,
						json=jd,
						headers=headers)
			if resp.status==200:
				return await self.handleResp(url, resp, response_type, stream_func=stream_func)
			msg = f'http error({resp.status}, {url=},{params=}, {data=}, {jd=})'
			exception(msg)
			raise HttpError(resp.status, msg)

	async def request(self, url, method='GET',
							response_type=RESPONSE_TEXT,
							params=None,
							data=None,
							jd=None,
							stream_func=None,
							headers=None,
							**kw
			):
		if self.socks5_proxy_url is None:
			resp = await self.make_request(url, method=method, 
										response_type=response_type,
										params=params,
										data=data,
										jd=jd,
										use_proxy=False,
										stream_func=stream_func,
										headers=headers
										)
			return resp
		domain = get_domain(url)
		if domain not in self.blocked_domains:
			try:
				resp = await self.make_request(url, method=method, 
										response_type=response_type,
										params=params,
										data=data,
										jd=jd,
										use_proxy=False,
										stream_func=stream_func,
										headers=headers
										)
				return resp
			except:
				if domain not in self.blocked_domains:
					self.blocked_domains.add(domain)
					self.save_cache()
		resp = await self.make_request(url, method=method, 
										response_type=response_type,
										params=params,
										data=data,
										jd=jd,
										use_proxy=True,
										stream_func=stream_func,
										headers=headers
										)
		return resp
			
	async def get(self,url,**kw):
		return self.request(url, 'GET', **kw)

	async def post(self,url, **kw):
		return self.request(url, 'POST', **kw)
		session = self.getsession(url)

class JsonHttpAPI:
	def __init__(self, env={}, socks5_proxy_url=None):
		self.env = env
		self.te = MyTemplateEngine([], env=env)
		self.hc = HttpClient(socks5_proxy_url=socks5_proxy_url)

	async def call(self, url, method='GET', ns={}, 
					stream_func=None,
					headerstmpl=None, 
					paramstmpl=None,
					datatmpl=None,
					resptmpl=None):
		headers = None
		ns1 = self.env.copy()
		ns1.update(ns)
		if headerstmpl:
			headers = json.loads(self.te.renders(headerstmpl, ns1))
			info(f'{headers=},{ns=}, {headerstmpl=}')
		params = None
		if paramstmpl:
			params = json.loads(self.te.renders(paramstmpl, ns1))
		data = None
		if datatmpl:
			datadic = json.loads(self.te.renders(datatmpl, ns1))
			data = FormData()
			for k,v in datadic.items():
				data.add_field(k, v)

			info(f'{data=},{ns=}, {datatmpl=}')
		resp = await self.hc.request(url, method=method, headers=headers,
						response_type=None,
						stream_func=stream_func,
						params=params,
						data=data)
		ret = resp
		if resptmpl:
			ns1 = self.env.copy()
			ns1.update(resp)
			rets = self.te.renders(resptmpl, ns1)
			ret = json.loads(rets)
		return ret

if __name__ == '__main__':
	async def main():
		hc = HttpClient(socks5_proxy_url='socks5://localhost:1086')
		r = await hc.request('https://www.baidu.com')
		print(r)
		r = await hc.request('https://www.google.com')
		print(r)
		await hc.close()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

