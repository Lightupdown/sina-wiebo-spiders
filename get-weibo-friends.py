#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__  = '深层爬取微博用户的关注列表，再爬取关注列表中的每一个用户的关注列表'
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
import re
import traceback

import time

import os
from lxml import etree

import requests

'''
以下三个变量请自己根据实际情况进行修改
'''
DEPTH = 2   # 深度：每爬取一层关注列表 +1。2的意思就是 除爬取种子用户的关注列表之外，还会爬关注列表中每个用户的关注列表

user_id = '5341308489'  # 种子用户。你可以改成你想要开始的任意合法的用户id
cookie = {
    "Cookie": ""}  # 将 "" 中替换成自己的cookie，cookie的获取办法可百度

def get_weibo_friends(uid):
    '''
    根据目标的UID获取此用户的关注列表
    :param uid:   目标用户uid
    :return:  生成一个 uid+'friends.txt'的文本，里面存储了此用户的关注用户uid
    '''
    pageflag = 0       # 第几页
    myUid = uid        # uid
    weiboFriends = 1   # 为了循环预设的值
    friendsL = []
    try:
        filename = myUid + 'friends.txt'       # 此uid的关注列表存放路径
        with open(filename, 'w+') as f:
            while weiboFriends:
                pageflag += 1
                url = 'https://weibo.cn/%s/follow?page=%d' % (myUid, pageflag)
                print('url: ', url)
                print('请等待2秒钟...')
                time.sleep(2)
                print('正在爬取第%d页' % pageflag)
                try:
                    '''这里暂时没有用代理IP，关于代理IP的代码参考：
                                    get-agency-ip.py中get_ip_status_requests()方法
                    具体的代理IP的使用放到了后面关于图片下载部分
                    '''
                    html = requests.get(url, cookies=cookie, timeout=20)
                except Exception as e:
                    print('出错的链接： ', url + '已自动略过...\n')
                    print('Error: ', e)
                    continue

                seletor = etree.HTML(html.content)
                weiboFriends = seletor.xpath('//table//tr/td[1]/a[1]/@href')
                # print('weibofriends: ', weibofriends)
                print('正在写入%s文件...' % filename)
                for friend in weiboFriends:
                    # friendUid = re.match(r'^(http://weibo.cn[\/.]{0,2}/)([\d\w]*)$', friend)
                    if friend != ['']:
                        friendUidTemp = re.split(r'[/]+', friend)
                        friendUid = friendUidTemp[len(friendUidTemp) - 1]
                        print(friendUid)
                        friendsL.append(friendUid)
                        f.write(friendUid + '\n')

        return friendsL
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()

def filter_file(path):
    '''
    部分用户没有关注，所以会生成一个大小为0的无效文件，所以需删除目录下大小为0kb的无效文件
    :param path:目录
    :return:  无
    '''
    try:
        for oneFile in os.listdir(path):
            onePathfile = os.path.join(path, oneFile)
            if os.path.exists(onePathfile):
                if not os.path.getsize(onePathfile):
                    os.remove(onePathfile)
                    print('删除大小为0的无效文件：', oneFile)
        return True
    except Exception as e:
        print('Error: ', e)

def friends_get(uid):
    '''
    非递归实现，循环调用 get_weibo_friends()方法,理解原理就好
    :param uid:   用户uid
    :return:    无
    '''
    oneUid = uid
    # 第一层
    friendsL1 = get_weibo_friends(oneUid)
    # 第二层
    for f1 in friendsL1:
        friendsL2 = get_weibo_friends(f1)
        # 第三层
        for f2 in friendsL2:
            friendsL3 = get_weibo_friends(f2)
            # 第四层
            # for f3 in friendsL3:
                # friendsL4 = get_weibo_friends(f3)
                    # ...不断循环

def loop_dynamic_get(friendsL, depth=0):
    '''
    递归实现，递归调用 get_weibo_friends()
    :param friendsL:  一个list,原始种子用户以单元素list存在。例：['5341308489']
    :param depth: 一个积累的变量，无需理会
    :return:  无
    '''
    for f in friendsL:
        if depth < DEPTH:
            friendsLs = get_weibo_friends(f)
            return loop_dynamic_get(friendsLs, depth+1)

if __name__ == '__main__':
    # friends_get(user_id)
    # 结果会在代码目录下 生成一个friends的目录，里面以 uid+friends.txt  为文件名，存储了各个用户的关注列表
    loop_dynamic_get([user_id])
    path = os.path.join(os.path.abspath('.'), 'friends')
    print(path)
    filter_file(path)
