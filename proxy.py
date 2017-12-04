# -*- coding: utf-8 -*-

from urllib import request
from random import choice
from bs4 import BeautifulSoup

class proxy(object):
	proxyUrls = ['http://www.xicidaili.com/']
	testUrl = 'http://icanhazip.com/'
	proxyList = []

	def __getProxy(self):
		headers = {}
		unCheckproxyList = []
		headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
		for proxyUrl in proxyUrls:
			try:
				req = request.Request(proxyUrl, headers=headers)
				res = request.urlopen(req, timeout=3)
			except:
				print('Can not open %s, removed' % proxyUrl)
				self.proxyUrls.remove(proxyUrl)
				continue
			content = res.read()
			soup = BeautifulSoup(content, "lxml")
			ipInfoList = soup.find_all('tr', attrs={'class':'odd'})
			for ipInfo in ipInfoList:
				proxyType = ipInfo.find_all('td')[4].get_text()
				if proxyType != '透明':
					continue
				httpType = ipInfo.find_all('td')[5].get_text()
				if httpType != 'HTTP':
					continue

				ip = ipInfo.find_all('td')[1].get_text()
				try 
					port = int(ipInfo.find_all('td')[2].get_text())
				except ValueError:
					continue

				proxy = '%s:%d' % (ip, port)
				unCheckproxyList.append(proxy)
				self.checkProxy(unCheckproxyList)

	def startGetProxy(self):
		self.__getProxy()


	def checkProxy(self, proxyList):
		url = 'http://icanhazip.com/'
		for proxy in proxyList:
			choiceProxy = {'http': proxy}
			proxy_support = request.ProxyHandler(choiceProxy)
			opener = request.build_opener(proxy_support)
			request.install_opener(opener)
			try:
				response = request.urlopen(url, timeout=3)
			except:
				continue
			ip = proxy.split(':')[0]
			content = response.read()
			content = content.decode('utf8')
			content = content.strip('\n')
			if content == ip:
				self.proxyList.append(proxy)

		print('Length:%d' % len(self.proxyList))

	def randomChoice(self):
		return choice(self.proxyList)


if __name__ == "__main__":
	ipProxy = proxy()
	aproxy = ipProxy.randomChoice()
	print('proxy:', aproxy)
	# proxies = {'http' : '222.222.169.60:53281'}
	# url = 'http://icanhazip.com/'
	# proxy_support = request.ProxyHandler(proxies)
	# opener = request.build_opener(proxy_support)
	# request.install_opener(opener)
	# response = request.urlopen(url)
	# print(response.read())