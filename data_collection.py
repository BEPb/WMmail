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
    password_site.send_keys('3BEPb1201111')
    password_site.send_keys(Keys.ENTER)

    # обходим проверочный код
    if check_exists_by_name("pass1") == True:
        password_opp = driver.find_element_by_name("pass1")
        password_opp.send_keys('F0eX1lf5NH')
        password_opp.send_keys(Keys.ENTER)


    print('Done')

    driver.close()


if __name__ == "__main__":
    main()