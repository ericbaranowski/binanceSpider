# -*- coding: utf-8 -*-

import common
from re import compile
from json import loads
# from socket import timeout
from urllib import request
from random import choice
from time import sleep
from bs4 import BeautifulSoup


class proxy(object):
    proxyUrls = {'ip3366':'http://www.ip3366.net/free/?stype=2', 'xici':'http://www.xicidaili.com/', '89ip':'http://www.89ip.cn/tiqv.php?sxb=&tqsl=30&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1', 'xdaili':'http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10', 'kuaidaili':'http://www.kuaidaili.com/free/intr/', 'cnproxy':'http://cn-proxy.com/'}
    #proxyUrls = {'ip3366':'http://www.ip3366.net/free/?stype=2'}
    testUrl = 'http://icanhazip.com/'
    proxyDict = {}
    checking = False

    def __getSpecifyUrl(self, webSite, url):
        headers = {}
        ipDict = {}
        headers['user-agent'] = common.getRandomUserAgents('PC')
        if webSite == 'kuaidaili':
            headers = common.getRandomHeaders('kuaidaili', 'PC')
            
        try:
            req = request.Request(url, headers=headers)
            res = request.urlopen(req, timeout=3)
        except Exception as e:
            print('%s error happend when open %s with %s user_agent' % (e, url, headers))
            return ipDict

        content = res.read()
        soup = BeautifulSoup(content, "lxml")
        if webSite == 'xici':
            ipInfoList = soup.find_all('tr', attrs={'class':'odd'})
            for ipInfo in ipInfoList:
                proxyType = ipInfo.find_all('td')[4].get_text()
                if proxyType != '透明':
                    continue
                httpType = ipInfo.find_all('td')[5].get_text()
                # if httpType != 'HTTP':
                #     continue
                ip = ipInfo.find_all('td')[1].get_text()
                try:
                    port = int(ipInfo.find_all('td')[2].get_text())
                except ValueError:
                    continue
                proxy = '%s:%d' % (ip, port)
                ipDict[proxy] = httpType

        elif webSite == 'ip3366':
            print('go to ip3366')
            divTag = soup.find_all('div', attrs={'id':'list', 'style':'margin-top:15px;'})[0]
            trResult = divTag.find_all('tr')
            for tr in trResult:
                try:
                    ip = tr.find_all('td')[0].get_text()
                    port = tr.find_all('td')[1].get_text()
                    port = int(port)
                    httpType = tr.find_all('td')[3].get_text()
                except (IndexError, ValueError):
                    continue
                proxy = '%s:%d' % (ip, port)
                ipDict[proxy] = httpType

        elif webSite == "cnproxy":
            print('go to cnproxy')
            tbodyResult = soup.find_all('tbody')
            for tbody in tbodyResult:
                trResult = tbody.find_all('tr')
                for tr in trResult:
                    try:
                        ip = tr.find_all('td')[0].get_text()
                        port = int(tr.find_all('td')[1].get_text())
                    except (IndexError, ValueError):
                        continue
                    proxy = '%s:%d' % (ip, port)
                    ipDict[proxy] = 'http'

        elif webSite == '89ip':
            print('go to 89ip')
            proxyPat = compile(r'(\d+\.\d+\.\d+\.\d+:\d+)')
            fixedContent = soup.prettify()
            lines = fixedContent.split('\n')
            for line in lines:
                line = line.strip(' ')
                match = proxyPat.match(line)
                if not match:
                    continue
                proxy = match.group(0)
                ipDict[proxy] = 'http'

        elif webSite == 'xdaili':
            content = content.decode('utf8')
            jsonContent = loads(content)
            ipProxies = jsonContent['RESULT']['rows']
            for ipProxy in ipProxies:
                ip = ipProxy['ip']
                try:
                    port = int(ipProxy['port'])
                except ValueError:
                    continue
                proxy = '%s:%d' % (ip, port)
                ipDict[proxy] = 'http'

        elif webSite == 'kuaidaili':
            unGzipContent = common.gunzip_bytes_obj(content)
            soup = BeautifulSoup(unGzipContent, "lxml")
            divResult = soup.find_all('div', attrs={'id':'list', 'style':'margin-top:15px;'})
            divTag = divResult[0]
            trResult = divTag.find_all('tr')
            for tr in trResult:
                try:
                    ip = tr.find_all('td')[0].get_text()
                    port = int(tr.find_all('td')[1].get_text())
                    httpType = tr.find_all('td')[3].get_text()
                except (ValueError, IndexError):
                    continue
                proxy = '%s:%d' % (ip, port)
                ipDict[proxy] = httpType

        #print('allUncheckProxy:', ipDict)
        return ipDict

    def __getProxy(self):
        if self.checking == True:
            print('Checking, please wait')
            sleep(60)
            return
        self.checking = True
        unCheckProxyDict = {}
        for key, value in self.proxyUrls.items():
            # tmpProxyDict = self.__getSpecifyUrl(key, value)
            unCheckProxyDict = dict(unCheckProxyDict, **self.__getSpecifyUrl(key, value))

        #print('unCheckProxyDict:', len(unCheckProxyDict))
        self.checkProxy(unCheckProxyDict)

    def startGetProxy(self):
        self.__getProxy()


    def checkProxy(self, proxyDict):
        for proxy, httpType in proxyDict.items():
            choiceProxy = {httpType.lower(): proxy}
            #print('choiceProxy:', choiceProxy)
            proxy_support = request.ProxyHandler(choiceProxy)
            opener = request.build_opener(proxy_support)
            request.install_opener(opener)
            try:
                #response = request.urlopen(self.testUrl, timeout=3)
                response = request.urlopen(self.testUrl, timeout=5)
                content = response.read()
            except Exception as e:
                print('Error happened:%s. proxy %s:%s can not be used, continue' % (e, httpType, proxy))
                continue
            ip = proxy.split(':')[0]
            content = content.decode('utf8')
            content = content.strip('\n')
            #print('content:%s, ip:%s' % (content, ip))
            if content == ip:
                self.proxyDict[proxy] = httpType
        self.checking = False
        #print('Length:%d' % len(self.proxyDict))

    def randomChoice(self):
        try:
            return choice(list(self.proxyDict.items()))
        except IndexError:
            return

    def removeProxy(self, aproxy):
        try:
            self.proxyDict.pop(aproxy)
        except KeyError:
            print('alread removed, ignore')
        return

    def showAllProxy(self):
        return self.proxyDict


#if __name__ == "__main__":
#    ipProxy = proxy()
#    ipProxy.startGetProxy()
#    ipProxy.showAllProxy()

    # aproxy = ipProxy.randomChoice()
    # print('proxy:', aproxy)

    #proxies = {'http' : '115.183.11.158:9999'}
    #url = 'http://icanhazip.com/'
    #proxy_support = request.ProxyHandler(proxies)
    #opener = request.build_opener(proxy_support)
    #request.install_opener(opener)
    #response = request.urlopen(url)
    #print(response.read())
