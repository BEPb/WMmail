# import driver as driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


def search_letter():
    global mid
    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")

        if a[0:53] == 'http://www.wmmail.ru/index.php?cf=mail-readpmail&mid=':
            driver.get(a)
            mid = a[53:59]
            return mid
            break


def search_job():
    global mid
    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")

        if a[0:50] == 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=':
            uid = a[50:57]
            href_uid_mid = 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=' + uid + '&mid=' + mid

            if a[0:68] == href_uid_mid:
                driver.get(a)

                break


# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Работа с хромом в невидимом режиме
# driver = webdriver.Chrome(options=chrome_options)


driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')

login_site = driver.find_element_by_name("ulogin")
login_site.send_keys('3BEPb1')
password_site = driver.find_element_by_name("pass")
password_site.send_keys('3BEPb184')
password_site.send_keys(Keys.ENTER)


letter_number = driver.find_element_by_partial_link_text('Письма').get_attribute('text')
letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')

#while letter_number[8] != '0':
driver.get(letter_href)
letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')
driver.find_element_by_partial_link_text('Письма').click()
search_letter()
search_job()

time.sleep(45)

driver.switch_to.frame("timerfrm") # переход в фрейм с именем

elements = driver.find_elements_by_class_name('cifra')

print('поиск цифр, всего найдено -', len(elements))
for element in elements:
    cifra = element.get_attribute('text')
    print(cifra)


elements = driver.find_elements_by_xpath('//img[@src]')
print('search capcha')
print(len(elements))

for element in elements:
    url_capcha = element.get_attribute("src")
    if url_capcha[0:48] == 'http://www.wmmail.ru/index.php?cf=pmail-viewimg&':
        print(url_capcha)
        driver.get(url_capcha)
        print('Done')
        break

driver.switch_to.default_content()
driver.close()
