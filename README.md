# sina-wiebo-spiders

代码的功能就是从（手机端）新浪微博的页面爬取微博配图，也就是某人发微博时配的图
======================
（毕竟有很多有趣的东西(｀・ω・´)) <br>
但是吧，我这人懒，又不想挨个去找每个用户的uid，然后一个一个爬...<br>
我的理想目标是找到一个原始用户，单后爬取这个这个用户的所有微博配图，再爬取这个用户所关注用户（毕竟关注了，审美应该也差不多嘿嘿嘿<br>
然后在爬这些个关注用户的微博图，再以此爬这些个关注用户的关注用户的微博图。。。来个几轮我觉得也就有个几十多G了<br>

为此我找了半天，结果没发现。。果然真正的大侠都是不屑于这种小把戏的。。。<br>

所以只能自己写了：<br>

# 代理IP的获取及筛选：<br>
* 代码： `get-agency-ip.py`   <br>
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


