# python3

import subprocess  # Запуск приложений windows
import time  # работа со временем
import pyautogui as pg  # работа с картинками
from bs4 import BeautifulSoup
import urllib.request

import keyboard  # работа с нажатиями клавиш
import sys  # системными библиотеками
import datetime  # работа с датой и времени
from datetime import datetime
import sqlite3  # Импортируем библиотеку, соответствующую типу нашей базы данных
import random  # рандомные числа


def startlnk():  # функция запуска приложения
    subprocess.Popen('C:\Program Files (x86)\WMMail\wmmail.exe')  # запуск приложения
    time.sleep(2)  # время ожидания запуска


def enter_login():
    print("start")
    simple_press('btn_connect.png')
    simple_press('to_account.png')
    simple_press('login.png')
    simple_press('login_in.png')
    simple_press('btn_enter_login.png')
    time.sleep(5)


def second_enter_login():
    simple_press('login.png')
    simple_press('login_in.png')
    simple_press('enter_to_account.png')


def pointclick():  # функция произвольного нажатия в цикле
    pg.doubleClick(1599, 524)


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


def parcer_wm():
    req = urllib.request.urlopen("https://www.onliner.by/")
    # print(req)
    html = req.read()

    # print(html)

    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('li', class_="b-teasers-2__teaser")
    main_news = soup.find_all('li', class_='cfix')
    # print(main_news)

    results_dict = []
    for item in news:
        title = item.find('span', class_='text-i').get_text()
        href = item.a.get('href')
        print(title)
        print(href)
        results_dict.append({
            'title': title,
            'href': href
        })
    # print(results_dict)

    f = open('news.txt', 'w', encoding='utf-8')
    i = 1

    for item in results_dict:
        f.write(f'Новость № {i} \n\n Название: {item["title"]}\nСсылка: {item["href"]}\n\n')
        i += 1
    f.close()


# variables (переменные)
zero = 0  # переменная отрицания

# исполняемый код
startlnk()  # запуск приложения
enter_login()

while "Бесконечный цикл":
    pointclick()
    time.sleep(5)
    second_enter_login()
