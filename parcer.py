# python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui as pg
from selenium.webdriver.common.action_chains import ActionChains
import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.chrome.options import Options
import time


def search_letter():
    global mid, driver
    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")

        if a[0:53] == 'http://www.wmmail.ru/index.php?cf=mail-readpmail&mid=':
            driver.get(a)
            mid = a[53:59]
            return mid
            break


def search_job():
    global mid, driver
    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")

        if a[0:50] == 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=':
            uid = a[50:57]
            href_uid_mid = 'http://www.wmmail.ru/index.php?cf=pmail-readm&uid=' + uid + '&mid=' + mid

            if a[0:68] == href_uid_mid:
                driver.get(a)

                break


def simple_press(template):  # функция определения и двойного нажатия на координаты кнопки
    global zero
    try:
        buttonx, buttony = pg.locateCenterOnScreen(template, region=(0, 0, 1600, 900), confidence=0.7)
        pg.moveTo(buttonx, buttony)
        pg.click(buttonx, buttony)
        print(buttonx, buttony)
        time.sleep(2)
    except TypeError:
        return zero



# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Работа с хромом в невидимом режиме
# driver = webdriver.Chrome(options=chrome_options)

def main():
    global driver
    driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')

    driver.set_window_size(1600, 900)
    driver.maximize_window()
    # body = driver.find_element_by_tag_name("body")
    # body.send_keys(Keys.CONTROL, 's')
    # time.sleep(2)
    # body.send_keys(Keys.ENTER)
    # time.sleep(2)
    # screenshot = driver.save_screenshot("{i}.png")
    # driver.close()

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
            driver.switch_to.default_content()
            driver.get(url_capcha)

            for capha in range(10):
                print('capcha save', capha)
                pg.hotkey('ctrl', 's')
                if capha == 0:
                    time.sleep(10)
                    pg.hotkey('ctrl', 'shift', 'n')
                    time.sleep(5)
                    pg.hotkey('enter')
                    time.sleep(2)
                    pg.hotkey('enter')
                    time.sleep(2)
                time.sleep(1)
                pg.hotkey('enter')
            print('Done')
            break
        return driver
    driver.close()


if __name__ == "__main__":
    main()