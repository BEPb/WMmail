# python3
# программа для сбора капч (данных) для машинного обучения

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
from PIL import Image
from keras.models import load_model
import argparse
import pickle
import cv2
import sqlite3  # Импортируем библиотеку, соответствующую типу нашей базы данных

import task


def check_exists_by_name(name):  # проверка на наличие соответсвующего имени
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True



def main():
    global driver, number_of_letters, amount_of_money
    #driver = webdriver.Chrome(r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMRBOOK

    driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")  # место расположения chromedriver.exe
    driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')
    # вводим логин
    login_site = driver.find_element_by_name("ulogin")
    login_site.send_keys('3BEPb1')
    password_site = driver.find_element_by_name("pass")
    password_site.send_keys('F0eX1lf5NH1111')
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

    ##### анализ проверочной капчи из 5 цифр
    elements = driver.find_elements_by_xpath(
        '//img[@src]')  # находим капчу <img src="index.php?cf=reg-lostpassnum&amp;rnd=1619526.4295704" alt="" border="0">
    print('search capcha')

    for element in elements:
        url_capcha = element.get_attribute("src")
        if url_capcha[0:36] == 'index.php?cf=reg-lostpassnum&amp;rnd=':
            print(url_capcha)

            screenshot_as_bytes = element.screenshot_as_png


    print('Done')

    driver.close()


if __name__ == "__main__":
    main()