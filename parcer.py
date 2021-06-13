# python3

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

# import task

def search_letter():
    global mid, driver
    elements = driver.find_elements_by_xpath('//tbody/tr/td/a[@href]')
    for element in elements:
        a = element.get_attribute("href")
        if a[0:53] == 'http://www.wmmail.ru/index.php?cf=mail-readpmail&mid=':
            driver.get(a)
            mid = a[53:59]
            return mid


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


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)


def job(driver):
    global label
    time.sleep(2)
    if check_exists_by_name("timerfrm") == True:
        driver.switch_to.frame("timerfrm")  # переход в фрейм с именем

        money = driver.find_elements_by_link_text('Деньги зачислены')
        print('Деньги зачислены -', len(money))
        if len(money) == 1:
            return
        time.sleep(43)

        cifras = driver.find_elements_by_class_name('cifra')
        print('поиск цифр, всего найдено -', len(cifras))

        # executor_url = driver.command_executor._url
        # session_id = driver.session_id
        # print(executor_url)
        # print(session_id)

        for element in cifras:
            cifra = element.get_attribute('text')
            print(cifra)
            src_cifras = element.get_attribute('href')
            print(src_cifras)

        elements = driver.find_elements_by_xpath('//img[@src]')
        print('search capcha')
        print(len(elements))
        for element in elements:
            url_capcha = element.get_attribute("src")
            if url_capcha[0:48] == 'http://www.wmmail.ru/index.php?cf=pmail-viewimg&':
                print(url_capcha)

                screenshot_as_bytes = element.screenshot_as_png
                with open('capcha.png', 'wb') as f:
                    f.write(screenshot_as_bytes)

                coords = (32, 0, 68, 60)  # Обрезка двойной цифры из общей капчи
                coords_lt = (0, 0, 18, 60)  # вырезаем левую цифру
                coords_rd = (19, 0, 36, 60)  # вырезаем правую цифру
                coords_mid = (8, 0, 24, 60)  # вырезаем центр

    #            im = Image.open("capcha.png")  # uses PIL library to open image in memory
    #            im.save('screenshot.png')  # saves new cropped image
                crop("capcha.png", coords, 'crop_capcha.png')
                time.sleep(2)
                crop('crop_capcha.png', coords_lt, 'number_left.png')
                crop('crop_capcha.png', coords_rd, 'number_right.png')
                crop('crop_capcha.png', coords_mid, 'number_mid.png')
                capcha_analiz('number_left.png')
                number_left = label
                print('левая цифра', number_left)
                capcha_analiz('number_right.png')
                number_right = label
                print('правая цифра', number_right)
                number = number_left + number_right
                print(number)
                capcha_analiz('number_mid.png')
                number_mid = label
                print('центральная цифра', number_mid)
                for element in cifras:
                    cifra = element.get_attribute('text')
                    print(cifra)
                    if cifra == number:
                        src_cifras = element.get_attribute('href')
                        driver.get(src_cifras)
                        time.sleep(2)
                        return
                    elif cifra == number_mid:
                        src_cifras = element.get_attribute('href')
                        driver.get(src_cifras)
                        print(src_cifras)
                        time.sleep(2)
                        return

        money = driver.find_elements_by_link_text('Деньги зачислены')
        print('Деньги зачислены -', len(money))
        if len(money) == 1:
            driver.switch_to.default_content()
            return
    else:
        exit(0)


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


def check_exists_by_name(name):
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True


# def check_exists_frame(name):
#     try:
#         driver.switch_to.frame(name)
#     except NoSuchFrameException:
#         return False
#     return True


# Работа с БД
conn = sqlite3.connect('mydatabase.db')  # создаем переменную conn и  соединение с нашей базой данных
c = conn.cursor()  # Создаем курсор - это специальный объект который делает запросы и получает их результаты
c.execute("""CREATE TABLE IF NOT EXISTS total(
   name_id INTEGER PRIMARY KEY,
   date DATE NOT NULL,
   time DATE NOT NULL,
   tipe_of_tasks TEXT NOT NULL,   
   number_of_letters TEXT NOT NULL,
   amount_of_money INT NOT NULL);
""")
conn.commit()  # применяем изменения


def print_oll_table():  # функция вывода всей таблицы
    c.execute("SELECT * FROM total;")
    all_results = c.fetchall()
    for id in all_results:
        print(id[0], id[1], id[2], id[3], id[4], id[5])
        conn.commit()  # применяем изменения


def load_table():
    c.execute("SELECT * FROM total  WHERE   name_id = (SELECT MAX(name_id)  FROM total);")
    result_old = c.fetchone()
    # print(result_old) # выводит последнюю строку таблицы
    # for id in result_old: # выводит по одному все значения последней строки
    #     print(id)
    b = result_old[1]
    # print(result_old[0])
    # print(b)
    conn.commit()


def fill_table_start():  # заполняем строку таблицы
    c.execute("""INSERT INTO total(date, time, tipe_of_tasks, number_of_letters, amount_of_money)
                VALUES('10.05.2021', '00:00', 'письма', '1', '0.01');""")
    conn.commit()


def fill_table():  # заполняем строку таблицы
    global start_time, number_of_letters, amount_of_money, tipe_of_tasks
    date = start_time.strftime("%d.%m.%Y")  # дата запуска программы
    time = start_time.strftime("%H:%M:%S")  # время запуска программы

    c.execute("""INSERT INTO total(date, time, tipe_of_tasks, number_of_letters, amount_of_money) 
                    VALUES(?, ?, ?, ?, ?);""",
              (date, time, tipe_of_tasks, number_of_letters, amount_of_money))
    conn.commit()


def main():
    global driver, number_of_letters, amount_of_money
    driver = webdriver.Chrome(r"C:\Users\admin\Downloads\chromedriver.exe")

    driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')
#    driver.set_window_size(1600, 900)
#    driver.maximize_window()
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

    # проверяем сколько писем и баланс
    letter_number = driver.find_element_by_partial_link_text('Письма').get_attribute('text')
    letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')
    amount_of_money = driver.find_element_by_id('ubalance').get_attribute('textContent')

    if len(letter_number) != 6:
        number_of_letters = letter_number[7:8]
        fill_table()
    else:
        number_of_letters = 0
        fill_table()

    # если количество писем не равно 0 то приступаем их читать
    while len(letter_number) != 6:
        driver.get(letter_href)
        letter_href = driver.find_element_by_partial_link_text('Письма').get_attribute('href')
        driver.find_element_by_partial_link_text('Письма').click()
        search_letter()
        search_job()
        job(driver)

#    task.task_1()

    print('Done')
    print_oll_table()
    driver.close()

# fill_table_start()  # стартовое заполнение бд

# переменные
start_time = datetime.now()  # текущие дата и время
tipe_of_tasks = "письма"

if __name__ == "__main__":
    main()