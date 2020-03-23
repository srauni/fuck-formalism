### 代码文件的作用

服务端有两个可执行文件

`server.py` 用于服务器的网页处理，接受token传入并存储

`auto.py` 用selenium配合firefox浏览器实现模拟操作功能，24小时不断打卡



### 搭建的方法

在Windows系统下，安装最新Python，版本不得低于Python3.5，安装时注意勾选加入PATH

`https://www.python.org/downloads/windows/`

在命令行执行以下代码安装依赖

`pip install selenium requests gevent flask`

下载最新的Firefox浏览器内核

`https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip`

将内核解压到任意位置，并将内核的路径添加到PATH

下载最新的Firefox浏览器并安装

`https://www.mozilla.org/zh-CN/firefox/new/`

环境搭建到此结束



### 服务运行方法

运行`server.py` `auto.py`两个文件即可



### 额外说明

`token.json` 存储托管在服务器的所有token

`uesless_token.json`  存储经排查无效的token

`<year>-<month>-<day>.json` 存储当日已打卡的token