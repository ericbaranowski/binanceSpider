# -*- coding: utf-8 -*-

import io
import gzip
from random import choice, randint
from urllib import request

BASEHEADERS = {'binanceProduct':{'method': 'GET',
                        'scheme': 'https',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)',
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
                        'accept-encoding': 'gzip, deflate, br',
                        'cache-control': 'max-age=0',
                        'lang': 'cn',
                        'upgrade-insecure-requests':'1'
                        },
                'binanceTrade':{'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   	 	'accept-encoding':'gzip, deflate, br',
                   	 	'accept-language':'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
                   	 	'cache-control':'max-age=0',
                   	 	'upgrade-insecure-requests':'1'
                   	 },
                'xici':{'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                   	 	'Accept-Encoding':'gzip, deflate',
                   	 	'Accept-Language':'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
                   	 	'Cache-Control':'max-age=0',
                   	 	'Connection':'keep-alive',
                   	 	'Host':'www.xicidaili.com',
                   	 	'If-None-Match':'W/"b93c86acbabfbc396f5677c6605012ac"',
                   	 	'Upgrade-Insecure-Requests':'1'
                   	 	},
                'kuaidaili':{
                    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,de;q=0.5',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Cookie':'yd_cookie=feba52a3-03f6-45cd508dba336e0c909c630df298a92d269c; _gat=1; _ga=GA1.2.1993143436.1512804818; _gid=GA1.2.1168630916.1512804818; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1512804820; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1512804975',
                    'Host':'www.kuaidaili.com',
                    'Upgrade-Insecure-Requests':'1',

                },
                '58tongchen':{
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.9;q=0.8,zh;q=0.7',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'xm.58.com',
                # 'If-Modified-Since':'Tue, 24 Oct 2017 02:01:37 GMT',
                'Referer':'http://xm.58.com',
                #'Referer':'http://xm.58.com/chuzu/?key=%E8%BD%AF%E4%BB%B6%E5%9B%AD%E4%BA%8C%E6%9C%9F&ispic=1&selpic=2',
                'Upgrade-Insecure-Requests':'1',
                },
            }

PCUSERAGENTS =  [
    # "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
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
    # "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    # "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    # "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    # "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    # "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    # "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    # "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    # "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    # "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    # "Mozilla/2.02E (Win95; U)",
    # "Mozilla/3.01Gold (Win95; I)",
    # "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    # "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
]

MOBILEUSERAGENTS= [
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


def getRandomHeaders(webName, userAgentsType='All'):
    if userAgentsType == 'PC':
        userAgent = choice(PCUSERAGENTS)
    elif userAgentsType == 'Mobile':
        userAgent = choice(MOBILEUSERAGENTS)
    else:
        allUserAgents = PCUSERAGENTS + MOBILEUSERAGENTS
        userAgent = choice(allUserAgents)

    baseHeaders = BASEHEADERS[webName]
    baseHeaders['user-agent'] = userAgent
    return baseHeaders


def getRandomUserAgents(userAgentsType='All'):
    if userAgentsType == 'PC':
        return choice(PCUSERAGENTS)
    elif userAgentsType == 'Mobile':
        return choice(MOBILEUSERAGENTS)
    else:
        allUserAgents = PCUSERAGENTS + MOBILEUSERAGENTS
        return choice(allUserAgents)


def gzip_str(string_):
    out = io.BytesIO()

    with gzip.GzipFile(fileobj=out, mode='w') as fo:
        fo.write(string_.encode())

    bytes_obj = out.getvalue()
    return bytes_obj


def gunzip_bytes_obj(bytes_obj, coding='utf8', errors='strict'):
    in_ = io.BytesIO()
    in_.write(bytes_obj)
    in_.seek(0)
    with gzip.GzipFile(fileobj=in_, mode='rb') as fo:
        gunzipped_bytes_obj = fo.read()

    return gunzipped_bytes_obj.decode(coding, errors)


def getRandomProxy():
    url = 'http://45.62.96.7:5000/randomProxy'
    req = request.Request(url)
    try:
        res = request.urlopen(req, timeout=3)
    except Exception as e:
        return None

    body = res.read()
    body = body.decode('utf8')
    return eval(body)


def showAllProxy():
    url = 'http://45.62.96.7:5000/showAllProxy'
    req = request.Request(url)
    try:
        res = request.urlopen(req, timeout=3)
    except Exception as e:
        return None

    body = res.read()
    body = body.decode('utf8')
    return eval(body)


def removeProxy(proxy):
    url = 'http://45.62.96.7:5000/removeProxy/%s'
    url = url % proxy
    req = request.Request(url)
    try:
        res = request.urlopen(req, timeout=3)
    except Exception as e:
        return None
    return None


def reGetProxy():
    url = 'http://45.62.96.7:5000/startGetProxy'
    req = request.Request(url)
    try:
        res = request.urlopen(req, timeout=600)
    except Exception as e:
        return e
    return None


def takeChoiceProxy():
    n = randint(1,10)
    if n > 3:
        return True
    return False

if __name__ == '__main__':
    headers = getRandomHeaders('xici')
    print(headers)
