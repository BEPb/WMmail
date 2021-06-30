# python3
# модуль выполнения заданий

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains  # переход по координатам
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
        start_link_advertising = driver.find_element_by_partial_link_text(name)
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
    url_total = [' ', ' ', 'Баннеры рекламы:', ' ']
    elements = driver.find_elements_by_xpath("//img[@nopin='nopin']")
    a = 0
    for element in elements:  # открываем 4 вкладки рекламы
        if a < 4:
            a += 1

            element.click()
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[a])
            url = driver.current_url
            print(url)
            url_total.append(url)
        driver.switch_to.window(driver.window_handles[0])

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

    # запись в файл отчета по просмотру по строчно
    with open("task_report.txt", "w") as file:
        for line in url_total:
            file.write(line + '\n')

    time.sleep(1)

    for i in range(1, 6):  # закрывает все вкладки рекламы
        driver.switch_to.window(driver.window_handles[0])
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


def complex_captcha(elements):
    global capcha_reshena
    url_faunded = 0
    for element in elements:  # во множестве ссылок выбираем именно нашу капчу
        url_capcha = element.get_attribute("src")
        if url_capcha[0:53] == 'http://www.wmmail.ru/index.php?cf=reg-lostpassnum&rnd':
            screenshot_as_bytes = element.screenshot_as_png
            with open('capcha.png', 'wb') as f:
                f.write(screenshot_as_bytes)

            coords = (16, 0, 100,
                      40)  # Обрезка пяти цифр из общей капчи 115х40 (отрезаем лишние квадраты в начале и конеце капчи)
            coords_c1 = (0, 0, 16, 40)  # задаем координаты  цифры №1 17x40
            coords_c2 = (17, 0, 34, 40)  # задаем координаты  цифры №2 17x40
            coords_c3 = (35, 0, 51, 40)  # задаем координаты  цифры №3 17x40
            coords_c4 = (52, 0, 68, 40)  # задаем координаты  цифры №4 17x40
            coords_c5 = (69, 0, 85, 40)  # задаем координаты  цифры №5 17x40

            #            im = Image.open("capcha.png")  # uses PIL library to open image in memory
            #            im.save('screenshot.png')  # saves new cropped image
            crop("capcha.png", coords, 'crop_capcha.png')  # вырезаем 5 цифр
            time.sleep(2)
            crop('crop_capcha.png', coords_c1, 'number_c1.png')  # вырезаем цифру №1
            crop('crop_capcha.png', coords_c2, 'number_c2.png')  # вырезаем цифру №2
            crop('crop_capcha.png', coords_c3, 'number_c3.png')  # вырезаем цифру №3
            crop('crop_capcha.png', coords_c4, 'number_c4.png')  # вырезаем цифру №4
            crop('crop_capcha.png', coords_c5, 'number_c5.png')  # вырезаем цифру №5

            # приступаем к анализу каждой цифры
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

            time.sleep(2)

            elements = driver.find_elements_by_xpath('//img[@src]')

            for element in elements:  # во множестве ссылок выбираем именно нашу капчу
                url_capcha = element.get_attribute("src")
                if url_capcha[0:53] == 'http://www.wmmail.ru/index.php?cf=reg-lostpassnum&rnd':
                    url_faunded = 1

            if url_faunded == 1:
                capcha_reshena = 0
                print('Капча решена не правильно')
            else:
                capcha_reshena = 1
                print('Капча решена правильно')
            return capcha_reshena


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)


def active_window():
    try:
        driver.switch_to.window(driver.window_handles[1])
    except IndexError:
        driver.switch_to.window(driver.window_handles[0])


def return_main_window():
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except IndexError:
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_tag_name('body').send_keys(Keys.ALT + Keys.ARROW_LEFT)


def task_1():  # Оплачиваемое задание #1595642
    global driver, url_total, capcha_reshena
    driver = webdriver.Chrome(
        r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMIBOOK

    # driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")  # место расположения chromedriver.exe

    driver.get('https://www.google.com/')
    google_poisk = driver.find_element_by_name("q")
    google_poisk.send_keys('Cofax ru')
    google_poisk.send_keys(Keys.ENTER)
    find_google('Игры онлайн - Cofax.ru')
    viewing_ads()

    driver = webdriver.Chrome(
        r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMIBOOK

    # driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")
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

    # поиск задания
    tak_id_input.send_keys('1595642')
    tak_id_input.send_keys(Keys.ENTER)

    # выбор активного задания
    try:
        driver.find_element_by_partial_link_text('КЛИКАТЬ на 4 баннер рекламы').click()
        element = driver.find_element_by_xpath("//input[@type = 'submit']")
        element.click()
    except NoSuchElementException:
        print("Задание №1595642 не доступно к выполнению")
        driver.close()
        return

    ##### анализ проверочной капчи из 5 цифр
    driver.switch_to.window(driver.window_handles[1])  # переход в окно 1
    capcha_reshena = 0

    print('Начинаем решать качпу')

    time.sleep(2)

    while capcha_reshena == 0:
        elements = driver.find_elements_by_xpath('//img[@src]')
        print("Решаем")
        complex_captcha(elements)

    time.sleep(2)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;" >

    # нажимаем на кнопку подтвердить выполнение задания

    # element = driver.find_element_by_xpath('//input[@value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]')
    elements = driver.find_elements_by_xpath("//input[@type = 'submit']")
    for element in elements:
        print(element)
        value_faunded = element.get_attribute("value")
        print(value_faunded)
        if value_faunded == "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;":
            element.click()

    # < textarea
    # cols = ""
    # rows = "7"
    # name = "zdtext"
    # id = "zdtext"
    # style = "width: 100%;" > < / textarea >

    # вводим данные в окно
    answer_window = driver.find_element_by_name("zdtext")
    answer_window.send_keys(url_total)
    answer_window.send_keys(Keys.LEFT_CONTROL + Keys.ENTER)  # это сочитание заменяет нажатие кнопки отправить
    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Отправить&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;" >

    # # нажимаем на кнопку - отправить
    # # element = driver.find_element_by_xpath("//input[@value = '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Отправить&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']")
    # elements = driver.find_elements_by_xpath("//input[@type = 'submit']")
    # for element in elements:
    #     value_faunded = element.get_attribute("value")
    #     if value_faunded == "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Отправить&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;":
    #         element.click()

    print('Задание завершено')

    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Начать выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;"
    # onclick = "setInterval(function fresh() {location.reload();} , 1000);" >

    driver.switch_to.window(driver.window_handles[0])
    driver.close()


def task_2():  # Оплачиваемое задание #1342716
    global driver  # объявляем глобальную переменную для применения ее между фукнциями
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")


    driver = webdriver.Chrome(
        r"C:\Users\admin\Downloads\chromedriver.exe", chrome_options=options)  # место расположения chromedriver.exe REDMIBOOK

    # driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")  # место расположения chromedriver.exe
    driver.get('https://www.google.com/')
    google_poisk = driver.find_element_by_name("q")

    # вводи фразу в окно поиска "форум новых краснодарцев"
    google_poisk.send_keys('форум новых краснодарцев')
    google_poisk.send_keys(Keys.ENTER)
    find_google('Переезд в краснодар форум')

    # для отображения баннеров рекламы необходимо перейти по странице сайта через выпадающее меню
    driver.find_element_by_xpath("//i[@class = 'fa fm fa-clipboard']").click()  # после нажатия выпадает меню
    #< i class ="fa fm fa-clipboard" > < / i > Инфа о Кубани

    driver.find_element_by_xpath("//a[@href = '/viewforum.php?f=219']").click()  # переход на страницук сайта
    # < a href = "/viewforum.php?f=219" > Путеводитель по Краю < / a >


    time.sleep(5)
    # переход по верхнему баннеру
    ActionChains(driver).move_by_offset(1000, 100).click().perform()  # работает только для разрешения 1920х1080


    active_window()
    url = driver.current_url
    print(url)
    url_total_2 = [' ', ' ', 'Баннер в шапке сайта:', ' ']
    url_total_2.append(url)
    print(url_total_2)
    time.sleep(2)

    return_main_window()

    # # для отображения баннеров рекламы необходимо перейти по странице сайта через выпадающее меню
    # driver.find_element_by_xpath("//i[@class = 'fa fm fa-clipboard']").click()  # после нажатия выпадает меню
    # # < i class ="fa fm fa-clipboard" > < / i > Инфа о Кубани
    #
    # driver.find_element_by_xpath("//a[@href = '/viewforum.php?f=219']").click()  # переход на страницук сайта
    # # < a href = "/viewforum.php?f=219" > Путеводитель по Краю < / a >

    # переход по правому баннеру
    ActionChains(driver).reset_actions()
    ActionChains(driver).move_by_offset(1820, 980).click().perform()   # работает только для разрешения 1920х1080
    active_window()
    url = driver.current_url
    print(url)
    url_total_2.append(url)
    print(url_total_2)
    time.sleep(2)

    return_main_window()

    driver.close()


    # # вводим отчет
    # driver.get('http://www.wmmail.ru/index.php?cf=akk-viewstat/')
    #
    # # вводим логин
    # login_site = driver.find_element_by_name("ulogin")
    # login_site.send_keys('3BEPb1')
    # password_site = driver.find_element_by_name("pass")
    # password_site.send_keys('3BEPb120')
    # password_site.send_keys(Keys.ENTER)
    #
    # # обходим проверочный код
    # if check_exists_by_name("pass1") == True:
    #     password_opp = driver.find_element_by_name("pass1")
    #     password_opp.send_keys('F0eX1lf5NH')
    #     password_opp.send_keys(Keys.ENTER)
    #
    # driver.find_element_by_partial_link_text('Задания').click()
    # tak_id_input = driver.find_element_by_name("zd_name")
    # tak_id_input.send_keys('1342716')
    # tak_id_input.send_keys(Keys.ENTER)
    # driver.find_element_by_partial_link_text('КЛИКАТЬ на 4 баннер рекламы').click()

    # element = driver.find_element_by_xpath("//input[@type = 'submit']")
    # element.click()
    #
    # element = driver.find_element_by_xpath(
    #     "//input[@value='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Подтвердить выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']")
    # element.click()

    # < input
    # type = "submit"
    # value = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Начать выполнение задания&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    # style = "font-weight: bold;"
    # onclick = "setInterval(function fresh() {location.reload();} , 1000);" >


# task_1()
task_2()




# верхний баннер структура
# <div class="topic--list hidden-md hidden-sm hidden-xs" style="text-align: center">
#     <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
#     <!-- 1 и 2 пост -->
#     <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-6991603178769043" data-ad-slot="6340257014" data-adsbygoogle-status="done" data-ad-status="filled"><ins id="aswift_0_expand" style="display:inline-table;border:none;height:90px;margin:0;padding:0;position:relative;visibility:visible;width:728px;background-color:transparent;" tabindex="0" title="Advertisement" aria-label="Advertisement"><ins id="aswift_0_anchor" style="display:block;border:none;height:90px;margin:0;padding:0;position:relative;visibility:visible;width:728px;background-color:transparent;"><iframe id="aswift_0" name="aswift_0" style="left:0;position:absolute;top:0;border:0;width:728px;height:90px;" sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-top-navigation-by-user-activation" width="728" height="90" frameborder="0" src="https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-6991603178769043&amp;output=html&amp;h=90&amp;slotname=6340257014&amp;adk=1814655294&amp;adf=1920817249&amp;pi=t.ma~as.6340257014&amp;w=728&amp;lmt=1624988246&amp;psa=1&amp;format=728x90&amp;url=https%3A%2F%2Fkmory.ru%2Fviewforum.php%3Ff%3D219&amp;flash=0&amp;wgl=1&amp;uach=WyJXaW5kb3dzIiwiMTAuMCIsIng4NiIsIiIsIjkxLjAuNDQ3Mi4xMTQiLFtdLG51bGwsbnVsbCxudWxsXQ..&amp;tt_state=W3siaXNzdWVyT3JpZ2luIjoiaHR0cHM6Ly9hZHNlcnZpY2UuZ29vZ2xlLmNvbSIsInN0YXRlIjo2fSx7Imlzc3Vlck9yaWdpbiI6Imh0dHBzOi8vYXR0ZXN0YXRpb24uYW5kcm9pZC5jb20iLCJzdGF0ZSI6N31d&amp;dt=1624988245743&amp;bpp=8&amp;bdt=351&amp;idt=300&amp;shv=r20210624&amp;cbv=%2Fr20190131&amp;ptt=9&amp;saldr=aa&amp;abxe=1&amp;cookie=ID%3Dc1e9ccdc3d9cb979-2225f74a6ec80050%3AT%3D1624986658%3ART%3D1624986658%3AS%3DALNI_MaO0I7GK2lhBqAhe0UIJSsJnts57w&amp;correlator=8564851190323&amp;frm=20&amp;pv=2&amp;ga_vid=1090465500.1624986659&amp;ga_sid=1624986659&amp;ga_hid=1737971741&amp;ga_fc=1&amp;u_tz=180&amp;u_his=4&amp;u_java=0&amp;u_h=1080&amp;u_w=1920&amp;u_ah=1040&amp;u_aw=1920&amp;u_cd=24&amp;u_nplug=3&amp;u_nmime=4&amp;adx=470&amp;ady=45&amp;biw=1348&amp;bih=937&amp;scr_x=0&amp;scr_y=0&amp;eid=31060956%2C21067496%2C31061217%2C31061662&amp;oid=3&amp;pvsid=4276407149325271&amp;pem=122&amp;ref=https%3A%2F%2Fkmory.ru%2Fviewforum.php%3Ff%3D219&amp;eae=0&amp;fc=896&amp;brdim=0%2C0%2C0%2C0%2C1920%2C0%2C1920%2C1040%2C1365%2C937&amp;vis=1&amp;rsz=M%7C%7ClpeE%7Cp&amp;abl=XS&amp;pfx=0&amp;fu=0&amp;bc=31&amp;ifi=1&amp;uci=a!1&amp;fsb=1&amp;xpc=joFx59THfY&amp;p=https%3A//kmory.ru&amp;dtd=313" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" scrolling="no" allowfullscreen="true" trusttoken="{&quot;type&quot;:&quot;send-redemption-record&quot;,&quot;issuers&quot;:[&quot;https://adservice.google.com&quot;],&quot;refreshPolicy&quot;:&quot;none&quot;,&quot;signRequestData&quot;:&quot;include&quot;,&quot;includeTimestampHeader&quot;:true,&quot;additionalSignedHeaders&quot;:[&quot;sec-time&quot;,&quot;Sec-Redemption-Record&quot;],&quot;additionalSigningData&quot;:&quot;eyJ1cmwiOiJodHRwczovL2ttb3J5LnJ1L3ZpZXdmb3J1bS5waHA_Zj0yMTkifQ..&quot;}" allow="conversion-measurement" data-google-container-id="a!1" data-google-query-id="CLHVuvmwvfECFQQ-GwodU0MJxw" data-load-complete="true"></iframe></ins></ins></ins>
#     <script>
#         (adsbygoogle = window.adsbygoogle || []).push({});
#     </script>
# </div>





# Боковой баннер полная структура
# <div class="topic-list--content" style="height: 600px;">
#         <div class="topic-sidebar-widget">
# <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
# <!-- адаптив сайдбар -->
# <ins class="adsbygoogle" style="display: block; height: 600px;" data-ad-client="ca-pub-6991603178769043" data-ad-slot="7631919260" data-ad-format="auto" data-adsbygoogle-status="done" data-ad-status="filled"><ins id="aswift_1_expand" style="display:inline-table;border:none;height:600px;margin:0;padding:0;position:relative;visibility:visible;width:191px;background-color:transparent;" tabindex="0" title="Advertisement" aria-label="Advertisement"><ins id="aswift_1_anchor" style="display: block; border: none; height: 600px; margin: 0px; padding: 0px; position: relative; visibility: visible; width: 191px; background-color: transparent; overflow: visible;"><iframe id="aswift_1" name="aswift_1" style="left:0;position:absolute;top:0;border:0;width:191px;height:600px;" sandbox="allow-forms allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-top-navigation-by-user-activation" width="191" height="600" frameborder="0" src="https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-6991603178769043&amp;output=html&amp;h=600&amp;slotname=7631919260&amp;adk=2300311168&amp;adf=79525872&amp;pi=t.ma~as.7631919260&amp;w=191&amp;fwrn=4&amp;fwrnh=100&amp;lmt=1624988246&amp;rafmt=1&amp;psa=1&amp;format=191x600&amp;url=https%3A%2F%2Fkmory.ru%2Fviewforum.php%3Ff%3D219&amp;flash=0&amp;fwr=0&amp;rpe=1&amp;resp_fmts=4&amp;wgl=1&amp;uach=WyJXaW5kb3dzIiwiMTAuMCIsIng4NiIsIiIsIjkxLjAuNDQ3Mi4xMTQiLFtdLG51bGwsbnVsbCxudWxsXQ..&amp;tt_state=W3siaXNzdWVyT3JpZ2luIjoiaHR0cHM6Ly9hZHNlcnZpY2UuZ29vZ2xlLmNvbSIsInN0YXRlIjo2fSx7Imlzc3Vlck9yaWdpbiI6Imh0dHBzOi8vYXR0ZXN0YXRpb24uYW5kcm9pZC5jb20iLCJzdGF0ZSI6N31d&amp;dt=1624988245754&amp;bpp=6&amp;bdt=362&amp;idt=323&amp;shv=r20210624&amp;cbv=%2Fr20190131&amp;ptt=9&amp;saldr=aa&amp;abxe=1&amp;cookie=ID%3Dc1e9ccdc3d9cb979-2225f74a6ec80050%3AT%3D1624986658%3ART%3D1624986658%3AS%3DALNI_MaO0I7GK2lhBqAhe0UIJSsJnts57w&amp;prev_fmts=728x90&amp;correlator=8564851190323&amp;frm=20&amp;pv=1&amp;ga_vid=1090465500.1624986659&amp;ga_sid=1624986659&amp;ga_hid=1737971741&amp;ga_fc=1&amp;u_tz=180&amp;u_his=4&amp;u_java=0&amp;u_h=1080&amp;u_w=1920&amp;u_ah=1040&amp;u_aw=1920&amp;u_cd=24&amp;u_nplug=3&amp;u_nmime=4&amp;adx=1064&amp;ady=365&amp;biw=1348&amp;bih=937&amp;scr_x=0&amp;scr_y=0&amp;eid=31060956%2C21067496%2C31061217%2C31061662&amp;oid=3&amp;pvsid=4276407149325271&amp;pem=122&amp;ref=https%3A%2F%2Fkmory.ru%2Fviewforum.php%3Ff%3D219&amp;eae=0&amp;fc=896&amp;brdim=0%2C0%2C0%2C0%2C1920%2C0%2C1920%2C1040%2C1365%2C937&amp;vis=1&amp;rsz=%7C%7CoeE%7C&amp;abl=CS&amp;pfx=0&amp;fu=128&amp;bc=31&amp;ifi=2&amp;uci=a!2&amp;fsb=1&amp;xpc=KO7gKBgv9T&amp;p=https%3A//kmory.ru&amp;dtd=329" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" scrolling="no" allowfullscreen="true" trusttoken="{&quot;type&quot;:&quot;send-redemption-record&quot;,&quot;issuers&quot;:[&quot;https://adservice.google.com&quot;],&quot;refreshPolicy&quot;:&quot;none&quot;,&quot;signRequestData&quot;:&quot;include&quot;,&quot;includeTimestampHeader&quot;:true,&quot;additionalSignedHeaders&quot;:[&quot;sec-time&quot;,&quot;Sec-Redemption-Record&quot;],&quot;additionalSigningData&quot;:&quot;eyJ1cmwiOiJodHRwczovL2ttb3J5LnJ1L3ZpZXdmb3J1bS5waHA_Zj0yMTkifQ..&quot;}" allow="conversion-measurement" data-google-container-id="a!2" data-google-query-id="CIP_u_mwvfECFZWEhQodjLQCwA" data-load-complete="true"></iframe></ins></ins></ins>
# <script>
# (adsbygoogle = window.adsbygoogle || []).push({});
# </script>
#         </div>
#     </div>

# после обновления баннеры меняются (но не всегда)


# Отчет
# 1. ссылка с баннера В ШАПКЕ:
# https://www.bydom.by/dushevoe-oborudovanie/dushevie-kabiny-s-vannoy/?utm_source=google&utm_medium=cpm&utm_campaign=Remarketing&utm_content=Kabini_s_vannoy&utm_term=kmory.ru&gclid=EAIaIQobChMIsdW6-bC98QIVBD4bCh1TQwnHEAEYASAAEgInRPD_BwE
#
# 2 ссылка с баннера В КОЛОНКЕ СПРАВА:
# https://yandex.by/promo/direct/promocode/2?utm_source=GA_Network_Bel&utm_medium=GA_Network_Bel_Brand&utm_campaign=New_GA_Network_Bel_Brand&utm_content=509922165116&utm_term=&gclid=EAIaIQobChMIsr_w_7K98QIVSoSFCh0zWQbPEAEYASAAEgLS0fD_BwE


# возвращаемся на вкладку wmail.ru
# нажимаем на кнопку подтвердить выполнение задания
# повторное логирование
# задания №

