#! usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import re  # 正则表达式
import yagmail
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



# 系统变量
StuID = os.environ['STUID']
PW = os.environ['PW']
MAILBOX = os.environ['MAILBOX']

CHROMEDRIVER_PATH = '/usr/bin/chromedriver'


# 基本个人信息
url = 'https://xmuxg.xmu.edu.cn/platform'  # 登录的网站
user_email='2576002875@qq.com'#(可选)发送的邮件方 我这里用的一个小号
password_email='ozsydzmhxuzddjhf'#（可选）邮件密码不是qq密码 而是需要到自己的邮箱设置的密码 具体可以百度怎么自动发送邮件
email_reciver=MAILBOX
User = StuID  
passwords = PW 
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
# driver = webdriver.Chrome(CHROMEDRIVER_PATH)
wait = WebDriverWait(driver, 5)  # 每次都进行显示等待，设立最大等待时间为5s，5s内不断检验如果为True则通过



# 启动浏览器
def get_web(driver):
    driver.get(url)
    print('正在打开网页....')

    # 等一下，等数据全部加载出来了再点击
    xpath_find_log_in = '//*[@id="loginLayout"]/div[3]/div[2]/div/button[3]'  # xpath 定位
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_find_log_in)))  # 等到有这个元素加载出现的时候再开始
    tong_yi = driver.find_element_by_xpath(xpath_find_log_in)  # 找到的元素为“统一身份登录”
    return tong_yi
    time.sleep(3)


def get_log(driver):
    tong_yi = get_web(driver)  # 点击“统一身份登录”
    tong_yi.click()
    print('正在尝试找到登录入口...')

    time.sleep(2)
    # 此时进入第一个网址，登录界面
    # xpath_denglu = '//*[@id="casLoginForm"]/p[5]/button'
    # wait.until(EC.presence_of_element_located((By.XPATH, xpath_denglu)))  
    driver.find_element_by_id("username").send_keys(User) 
    driver.find_element_by_id("password").send_keys(passwords) 
    denglu = '//*[@id="casLoginForm"]/p[4]/button'
    # '//*[@id="casLoginForm"]/p[4]/button'
    # '/html/body/div[3]/div[2]/div[2]/div/div[3]/div/form/p[4]/button'
    DengLu = driver.find_element_by_xpath(denglu)  
    return DengLu


def get_system(driver):
    DengLu = get_log(driver)
    DengLu.click()
    print('正在尝试登录账号...')
    time.sleep(2)
    xpath_gegnduo='/html/body/div[1]/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div'
    driver.find_element_by_xpath(xpath_gegnduo).click()
    print('正在进入应用界面')
    time.sleep(1)
    xpath_getsystem = '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div'  
    # xpath_getsystem = '//*[@id="mainPage-page"]/div[1]/div[3]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]'  
    # xpath_getday = '/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[2]/div[5]/div[2]/div[1]'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_getsystem)))
    
    GetSystem = driver.find_element_by_xpath(xpath_getsystem)
    return GetSystem




def log_system(driver):

    GetSystem = get_system(driver)
    GetSystem.click()
    print('正在尝试进入打卡系统...')

    time.sleep(5)  
    BrownserControl = driver.window_handles  
    driver.switch_to.window(BrownserControl[-1])  

    xpath_Health = '//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]'
    time.sleep(2)
#     wait.until(EC.presence_of_element_located((By.XPATH, xpath_Health))) 
    My_Health = driver.find_element_by_xpath(xpath_Health)
    return My_Health


def log_day(driver):
    BrownserControl = driver.window_handles 
    driver.switch_to.window(BrownserControl[-2])  
    xpath_day='/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/i'
    wait.until(EC.presence_of_element_located((By.XPATH, xpath_day))) 
    driver.find_element_by_xpath(xpath_day).click()

    print('正在尝试进入统计打卡系统...')

    time.sleep(3)  
    BrownserControl = driver.window_handles  
    driver.switch_to.window(BrownserControl[-1])  
    time.sleep(1)
    xpath_allday='/html/body/div[2]/div/span[3]' 
    day=driver.find_element_by_xpath(xpath_allday).text
    print(day)
    return day

def GetData(driver):
    My_Health = log_system(driver)
    My_Health.click()
    print('正在尝试进入我的表单...')

    
    time.sleep(3)

  
    content = driver.page_source
    return content


def daka(driver):
    content = GetData(driver)
    where_yes = re.compile('id="select_\d.*?"', re.S)  # 非贪心匹配
    where_save = re.compile('id="preview\d.*?"', re.S)
    whether_Daka = re.compile('span title=".*?"')

    whether_Daka = re.findall(whether_Daka, content)
    print(whether_Daka)

    whether_Daka = whether_Daka[-5]  
    print('你今天的打卡状态为:', whether_Daka)
    where_yes = re.findall(where_yes, content)
    where_save = re.findall(where_save, content)
    where_yes = where_yes[-1]  
    where_save = where_save[0] 

    print('你今天的选择地址为:', where_yes)
    print('你今天的保存地址为:', where_save)  
    if whether_Daka == 'span title="是 Yes"':
        final_content = '你今天已经打过卡了'
        time.sleep(2)


    else:

        xpath_yes = '//*[@' + str(where_yes) + ']/div/div'
        # 更改新的xpath路径,检查一下
        # xpath_save = '//*[@' + str(where_save) + ']/span/span'
        xpath_save = '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/span/span/i'


        wait.until(EC.presence_of_element_located((By.XPATH, xpath_yes)))
        try:
            driver.find_element_by_xpath(xpath_yes).click()
            print('请选择')

            time.sleep(3)
            
            element = driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li/label')
            driver.execute_script("arguments[0].click();", element)

            print('确认')
            time.sleep(1)
            # wait.until(EC.presence_of_element_located((By.XPATH, xpath_save)))
            driver.find_element_by_xpath(xpath_save).click()
            print('保存')

            time.sleep(2)
            
            try:
                alert = driver.switch_to.alert
                print(alert.text)  
                alert.accept()  
                print('选择"是"')
                time.sleep(2)
                content = driver.page_source
                final_data = driver.page_source
                where_yes = re.compile('id="select_\d.*?"', re.S)
                whether_Daka = re.compile('span title=".*?"')
                whether_Daka = re.findall(whether_Daka, content)
                whether_Daka = whether_Daka[-5]
                print(whether_Daka)
                print(where_yes)
                # print(final_data)

                if whether_Daka == 'span title="是 Yes"':
                    final_content = '完成了每日打卡'
                    print(final_content)
                else:  
                    final_content = '出现这种情况多半是学校又加了什么东西导致定位不准但是你已经打过卡啦'
                time.sleep(3)
            except Exception:  
                final_content = "出现这种情况多半是学校又加了什么东西导致定位不准但是你已经打过卡啦"
        except Exception:
            final_content = '无法点击 是不是错过了打卡时间'
    time.sleep(1)
    day=log_day(driver)
    driver.quit()
    output=final_content+'\n'+day
    print(output)
    send_message(output)
    return output



# 发送邮件(可选)
def send_message(content):
    server = yagmail.SMTP(user_email, password_email, host='smtp.qq.com')#, port=25, smtp_starttls=True, smtp_ssl=False
    emailtext = content
    server.send(email_reciver, 'IMPORTANT', emailtext)
    print("发送成功")


# 主函数
final_content = daka(driver)



