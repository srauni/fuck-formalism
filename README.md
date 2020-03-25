### 代码文件的作用

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

打开auto.py，在代码的`if __name__ == '__main__'`下面填写自己的帐号密码

运行`auto.py`两个文件即可



### 原理说明

Selenium库可以调用Firefox浏览器自动化，此脚本实现全套的登录、打卡操作