# sina-wiebo-spiders

代码的功能就是从（手机端）新浪微博的页面爬取微博配图，也就是某人发微博时配的图
======================
（毕竟有很多有趣的东西(｀・ω・´)) <br>
但是吧，我这人懒，又不想挨个去找每个用户的uid，然后一个一个爬...<br>
我的理想目标是找到一个原始用户，单后爬取这个这个用户的所有微博配图，再爬取这个用户所关注用户（毕竟关注了，审美应该也差不多嘿嘿)<br>
然后在爬这些个关注用户的微博图，再依次爬这些个关注用户的关注用户的微博图。。。来个几轮我觉得也就有个几十多G了<br>

最重要的是：<br>
必须自动化！！也就是我点一个 run，然后静待几十G的成果就好了啊~~

为此我找了半天，结果没找到。。果然真正的大侠都是不屑于这种小把戏的。。。<br>

所以只能自己写了：<br>

# 代理IP的获取及筛选：<br>
* 代码： `get_agency_ip.py`   <br>
(内有超级详细的注释（づ￣3￣）づ╭❤～)   <br>

* 运行方式： 直接运行
* 方法展示：
```python
def get_agency_ip(page=1):
    '''
    从西刺代理爬下来所需要的IP和端口，但是你知道的，大部分都不能用，所以还需过滤，过滤在后面
    :param page: 从第几页开始爬，无需理会
    :return: 无  会在代码根目录生成一个 proxyold.txt 的文本文件，不想放那你就自己换位置吧
    '''

def get_ip_status_http(ip=0, port=0):
    '''
    通过urllib.request的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个proxynew.txt 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''

def get_ip_status_telnet(ip=0, port=0):
    '''
    通过telnet的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个proxynew.txt 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''

def get_ip_status_requests(ip=0, port=0):
    '''
    通过requests.get的方式确定某个IP和端口是否能用，能用的保留到 proxynew.txt 文件中
    :param ip:  本来是为了某些个功能留存的，现在没啥用，可删可留
    :param port: 同上
    :return: 无  生成一个proxynew.txt 的文本文件，其中的所有IP和端口都经过了此方式的验证
    '''
```

# 微博以种子用户为延伸的获取关注列表：<br>
* 代码： `get_weibo_friends.py`   <br>
* 运行方式： 修改部分关键参数（种子用户UID，你的cookie），直接运行<br>
* 方法展示：<br>

```python
'''
关键参数：
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

def loop_dynamic_get(friendsL, depth=0):
    '''
    递归实现，递归调用 get_weibo_friends()
    :param friendsL:  一个list,原始种子用户以单元素list存在。例：['5341308489']
    :param depth: 一个积累的变量，无需理会
    :return:  无
    '''

def friends_get(uid):
    '''
    非递归实现，循环调用 get_weibo_friends()方法,理解原理就好
    :param uid:   用户uid
    :return:    无
    '''

def filter_file(path):
    '''
    部分用户没有关注，所以会生成一个大小为0的无效文件，所以需删除目录下大小为0kb的无效文件
    :param path:目录
    :return:  无
    '''
```

# 下载微博用户的高清图片<br>
* 代码： `get_weibo_photo.py`   <br>
* 运行方式： 修改部分关键参数（你的cookie），直接运行<br>
* 方法展示：<br>
```python
'''
你可以在此处将你的cookie填入， 但是你无需理会 User-Agent
'''
headers = {'User-Agent': '', 'cookie': ''}

def save_image(image_name, filepath):
    '''
    根据image_name 图片名称，下载并保存微博高清配图
    :param image_name:  图片名称
    :param filepath:   保存路径
    :return: 无
    '''

def get_photo():
    '''
    获取 ../friends/ 目录下的各个uid文件来下载用户的微博配图
    使用了代理IP和随机UA来避免被网站抓现行。
    还有很多种不同的反反爬虫的方法，具体可参考GitHub中 luyishisi / Anti-Anti-Spider 项目
    :return: 会在 ../photo/ 目录下生成各个用户的微博图片
    '''

def get_random_agency_ip():
    '''
    从ntproxynew.txt（姑且称其IP池）中随机取一个IP地址返回
    :return:   IP+port   string类型
    '''

def get_random_user_agent():
    '''
    从user_agent_android.txt（UA池）中随机取得一个UA返回
    :return: user-agent   string类型
    '''
```
