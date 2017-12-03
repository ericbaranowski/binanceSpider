# -*- coding: utf-8 -*-

import ssl
import multiprocessing
from json import loads
from urllib import request
from random import choice
from time import sleep
from pymongo import MongoClient


def getAllCoin(url, headers, tradeType):
    context = ssl._create_unverified_context()
    req = request.Request(url, headers=headers)
    res = request.urlopen(req, context=context)
    body = res.read()
    body = body.decode('utf8')
    jsonBody = loads(body)
    data = jsonBody['data']
    coins = []
    for d in data:
        if d['symbol'].endswith(tradeType):
            if d['active']:
                coins.append(d['baseAsset'])

    return coins


def getAllHeaders():
    user_agents = [
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
        "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
        "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
        "Mozilla/2.02E (Win95; U)",
        "Mozilla/3.01Gold (Win95; I)",
        "Mozilla/4.8 [en] (Windows NT 5.1; U)",
        "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
        "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
        "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
        "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    ]

    baseHeaders = {'method': 'GET',
                   'path': '/api/v1/aggTrades?limit=40&symbol=ETHUSDT',
                   'scheme': 'https',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
                   'accept': '*/*',
                   'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,de;q=0.5',
                   'clienttype': 'web',
                   'cookie': 'JSESSIONID=0A17511A64F73C36CA82187791AF272D; lang=cn',
                   'lang': 'cn',
                   'referer': 'https://www.binance.com/trade.html?symbol=ETH_USDT'}

    allHeaders = []

    for user_agent in user_agents:
        headers = baseHeaders
        headers['user-agent'] = user_agent
        allHeaders.append(headers)

    return allHeaders


def getCurrentPrice(url, headers, tradeType, timestamp):
    context = ssl._create_unverified_context()
    req = request.Request(url, headers=headers)
    res = request.urlopen(req, context=context)
    body = res.read()
    body = body.decode('utf8')
    jsonBody = loads(body)
    data = jsonBody['data']


class binanceSpider(object):
    productsUrl = 'https://www.binance.com/exchange/public/product'
    tradesUrl = 'https://www.binance.com/api/v1/aggTrades?limit=%d&symbol=%s'

    
    # def __inin__(self):
    def __prepareWork(self):
        self.allHeaders = getAllHeaders()
        # setup DB
        # self.mongoClient = MongoClient("mongodb://binance:binance@127.0.0.1:27017/binancedb")
        # self.db = self.mongoClient['binancedb']
        # get related coin
        self.allTradeWithBTC = getAllCoin(self.productsUrl, choice(self.allHeaders), 'BTC')
        self.allTradeWithUSDT = getAllCoin(self.productsUrl, choice(self.allHeaders), 'USDT')

    def startGetAggTrades(self):
        self.process = []
        # self.priceWithBTCProcess = []
        # self.priceWithUSDTProcess = []
        # self.marketProcess = []
        self.__prepareWork()
        print('Start Work')
        mp = multiprocessing.Process(target=self.__getCurrentPrice, args=('BTC',))
        mp.start()
        self.process.append(mp)

        mp = multiprocessing.Process(target=self.__getCurrentPrice, args=('USDT',))
        mp.start()
        self.process.append(mp)

        for coin in self.allTradeWithUSDT:
            p = multiprocessing.Process(target=self.__getAggTrades, args=(coin, 20, 'USDT'))
            p.start()
            self.process.append(p)

        for coin in self.allTradeWithBTC:
            p = multiprocessing.Process(target=self.__getAggTrades, args=(coin, 20, 'BTC'))
            p.start()
            self.process.append(p)

        for p in self.process:
            p.join()
            
    def __getCurrentPrice(self, tradeType):
        marketType = "coinmarket" + tradeType
        mongoClient = MongoClient("mongodb://binance:binance@127.0.0.1:27017/binancedb")
        db = mongoClient['binancedb']
        market = db[marketType]
        while True:
            context = ssl._create_unverified_context()
            req = request.Request(self.productsUrl, headers=choice(self.allHeaders))
            res = request.urlopen(req, context=context)
            body = res.read()
            body = body.decode('utf8')
            jsonBody = loads(body)
            data = jsonBody['data']
            coins = []
            for d in data:
                if d['symbol'].endswith(tradeType):
                    # print('CoinName:%s, Current Price:%s' % (d['baseAsset'], d['close']))
                    # coins.append(d)
                    market.insert(d)
            
            # print("Length:%d" % len(coins))
            sleep(60)

    def __getAggTrades(self, coin, limit, tradeType):
        coinTrade = coin + "with" + tradeType
        mongoClient = MongoClient("mongodb://binance:binance@127.0.0.1:27017/binancedb")
        db = mongoClient['binancedb']
        aggTrade = db[coinTrade]
        latestTimestamp = 0
        symbol = coin+tradeType
        url = self.tradesUrl % (limit, symbol)
        while True:
            context = ssl._create_unverified_context()
            req = request.Request(url, headers=choice(self.allHeaders))
            res = request.urlopen(req, context=context)
            body = res.read()
            body = body.decode('utf8')
            jsonBody = loads(body)
            index = 0
            for trade in reversed(jsonBody):
                if trade['T'] == latestTimestamp:
                    index = jsonBody.index(trade)+1
                    break
            latestTimestamp = jsonBody[-1]['T']
            newTrades = jsonBody[index:]
            # print('CoinName:%s, newst trade:%s' % (coin, newTrades))
            # print("CoinName:%s, Length:%d" % (coin, len(newTrades)))
            for trade in newTrades:
                aggTrade.insert(trade)

            if coin == 'BTC' or coin == 'ETH' or coin == 'IOTA':
                sleep(15)
            else:
                sleep(45)

if __name__ == '__main__':
    # productsUrl = 'https://www.binance.com/exchange/public/product'
    # tradeType = 'USDT'
    # allHeaders = getAllHeaders()
    # headers = choice(allHeaders)
    # coins = getAllCoin(productsUrl, headers, tradeType)
    # print(coins)

    binance = binanceSpider()
    binance.startGetAggTrades()