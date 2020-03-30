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

def start(driver, account, password):
    # 打开浏览器
    navigate(driver, 'http://yqfk.dgut.edu.cn/main')
    print('页面开启完成')

    # 等待帐号密码窗口均可键入
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="casPassword"]')))
    element = driver.find_element_by_xpath('//*[@id="username"]')
    element.send_keys(account)
    element = driver.find_element_by_xpath('//*[@id="casPassword"]')
    element.send_keys(password)
    print('帐号密码键入完毕')

    # 点击登录按钮
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
    element = driver.find_element_by_xpath('//*[@id="loginBtn"]')
    element.click()
    print('登录按钮已点击')

    # 等待当前窗口跳转到填表页面
    while driver.current_url != 'http://yqfk.dgut.edu.cn/main':
        try:
            element.click()
        except Exception:
            pass
        time.sleep(0.1)
    print('成功跳转到填表页面')

    # 等待已有资料加载完毕
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/form/div/div[1]/div[2]/div/div[1]/div')))
    element = driver.find_element_by_xpath('/html/body/div/div/div/form/div/div[1]/div[2]/div/div[1]/div')
    while element.text == '':
        time.sleep(0.1)
    print('已有资料加载完毕')
    # 判断是否已提交成功
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]')))
        element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]')
        print(element.text)
        if (element.text.find("成功") == -1):
            raise TimeoutException
        print('今日已提交成功，无需再次提交')
        return 0
    except TimeoutException:
        pass
    print('今日未提交，需要点击提交按钮')

    # 点击提交按钮
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/form/div/div[27]/a')))
    element = driver.find_element_by_xpath('/html/body/div/div/div/form/div/div[27]/a')
    element.click()
    print('已点击提交按钮')

    # 等待成功提交
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]')))
    element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]')
    for i in range(30):
        if element.text.find('成功') != -1:
            print('提交成功')
            return 0
        time.sleep(1)

    print('等待提交超时')
    return 1

if __name__ == '__main__':
    #---------------在此填写您的帐号和密码----------------
    ACCOUNT = ''
    PASSWORD = ''
    #-------------------------------------------------

    success_day_mark = 0        # 标记已打卡的day，如果获取当前day与此不同，则说明今日未打卡

    while True:
        time.sleep(5)

        localtime = time.localtime(time.time())
        
        # 在23:00~1:00之间不进行打卡操作，避开高峰期
        if localtime.tm_hour >= 23:
            time.sleep(5)
            continue
        if localtime.tm_hour < 1:
            time.sleep(5)
            continue

        # 已打卡则不打卡
        if (localtime.tm_yday == success_day_mark):
            continue
        try:
            driver = webdriver.Firefox()
            res = start(driver, ACCOUNT, PASSWORD)
            if res == 0:
                success_day_mark = localtime.tm_yday
        except Exception as e:
            print(e)
        finally:
            driver.quit()
        
        
        


    