import driver as driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')

login_site = driver.find_element_by_name("ulogin")
login_site.send_keys('3BEPb1')
password_site = driver.find_element_by_name("pass")
password_site.send_keys('3BEPb184')
password_site.send_keys(Keys.ENTER)


letter_number = driver.find_element_by_partial_link_text('Письма').get_attribute('text')
letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')
while letter_number[8] != '0':
    driver.get(letter_href)
    letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')

#    driver.find_element_by_partial_link_text('Письма').click()

    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')

    for element in elements:
        a = element.get_attribute("href")

        if a[0:53] == 'http://www.wmmail.ru/index.php?cf=mail-readpmail&mid=':

            driver.get(a)
            mid = a[53:59]
#            print(a)
#            print(mid)
            break

    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")

        if a[0:50] == 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=':
            uid = a[50:57]
#            print(uid)
            href_uid_mid = 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=' + uid + '&mid=' + mid

            if a[0:68] == href_uid_mid:
                driver.get(a)
                break

    time.sleep(60)

# driver.close()
