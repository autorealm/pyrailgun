Python 网页爬虫工具 - PyRailgun2
==============

 > **本开源项目** 
``Fork from`` [pyrailgun](https://github.com/princehaku/pyrailgun) 
原作者是 [princehaku](https://github.com/princehaku) 
并使用 ~~MIT~~ 许可协议

### 新特性说明 ###

1. 增强的 ``strip`` 规则配置参数。

 > 进行文本提取时可过滤 HTML 标签及自动换行。 

2. 新增加 ```match``` 规则配置参数。

 > 用于进行 正则表达式 规则匹配，与 ```rule``` 替换使用。

3. 新增加 ```extract``` 规则配置参数。

 > 可进行 XPath 规则匹配，用于将相同节点存储于数组中，需要配合 ```rule``` 或 ```match``` 使用。

4. 增强对重复节点分析功能。

 > 对空值自动匹配，使分析得到的数组个数与重复节点数相等，可使用 ```ignore``` 参数取消。

5. 更加友好的控制台输出提示。

 > 方便查找错误信息。

6. 可对抓取页面的连接进行控制。

 > 防止网络连接或其他情况造成的某些页面抓取失败。

7. 去除了 ```webkit``` 内核抓取支持及其他 BUG 修复。

 > 精简除 ```requests``` / ```lxml``` / ```bs4``` 外，不需要其他依赖包。


### 使用方法 ###

可参考根目录提供的两个样例 ```zhihu``` 和 ```bangumi``` ，分别是抓取 ```知乎``` 和 ```番组计划``` 的脚本。

1. 安装并配置 ```Python2.7``` 环境。
2. 点击运行 ```zhihu.py``` 或 ```bangumi.py``` 。

.. code-block:: python

    from pyrailgun import RailGun

    import sys, re, json
    
    reload(sys)
    sys.setdefaultencoding("utf-8")

    railgun = RailGun()
    railgun.setTask(file("xxx.json"))
    railgun.fire()
    nodes = railgun.getShells()
    
    for id in nodes:
        node = nodes[id]
        ......

--

**以下是源作者的 README：** 

----


NEED Python2.7

功能

* 支持从[json](https://github.com/princehaku/pyrailgun/blob/master/demo/tour/basic.json)文件读取抓取任务

* 支持 python字典数据源方式 定义抓取任务

* [通配符和多页码抓取](https://github.com/princehaku/pyrailgun/wiki/用通配符抓取多页码数据)

* [参数暂存和传递 深度抓取](https://github.com/princehaku/pyrailgun/wiki/参数传递)

* [css选择器](https://github.com/princehaku/pyrailgun/wiki/css选择器)

* [使用requests抓取网页](https://github.com/princehaku/pyrailgun/wiki/使用requests抓取网页)

* [使用webkit内核抓取网页](https://github.com/princehaku/pyrailgun/wiki/使用webkit内核抓取网页)


安装

* [从pip安装] (https://pypi.python.org/pypi/pyrailgun) `pip install pyrailgun`

* 源码安装 `python setup.py install`


语法

* [json对象说明](https://github.com/princehaku/pyrailgun/wiki/json%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E)

例子

* [快速入门] (https://github.com/princehaku/pyrailgun/wiki/简单使用说明)

* [全功能简单例子] (https://github.com/princehaku/pyrailgun/blob/master/demo/tour/)

* [读取输入变量] (https://github.com/princehaku/pyrailgun/blob/master/demo/userinput/)

* [WebKit抓取] (https://github.com/princehaku/pyrailgun/blob/master/demo/webkit/)

* [在没有X的服务器上运行webkit内核抓取](https://github.com/princehaku/pyrailgun/wiki/在没有X的服务器上运行webkit内核抓取)

其他

* python2.7 是必须的

* [_pages](https://github.com/princehaku/pyrailgun/wiki/_pages)

更新


* 0.25
  fix 一个crash问题

* 0.24
  受版权限制，替换webbroser为自己写的版本
  去除yaml的支持
