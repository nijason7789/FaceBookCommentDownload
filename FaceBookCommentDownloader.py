from selenium import webdriver
import time
import os
import pandas
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains #move_to_element
from selenium.common.exceptions import StaleElementReferenceException #error > element is not attached to the page document
from selenium.common.exceptions import NoSuchElementException #點完所有按鈕時

def login(account, password, driver):
    driver.get('https://www.facebook.com/')
    input_1 = driver.find_element_by_css_selector('#email')
    input_2 = driver.find_element_by_css_selector("input[type='password']")

    input_1.send_keys(account)
    input_2.send_keys(password)
    driver.find_element_by_css_selector("button[name='login']").click()
    time.sleep(1)

def crawl_comments(url, driver):

    #造訪網址
    driver.get(url)
    time.sleep(2)

    #點擊網頁消除 Popped up Notification 
    btn_0 = driver.find_element_by_css_selector('body')
    btn_0.click()
    time.sleep(1)

    #點選【x則留言】按鈕匯入留言資訊
    while(True):
        try:
            btn_1 = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[2]/div/div[2]/div/div[2]')
            driver.execute_script("arguments[0].click();", btn_1)
            time.sleep(1)
            break
        except NoSuchElementException:
            break

    #測試網站是否擁有展開箭頭
    while(True):
        try:
            #點擊展開箭頭
            btn_2 = driver.find_element_by_css_selector('div.rq0escxv.l9j0dhe7.du4w35lb.nc684nl6.g0qnabr5')
            driver.execute_script("arguments[0].click();", btn_2)
            #btn_2.click()
            time.sleep(1)

            #點擊最新留言
            btn_3 = driver.find_elements_by_css_selector("div[role='menuitem']")[2]
            driver.execute_script("arguments[0].click();", btn_3)
            #btn_3.click()
            time.sleep(1)
            break
        except NoSuchElementException:
            break

    #點擊更多留言
    while(True):
        try:
            btn_more = driver.find_element_by_css_selector('span.j83agx80.fv0vnmcu.hpfvmrgz')
            ActionChains(driver).move_to_element(btn_more).perform()
            driver.execute_script("arguments[0].click();", btn_more)
            time.sleep(1.5)
            #span.j83agx80.a5y0qf1c.fv0vnmcu.ozuftl9m
        except StaleElementReferenceException: #element is not attached to the page document
            #define the web element once again
            btn_more = driver.find_element_by_css_selector('span.j83agx80.fv0vnmcu.hpfvmrgz')
            ActionChains(driver).move_to_element(btn_more).perform()
            driver.execute_script("arguments[0].click();", btn_more)
            time.sleep(1.5)
            ##span.j83agx80.a5y0qf1c.fv0vnmcu.ozuftl9m
        except NoSuchElementException: #點完所有更多留言按鈕了
            break

    #點選查看更多
    while(True):
        try:
            btn_moreDetail = driver.find_element_by_xpath('//*[contains(text(),"查看更多")]')
            driver.execute_script("arguments[0].click();", btn_moreDetail)
            print('我點!')
            time.sleep(1)
        except NoSuchElementException:
            print('沒有查看更多!')
            break

    #將所有留言內容存起來
    all = [] #存放所有留言
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comments = soup.find_all("div", class_="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05")
    print('一共擷取到',len(comments),'則留言，已成功生成：留言內容.csv')
    for comment in comments:
        dic = {}
        dic['name'] = comment.find('span', class_='pq6dq46d').text
        try:
            dic['data'] = comment.find('div', class_='ecm0bbzt').text
        except AttributeError: #非文字檔
            dic['data'] = '圖檔'
        all.append(dic)

    #輸出
    out_dir = './data'
    out_name = '留言內容.csv'
    df = pandas.DataFrame(data = all)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    fullname = os.path.join(out_dir, out_name)    
    df.to_csv(fullname, encoding='utf_8_sig', index=False)

if __name__ == '__main__':
    #目標網址
    url = input('目標網址：')#

    #登入帳號
    account = input('您的帳號：')
    password = input('您的密碼：')

    #driver設定
    driver = webdriver.Chrome()
    
    login(account, password, driver)


    #開始爬蟲
    crawl_comments(url, driver)