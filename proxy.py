# -*- coding: utf-8 -*-

from urllib import request
from random import choice
from time import sleep
from bs4 import BeautifulSoup

class proxy(object):
    proxyUrls = ['http://www.xicidaili.com/']
    testUrl = 'http://icanhazip.com/'
    proxyList = []
    checking = False

    def __getProxy(self):
        if self.checking == True:
            print('Checking, please wait')
            sleep(60)
            return
        self.checking = True
        headers = {}
        unCheckproxyList = []
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
        for proxyUrl in self.proxyUrls:
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
                try:
                    port = int(ipInfo.find_all('td')[2].get_text())
                except ValueError:
                    continue

                proxy = '%s:%d' % (ip, port)
                unCheckproxyList.append(proxy)
        print("unCheckProxy:%d" % len(unCheckproxyList))
        self.checkProxy(unCheckproxyList)

    def startGetProxy(self):
        self.__getProxy()


    def checkProxy(self, proxyList):
        for proxy in proxyList:
            choiceProxy = {'http': proxy}
            proxy_support = request.ProxyHandler(choiceProxy)
            opener = request.build_opener(proxy_support)
            request.install_opener(opener)
            try:
                #response = request.urlopen(self.testUrl, timeout=3)
                response = request.urlopen(self.testUrl, timeout=5)
            except:
                print('%s proxy can not use, continue' % proxy)
                continue
            ip = proxy.split(':')[0]
            content = response.read()
            content = content.decode('utf8')
            content = content.strip('\n')
            print('content:%s, ip:%s' % (content, ip))
            if content == ip:
                self.proxyList.append(proxy)
        self.checking = False
        if len(self.proxyList) == 0:
            sleep(60)
            self.__getProxy()
            return
        print('Length:%d' % len(self.proxyList))

    def randomChoice(self):
        # if len(self.proxyList) == 0:
        #     self.__getProxy()
        #     return self.randomChoice()
        # return choice(self.proxyList)

        try:
            return choice(self.proxyList)
        except IndexError:
            self.__getProxy()
            return self.randomChoice()

    def removeProxy(self, aproxy):
        try:
            self.proxyList.remove(aproxy)
        except ValueError:
            print('alread removed, ignore')


if __name__ == "__main__":
    ipProxy = proxy()
    ipProxy.startGetProxy()
    aproxy = ipProxy.randomChoice()
    print('proxy:', aproxy)

    #proxies = {'http' : '115.183.11.158:9999'}
    #url = 'http://icanhazip.com/'
    #proxy_support = request.ProxyHandler(proxies)
    #opener = request.build_opener(proxy_support)
    #request.install_opener(opener)
    #response = request.urlopen(url)
    #print(response.read())
