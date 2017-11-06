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
from random import choice
import re
import urllib
from urllib import request

import os
import requests
import time

'''
你可以在此处将你的cookie填入， 但是你无需理会 User-Agent
'''
headers = {'User-Agent': '', 'cookie': ''}
'''
请注意get_random_agency_ip()中的 ip池'proxynew.txt'，将其改成你的文件名
'''
# path路径为 代码 根目录/photo/  是将来的图片存放路径
path = os.path.join(os.path.abspath('.'), 'photo')
# dirPath 为关注列表的存放路径
dirPath = os.path.join(os.path.abspath('.'), 'friends')

def save_image(image_name, filepath):
    '''
    根据image_name 图片名称，下载并保存微博高清配图
    :param image_name:  图片名称
    :param filepath:   保存路径
    :return: 无
    '''
    time.sleep(1)
    # if not os.path.isfile(SAVE_PATH + image_name):
    sina_image_url = 'http://ww1.sinaimg.cn/large/' + image_name
    # sina_image_url = image_name
    try:
        response = requests.get(sina_image_url, stream=True, timeout=10)
    except Exception as e:
        print('Error: ', e)
        return
    image = response.content
    if image:
        try:
            print(image_name)
            filename = os.path.join(filepath, image_name)
            print('正在生成图片[ %s ]...' % filename)
            with open(filename, "wb+") as image_object:
                image_object.write(image)
                return
        except IOError:
            print("IO Error\n")
            return

def get_photo():
    '''
    获取 ../friends/ 目录下的各个uid文件来下载用户的微博配图
    使用了代理IP和随机UA来避免被网站抓现行。
    还有很多种不同的反反爬虫的方法，具体可参考GitHub中 luyishisi / Anti-Anti-Spider 项目
    :return: 会在 ../photo/ 目录下生成各个用户的微博图片
    '''
    uidList = []
    # 从 friends文件夹中取得各个uid文件
    for oneFile in os.listdir(dirPath):
        print('正在读取 %s，准备下载...' % oneFile)
        txtpath = os.path.join(dirPath, oneFile)
        with open(txtpath, 'r+') as f:
            while True:
                oneUid = f.readline().strip()
                if not oneUid:
                    break
                uidList.append(oneUid)
        print('正在生成uid列表...')
        # 检查是否已经下载过此用户，如果没有，则生成此用户的目录，用来下载文件，如果已经下载过，则跳过
        for uid in uidList:
            if uid:
                filepath = os.path.join(path, uid)
            if os.path.exists(filepath):
                print('此文件夹%s已存在...' % filepath)
                continue
            else:
                os.makedirs(filepath)
            page = 0
            uuids = 1
            while uuids:
                print('等待一秒...')
                time.sleep(1)
                page += 1
                # url = 'http://weibo.cn/album/albummblog/?rl=11&fuid=%s&page=%d' % (uid, page)
                url = 'https://weibo.cn/%s?page=%d' % (uid, page)
                print('用户url: ', url)
                try:
                    # 搞一个代理IP： 代理IP池 可从 get_agency_ip.py 中生成
                    agencyip = get_random_agency_ip()  # 从IP池里随机取得代理IP
                    proxy_http = {'http': agencyip}
                    proxy_support = urllib.request.ProxyHandler(proxy_http)
                    opener = urllib.request.build_opener(proxy_support)
                    urllib.request.install_opener(opener)
                    # 随机生成UA
                    random_agent = get_random_user_agent()
                    headers['User-Agent'] = random_agent
                    # headers['cookie'] = ''  # 你也可以在此处填入你的cookie
                    req = urllib.request.Request(url, headers=headers)
                    try:
                        r = urllib.request.urlopen(req, timeout=10)
                    except Exception as e:
                        print('遭遇Error： ', e, '\n')
                        print('遇到错误的URL： ', url)
                        continue
                    data = r.read().decode('utf-8')
                    # print('data: ', data)
                    # p = re.compile(r'src="http://([.]+).sinaimg.cn/wap180/(\w+.png|\w+.jpg)" alt=')
                    p = re.compile(r'([0-9a-zA-Z]{32}.jpg)')
                    print('p: ', p)
                    uuids = p.findall(data)
                    print('uuids: ', uuids)
                    imageurls = []
                    for uuid in uuids:
                        # url = 'http://' + uuid[0] + '.sinaimg.cn/large/' + uuid[1]
                        print('获得图片下载地址：', uuid)
                        imageurls.append(uuid)
                        imageurls.reverse()
                        print('正在下载图片流并生成...')
                        for image in imageurls:
                            save_image(image, filepath)
                except Exception as e:
                    print('Error: ', e)
                    continue

def get_random_agency_ip():
    '''
    从ntproxynew.txt（姑且称其IP池）中随机取一个IP地址返回
    :return:   IP+port   string类型
    '''
    # 请注意此处的 ip池'proxynew.txt'，将其改成你的文件名
    with open('ntproxynew.txt', 'r') as f:
        ipLines = f.readlines()
    for i in range(len(ipLines)):
        ipLines[i] = ipLines[i].replace('\n', '')
        # print('line: ', ipLines[i])
    randomIp = choice(ipLines)
    print('从IP池中取得代理IP： ', randomIp)
    return randomIp

def get_random_user_agent():
    '''
    从user-agent-android.txt（UA池）中随机取得一个UA返回
    :return: user-agent   string类型
    '''
    with open('user_agent_android.txt', 'r') as f:
        agentLines = f.readlines()
    for i in range(len(agentLines)):
        agentLines[i] = agentLines[i].replace('\n', '')
    randomAgent = choice(agentLines)
    print('从UA池中取得user-agent: ', randomAgent)
    return randomAgent

def main():
    print('-----------action-start-------------')
    get_photo()
    print('-----------action--end--------------')

if __name__ == '__main__':
    main()
