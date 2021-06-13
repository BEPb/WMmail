# python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


def check_exists_by_name(name):
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_link(name):
    try:
        driver.find_element_by_partial_link_text(name)
    except NoSuchElementException:
        return False
    return True

def find_google(name):
    global start_link_adversting
    if check_exists_by_link(name):
        driver.find_element_by_partial_link_text(name).click()
    else:
        while check_exists_by_link(name) == False:
            driver.find_element_by_partial_link_text('Следующая').click()
        start_link_advertising = driver.find_element_by_partial_link_text(name)
        driver.find_element_by_partial_link_text(name).click()
    return start_link_advertising

def viewing_ads():  # просмотр рекламы
    global url_total
    time.sleep(5)
    url_total=[' ', ' ', 'Баннеры рекламы:', ' ']
    elements = driver.find_elements_by_xpath("//img[@nopin='nopin']")
    a = 0
    for element in elements:  # открываем 4 вкладки рекламы
        if a < 4:
            a += 1

            element.click()
            time.sleep(1)
            driver.switch_to_window(driver.window_handles[a])
            url = driver.current_url
            print(url)
            url_total.append(url)
        driver.switch_to_window(driver.window_handles[0])

    url_total.append(' ')
    url_total.append(' ')
    url_total.append('Страницы сайта:')
    url_total.append(' ')
    url_total.append('https://cofax.ru/page/--19.html')
    url_total.append('https://cofax.ru/page/-api-1.html')
    url_total.append('https://cofax.ru/page/--2.html')
    url_total.append('https://cofax.ru/page/--3.html')
    url_total.append('https://cofax.ru/page/developers-21.html')
    url_total.append(' ')
    for element in url_total:
        print(element)

    time.sleep(30)

    for i in range(1, 5):  # закрывает все вкладки рекламы
        driver.switch_to_window(driver.window_handles[1])
        driver.close()

    return url_total


def task_1():
    global driver

    driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get('https://www.google.com/')
    google_poisk = driver.find_element_by_name("q")
    google_poisk.send_keys('Cofax ru')
    google_poisk.send_keys(Keys.ENTER)

    find_google('Игры онлайн - Cofax.ru')

    viewing_ads()


    driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')

    # вводим логин
    login_site = driver.find_element_by_name("ulogin")
    login_site.send_keys('3BEPb1')
    password_site = driver.find_element_by_name("pass")
    password_site.send_keys('3BEPb120')
    password_site.send_keys(Keys.ENTER)

    # обходим проверочный код
    if check_exists_by_name("pass1") == True:
        password_opp = driver.find_element_by_name("pass1")
        password_opp.send_keys('F0eX1lf5NH')
        password_opp.send_keys(Keys.ENTER)

    driver.find_element_by_partial_link_text('Задания').click()
    tak_id_input = driver.find_element_by_name("zd_name")
    tak_id_input.send_keys('1595642')
    tak_id_input.send_keys(Keys.ENTER)
    driver.find_element_by_partial_link_text('КЛИКАТЬ на 4 баннер рекламы').click()

    element = driver.find_element_by_xpath("//input[@type = 'submit']")
    element.click()


    element = driver.find_element_by_xpath("//input[@value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']")
    element.click()

    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Начать выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;"
    # onclick = "setInterval(function fresh() {location.reload();} , 1000);" >

def task_2():
    driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
    driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')

    # вводим логин
    login_site = driver.find_element_by_name("ulogin")
    login_site.send_keys('3BEPb1')
    password_site = driver.find_element_by_name("pass")
    password_site.send_keys('3BEPb120')
    password_site.send_keys(Keys.ENTER)

    # обходим проверочный код
    if check_exists_by_name("pass1") == True:
        password_opp = driver.find_element_by_name("pass1")
        password_opp.send_keys('F0eX1lf5NH')
        password_opp.send_keys(Keys.ENTER)

    driver.find_element_by_partial_link_text('Задания').click()
    tak_id_input = driver.find_element_by_name("zd_name")
    tak_id_input.send_keys('1595642')
    tak_id_input.send_keys(Keys.ENTER)
    driver.find_element_by_partial_link_text('КЛИКАТЬ на 4 баннер рекламы').click()

    element = driver.find_element_by_xpath("//input[@type = 'submit']")
    element.click()


    element = driver.find_element_by_xpath("//input[@value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']")
    element.click()

    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Начать выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;"
    # onclick = "setInterval(function fresh() {location.reload();} , 1000);" >


#task_1()

#разделить картинку
#<img src="index.php?cf=reg-lostpassnum&amp;rnd=1619526.4295704" alt="" border="0">

#вставить в окно
#<input type="text" name="pnum" size="5">

#нажать на кнопку подтверждения
#<input type="submit" name="Submit" value="Начать выполнять задание">