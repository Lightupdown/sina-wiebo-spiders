#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = ''
__author__ = 'zhang'
__mtime__  = '2017/11/2'

              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import telnetlib
import urllib
from urllib import request

import time

import requests
from bs4 import BeautifulSoup

# 想爬多少页：每页100个
PAGE = 10   # 页数

'''
国内透明代理IP    nt
国内高匿代理IP    nn
HTTPS代理IP       wn
HTTP代理IP        wt
'''
TYPE = 'nt'    # 把你想爬的IP类型替换

# 包装的头，不用理
header = {}
User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header['User-Agent'] = User_Agent

def get_agency_ip(page=1):
    '''
    从西刺代理爬下来所需要的IP和端口，但是你知道的，大部分都不能用，所以还需过滤，过滤在后面
    :param page: 从第几页开始爬，无需理会
    :return: 无  会在代码根目录生成一个 proxyold.txt 的文本文件，不想放那你就自己换位置吧
    '''
    with open(TYPE + 'proxyold.txt', "w+") as f:
        while page <= PAGE:
            page += 1
            time.sleep(3)
            url = 'http://www.xicidaili.com/%s/%d' % (TYPE, page)
            req = urllib.request.Request(url, headers=header)
            res = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(res, 'lxml')
            ips = soup.findAll('tr')
            # 你可以自己换位置
            # path = os.path.abspath('.')
            # path = os.path.join(path, 'ipagency')
            # filename = os.path.join(path, 'proxy.txt')
            # print('filename: ', filename)
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + "\t\t" + tds[2].contents[0] + '\t\t' + tds[5].contents[0] + "\n"
                print(tds[1].contents[0]+"\t"+tds[2].contents[0])
                f.write(ip_temp)

def get_ip_status_http(ip=0, port=0):
    '''
    通过urllib.request的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个 TYPE+'proxynew.txt' 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''
    with open(TYPE+'proxynew.txt', 'w+') as f_w:
        with open(TYPE+'proxyold.txt', 'r') as f:
            lines = f.readlines()
            print('lines: ', lines)
            proxys = []
            for i in range(0, len(lines)):
                ip = lines[i].strip("\n").split("\t")
                proxy_host = "http://" + str(ip[0] + ":" + ip[1])
                print('proxy_host: ', proxy_host)
                # proxy_temp = {"http": proxy_host}
                # proxys.append(proxy_temp)
                proxys.append(proxy_host)
            # url = "http://ip.chinaz.com/getip.aspx"
            url = 'http://www.whatismyip.com.tw/'
            for proxy in proxys:
                try:
                    timeout = 3
                    proxy_http = {'http':proxy}
                    proxy_support = urllib.request.ProxyHandler(proxy_http)
                    opener = urllib.request.build_opener(proxy_support)
                    urllib.request.install_opener(opener)
                    res = urllib.request.urlopen(url, timeout).read().decode('utf-8')
                    print('res: ', res)
                    f_w.write(proxy)
                    f_w.flush()
                except Exception as e:
                    print(proxy)
                    print('Error: ', e)
                    continue

def get_ip_status_telnet(ip=0, port=0):
    '''
    通过telnet的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个 TYPE+'proxynew.txt' 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''
    with open(TYPE+'proxynew.txt', 'w+') as f_w:
        with open(TYPE+'proxyold.txt', 'r') as f:
            lines = f.readlines()
            print('lines: ', lines)
            # proxys = []
            for i in range(0, len(lines)):
                ip = lines[i].strip("\n").split("\t")
                proxy_host = str(ip[0] + ":" + ip[1])
                ip = str(ip[0])
                port = str(ip[1])
                try:
                    telnetlib.Telnet(ip, port=port, timeout=5)
                except:
                    print('onnect failed')
                else:
                    print('success')
                    f_w.write(proxy_host)
                    f_w.flush()  # 一定要加这个

def get_ip_status_requests(ip=0, port=0):
    '''
    通过requests.get的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个proxynew.txt 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''
    with open(TYPE+'proxyold.txt', 'r+') as f:
        lines = f.readlines()
    print('lines: ', lines)
    with open(TYPE+'proxynew.txt', 'w+') as f_w:
        # proxys = []
        for i in range(0, len(lines)):
            ip = lines[i].strip("\n").split("\t")
            proxy_host = 'http://' + str(ip[0] + ":" + ip[1])
            print('proxy_host: ', proxy_host)
            ipn = str(ip[0])
            port = str(ip[1])
            try:
                time.sleep(1)
                requests.get('http://ip.chinaz.com/getip.aspx', proxies={"http": proxy_host}, timeout=4)
                f_w.write(ipn + ':' + port + '\n')
                f_w.flush()   # 一定要加这个，要不然你中途停了，全都保存不了
            except:
                print('connect failed')
            else:
                print('success')



def main():
    get_agency_ip()    # 爬代理IP和端口
    # 以下是三种不同的方式验证IP是否可用，可斟酌调用
    # get_ip_status_http()
    # get_ip_status_telnet()
    get_ip_status_requests()

if __name__ == '__main__':
    main()
