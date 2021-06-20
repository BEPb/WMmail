# python3
# модуль выполнения заданий

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import cv2  # библиотека  OpenCV обработки изображений и видео
from PIL import Image
from keras.models import load_model
import argparse
import pickle


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

    time.sleep(1)

    for i in range(1, 6):  # закрывает все вкладки рекламы
        driver.switch_to_window(driver.window_handles[0])
        driver.close()

    return url_total

def capcha_analiz(image_element):
    global label
    # создаём парсер аргументов и передаём их
    ap = argparse.ArgumentParser()
#    ap.add_argument("-i", "--image", required=True,
#                    help="path to input image we are going to classify")
    ap.add_argument("-m", "--model", required=True,
                    help="path to trained Keras model")
    ap.add_argument("-l", "--label-bin", required=True,
                    help="path to label binarizer")
    # ap.add_argument("-w", "--width", type=int, default=28,
    #                 help="target spatial dimension width")
    # ap.add_argument("-e", "--height", type=int, default=28,
    #                 help="target spatial dimension height")
    ap.add_argument("-f", "--flatten", type=int, default=-1,
                    help="whether or not we should flatten the image")
    args = vars(ap.parse_args())

    # загружаем входное изображение и меняем его размер на необходимый
    image = cv2.imread(image_element)
    output = image.copy()

    image = cv2.resize(image, (18, 60))

    # масштабируем значения пикселей к диапазону [0, 1]
    image = image.astype("float") / 255.0

    # проверяем, необходимо ли сгладить изображение и добавить размер
    # пакета
    if args["flatten"] > 0:
        image = image.flatten()
        image = image.reshape((1, image.shape[0]))

    # в противном случае мы работаем с CNN -- не сглаживаем изображение
    # и просто добавляем размер пакета
    else:
        image = image.reshape((1, image.shape[0], image.shape[1],
                               image.shape[2]))

    # загружаем модель и бинаризатор меток
    print("[INFO] loading network and label binarizer...")
    model = load_model(args["model"])
    lb = pickle.loads(open(args["label_bin"], "rb").read())

    # делаем предсказание на изображении
    preds = model.predict(image)

    # находим индекс метки класса с наибольшей вероятностью
    # соответствия
    i = preds.argmax(axis=1)[0]
    label = lb.classes_[i]
    text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
    print(text)  # значение + процент
    return label


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)


def task_1():
    global driver
    driver = webdriver.Chrome(r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMIBOOK

    #driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")  # место расположения chromedriver.exe

    driver.get('https://www.google.com/')
    google_poisk = driver.find_element_by_name("q")
    google_poisk.send_keys('Cofax ru')
    google_poisk.send_keys(Keys.ENTER)
    find_google('Игры онлайн - Cofax.ru')
    viewing_ads()

    driver = webdriver.Chrome(
        r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMIBOOK

    #driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
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
    driver.switch_to.window(driver.window_handles[1])  # переход в окно 1
    capcha_reshena = 0
    url_faunded = 0
    print('Начинаем решать качпу')

    while capcha_reshena == 0:
        time.sleep(2)

        elements = driver.find_elements_by_xpath('//img[@src]')
        print("Решаем")

        for element in elements:  # во множестве ссылок выбираем именно нашу капчу
            url_capcha = element.get_attribute("src")
            if url_capcha[0:53] == 'http://www.wmmail.ru/index.php?cf=reg-lostpassnum&rnd':
                screenshot_as_bytes = element.screenshot_as_png
                with open('capcha.png', 'wb') as f:
                    f.write(screenshot_as_bytes)


                coords = (16, 0, 100, 40)  # Обрезка пяти цифр из общей капчи 115х40 (отрезаем лишние квадраты в начале и конеце капчи)
                coords_c1 = (0, 0, 16, 40)  # задаем координаты  цифры №1 17x40
                coords_c2 = (17, 0, 34, 40)  # задаем координаты  цифры №2 17x40
                coords_c3 = (35, 0, 51, 40)  # задаем координаты  цифры №3 17x40
                coords_c4 = (52, 0, 68, 40)  # задаем координаты  цифры №4 17x40
                coords_c5 = (69, 0, 85, 40)  # задаем координаты  цифры №5 17x40

                #            im = Image.open("capcha.png")  # uses PIL library to open image in memory
                #            im.save('screenshot.png')  # saves new cropped image
                crop("capcha.png", coords, 'crop_capcha.png')  # вырезаем 5 цифр
                time.sleep(2)
                crop('crop_capcha.png', coords_c1, 'number_c1.png') # вырезаем цифру №1
                crop('crop_capcha.png', coords_c2, 'number_c2.png') # вырезаем цифру №2
                crop('crop_capcha.png', coords_c3, 'number_c3.png')  # вырезаем цифру №3
                crop('crop_capcha.png', coords_c4, 'number_c4.png')  # вырезаем цифру №4
                crop('crop_capcha.png', coords_c5, 'number_c5.png')  # вырезаем цифру №5

                #приступаем к анализу каждой цифры
                capcha_analiz('number_c1.png')
                number_c1 = label
                print('1 цифра', number_c1)
                capcha_analiz('number_c2.png')
                number_c2 = label
                print('2 цифра', number_c2)
                capcha_analiz('number_c3.png')
                number_c3 = label
                print('3 цифра', number_c3)
                capcha_analiz('number_c4.png')
                number_c4 = label
                print('4 цифра', number_c4)
                capcha_analiz('number_c5.png')
                number_c5 = label
                print('5 цифра', number_c5)

                number = number_c1 + number_c2 + number_c3 + number_c4 + number_c5
                print('Итоговая цифра', number)

                capcha_site = driver.find_element_by_name("pnum")  # находим окно для ввода капчи
                capcha_site.send_keys(number)
                capcha_site.send_keys(Keys.ENTER)

                elements = driver.find_elements_by_xpath('//img[@src]')

                for element in elements:  # во множестве ссылок выбираем именно нашу капчу
                    url_capcha = element.get_attribute("src")
                    if url_capcha[0:53] == 'http://www.wmmail.ru/index.php?cf=reg-lostpassnum&rnd':
                        url_faunded = 1

                if url_faunded == 1:
                    capcha_reshena = 0
                else:
                    capcha_reshena = 1
            if capcha_reshena == 1:
                break

    time.sleep(2)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])




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


task_1()

#разделить картинку

#<img src="index.php?cf=reg-lostpassnum&amp;rnd=1622127.1898102" alt="" border="0">

#вставить в окно
#<input type="text" name="pnum" size="5">

#нажать на кнопку подтверждения
#<input type="submit" name="Submit" value="Начать выполнять задание">

    # element = driver.find_element_by_xpath("//input[@value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']")
    # element.click()



