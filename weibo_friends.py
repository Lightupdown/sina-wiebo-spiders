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
from lxml import etree

import requests

DEPTH = 10   # 深度：每爬取一层关注列表 +1

user_id = '5341308489'  # 可以改成任意合法的用户id（爬虫的微博id除外）
cookie = {
    "Cookie": "UM_distinctid=15d878eea3590-0218f16308289e-62101875-100200-15d878eea3644d; SINAGLOBAL=2236675123995.2686.1501217877465; ALF=1512091354; SUB=_2A250_VGKDeRhGedH4lYS9S7FwzmIHXVUHn_CrDV8PUJbkNAKLW_2kW1LL4Q_8rnvA_qW-NGaG10vmycidg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5HHJXCUIfDXAzd9W6MfkTF5JpX5oz75NHD95Qp1K.Xe0-71KnfWs4Dqcj.i--4i-20iKy8i--ci-i2iKnNi--RiK.7i-2Ni--ciKLFi-2c; wvr=6; _s_tentry=-; Apache=9427711519594.443.1509585302199; ULV=1509585302287:35:3:5:9427711519594.443.1509585302199:1509540355205; UOR=news.ifeng.com,widget.weibo.com,www.baidu.com"}  # 将your cookie替换成自己的cookie

'''
自建的多叉树结构
'''
class Catalog():
    def __init__(self,name):
        self.name = name              # 目录的名字
        self.isVstd = False
        self.children = []            # 子节点列表

    # 向该目录下添加一个目录或叶节点
    def add(self,leaf):
        self.children.append(leaf)

    # 以字符串为名字的节点是否在子节点列表中，若在返回下标，不在返回-1
    def name_in(self, name):
        for i in range(len(self.children)):
            child = self.children[i]
            if name == child.name:
                return i
        return -1

    # 删除该目录下的以leaf_name为名字的子节点，若无抛出异常
    def delete(self, leaf_name):
        index = self.name_in(leaf_name)
        if index >= 0:
            del self.children[index]
        else:
            raise Exception("Catalog without the deleted items")

    # 展示树形结构
    def display(self, depth):
        print('-'*depth + self.name)
        for child in self.children:
            child.display(depth+2)

class Leaves(Catalog):
    def __init__(self, name='', value=''):
        self.name = name
        self.isVstd = False
        self.children = []
        self.value = value              #叶节点的值

    # 若向叶节点添加目录或叶节点抛出异常
    def add(self, eaf):
        raise Exception("Leaf nodes can't insert catalog")

    # 想在叶节点下访问子节点列表，抛出异常
    def name_in(self, name):
        raise Exception("Leaf nodes without subcatalog")

    # 想在叶节点下访问子节点列表，抛出异常
    def delete(self, leaf_name):
        raise Exception("Leaf nodes without subcatalog")


def get_weibo_friends(uid):
    pageflag = 1       # 第几页
    myUid = uid        # uid
    weibofriends = 1   # 为了循环预设的值
    friendsL = []
    try:
        filename = myUid + 'friends.txt'       # 此uid的关注列表存放路径
        with open(filename, 'w+') as f:
            while weibofriends:
                url = 'https://weibo.cn/%s/follow?page=%d' % (myUid, pageflag)
                print('url: ', url)
                print('请等待5秒钟...')
                time.sleep(5)
                print('正在爬取第%d页' % pageflag)
                html = requests.get(url, cookies=cookie).content
                # print(html)
                # with open('myhtml.txt', 'rb') as f:
                #     html = f.read()
                # print(html)
                seletor = etree.HTML(html)
                weibofriends = seletor.xpath('//table//tr/td[1]/a[1]/@href')
                # print('weibofriends: ', weibofriends)
                print('正在写入%s文件...' % filename)
                for friend in weibofriends:
                    # friendUid = re.match(r'^(http://weibo.cn[\/.]{0,2}/)([\d\w]*)$', friend)
                    if friend != ['']:
                        friendUidTemp = re.split(r'[/]+', friend)
                        friendUid = friendUidTemp[len(friendUidTemp) - 1]
                        print(friendUid)
                        friendsL.append(friendUid)
                        f.write(friendUid + '\n')
                pageflag += 1
        return friendsL
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


def friends_get(uid):

    oneUid = uid
    root = Catalog(oneUid)

    friendsL1 = get_weibo_friends(root.name)
    # root.isVstd = True

    for f1 in friendsL1:
        friendsL2 = get_weibo_friends(f1)
        f1 = Catalog(f1)
        root.add(f1)
        for f2 in friendsL2:
            friendsL3 = get_weibo_friends(f2)
            f2 = Catalog(f2)
            f1.add(f2)
            for f3 in friendsL3:
                f3 = Catalog(f3)
                f2.add(f3)

    root.display(0)


def test():
    i = []
    while i:
        print('hahhatest')


if __name__ == '__main__':
    friends_get(user_id)
    # test()