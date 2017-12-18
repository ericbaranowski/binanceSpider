# -*- coding: utf-8 -*-

import ssl
import common
import multiprocessing
from json import loads
from random import randint
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

    def __prepareWork(self):
        self.allTradeWithBTC = getAllCoin(self.productsUrl, common.getRandomHeaders('binanceProduct'), 'BTC')
        self.allTradeWithUSDT = getAllCoin(self.productsUrl, common.getRandomHeaders('binanceProduct'), 'USDT')

    def startGetAggTrades(self):
        self.process = []
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
            # aproxy = self.proxyObj.randomChoice()
            # choiceProxy = {'http': aproxy}
            # proxy_support = request.ProxyHandler(choiceProxy)
            # opener = request.build_opener(proxy_support)
            # request.install_opener(opener)
            req = request.Request(self.productsUrl, headers=common.getRandomHeaders('binanceProduct'))
            try:
                res = request.urlopen(req, context=context)
            except Exception as e:
                # print('%s proxy can not use, remove' % aproxy)
                # self.proxyObj.removeProxy(aproxy)
                print('%s error happend when getCurrentPrice, sleep 60 second' % e)
                sleep(randint(50,70))
                continue
            body = res.read()
            body = body.decode('utf8')
            jsonBody = loads(body)
            data = jsonBody['data']
            coins = []
            for d in data:
                if d['symbol'].endswith(tradeType):
                    print('Insert CoinName:%s, Current Price:%s' % (d['baseAsset'], d['close']))
                    market.insert(d)
            
            sleep(randint(50,70))

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
            # aproxy = self.proxyObj.randomChoice()
            # choiceProxy = {'http': aproxy}
            # proxy_support = request.ProxyHandler(choiceProxy)
            # opener = request.build_opener(proxy_support)
            # request.install_opener(opener)
            req = request.Request(url, headers=common.getRandomHeaders('binanceTrade'))
            try:
                res = request.urlopen(req, context=context)
            except Exception as e:
                # print('%s proxy can not use, remove' % aproxy)
                # self.proxyObj.removeProxy(aproxy)
                print('%s error happend when getAggTrades, sleep 60 second' % e)
                sleep(randint(50,70))
                continue
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
            print("Insert CoinName:%s, Length:%d" % (coin, len(newTrades)))
            for trade in newTrades:
                aggTrade.insert(trade)

            if coin == 'BTC' or coin == 'ETH' or coin == 'IOTA':
                sleep(randint(10,20))
            else:
                sleep(randint(35, 55))

if __name__ == '__main__':
    binance = binanceSpider()
    binance.startGetAggTrades()
