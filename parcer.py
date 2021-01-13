# import driver as driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
            # print(a)
            # print(mid)
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

print('search capcha')


capcha_frame = driver.find_element_by_name("timerfrm")


elements = capcha_frame.find_elements_by_xpath('//img[@src]')
for element in elements:
    a = element.get_attribute("src")
    print(a)
#    a.driver.save_screenshot("capcha.png")






# window_list = driver.window_handles  # список открытых сейчас вкладок
# current_window = driver.current_window_handle  # рабочее окно
#
# print(window_list)
# print(current_window)






#     timer_site = driver.find_element_by_id("seconds")
#     while timer_site != 1:
#         timer_site = driver.find_element_by_id("seconds").get_attribute('text')
#         print(timer_site)
#
#
#     # elements = driver.find_elements_by_xpath('//tbody/tr/td/img[@src]')
#     # for element in elements:
#     #     a = element.get_attribute("src")
#     cifra_capcha = driver.find_elements_by_class_name('cifra')
#     for element in cifra_capcha:
#         a = element.get_attribute("src")
#         print(cifra_capcha)
#
#
# #    time.sleep(60)
#
# # driver.close()
