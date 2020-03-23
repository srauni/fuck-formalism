from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
import json
import sys
import time

def navigate(driver, url):
    while True:
        try:
            driver.get(url)
            break
        except WebDriverException:
            continue

def start(token):
    token = "'" + token + "'"

    # 打开浏览器，注入token
    driver = webdriver.Firefox()
    navigate(driver, 'http://yqfk.dgut.edu.cn/main')
    driver.execute_script("window.localStorage.setItem('token'," + token + ");")
    navigate(driver, 'http://yqfk.dgut.edu.cn/main')

    # 判断token是否已失效（失效会跳转到登录页面且不跳回，但有时又不会跳转到登录页面）
    try:
        WebDriverWait(driver, 10).until(EC.url_matches('https://cas.dgut.edu.cn'))
    except TimeoutException:
        pass
    try:
        WebDriverWait(driver, 10).until(EC.url_matches('http://yqfk.dgut.edu.cn/'))
    except TimeoutException:
        driver.quit()
        return 1

    try:
        # 等待已有资料加载出来
        element = driver.find_element_by_xpath('/html/body/div/div/div/form/div/div[1]/div[2]/div/div[1]/div')
        while element.text == '':
            time.sleep(0.1)
        print(element.text)
    except StaleElementReferenceException:
        # 页面跳转后也会导致元素失效，故在此设置异常
        driver.quit()
        return 1

    # 判断是否已提交成功
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]')))
        driver.quit()
        return 0
    except TimeoutException:
        pass
    
    # 点击提交按钮
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/form/div/div[27]/a')))
    element = driver.find_element_by_xpath('/html/body/div/div/div/form/div/div[27]/a')
    element.click()

    # 等待成功提交
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]')))
    
    driver.quit()

    return 0

if __name__ == '__main__':
    while True:
        localtime = time.localtime(time.time())
        
        # 在23:00~1:00之间不进行打卡操作
        if localtime.tm_hour >= 23:
            time.sleep(5)
            continue
        if localtime.tm_hour < 1:
            time.sleep(5)
            continue

        # 读取今日已填token
        success_token = None
        try:
            with open(str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday) + '.json', 'r') as f:
                success_token = json.loads(f.read())
        except FileNotFoundError:
            success_token = []

        # 读取所有托管token
        all_token = None
        try:
            with open('token.json', 'r') as f:
                all_token = json.loads(f.read())
        except FileNotFoundError:
            all_token = []

        # 读取所有失效token
        useless_token = None
        try:
            with open('useless_token.json', 'r') as f:
                useless_token = json.loads(f.read())
        except FileNotFoundError:
            useless_token = []

        # 执行一遍打卡操作
        for token in all_token:
            if token in useless_token:
                continue
            if token in success_token:
                continue
            while True:
                try:
                    res = start(token)
                    if res == 0:
                        with open(str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday) + '.json', 'w') as f:
                            success_token.append(token)
                            f.write(json.dumps(success_token))
                    elif res == 1:
                        with open('useless_token.json', 'w') as f:
                            useless_token.append(token)
                            f.write(json.dumps(useless_token))
                    else:
                        print('意外的返回')
                    break
                except Exception as e:
                    print(e)
        time.sleep(5)


    