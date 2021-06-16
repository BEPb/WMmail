# python 3.9
# программа для сбора капч (данных) для машинного обучения, используется уязвимость wmmail после обновления страницы - меняется капча
# цель собрать достаточно капч (4000) для тренировки в папку data.  Выполнено 16.06.2021

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

def check_exists_by_name(name):  # проверка на наличие соответсвующего имени
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True



def main():
    global driver, number_of_letters, amount_of_money
    driver = webdriver.Chrome(r"C:\Users\admin\Downloads\chromedriver.exe")  # место расположения chromedriver.exe REDMEBOOK

    #driver = webdriver.Chrome(r"C:\Users\andre\Downloads\chromedriver_win32\chromedriver.exe")  # место расположения chromedriver.exe
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
    for a in range(2976, 4000):
        driver.switch_to.window(driver.window_handles[1])  # переход в окно 1
        elements = driver.find_elements_by_xpath('//img[@src]')

        for element in elements:   # во множестве ссылок выбираем именно нашу капчу
            url_capcha = element.get_attribute("src")
            if url_capcha[0:53] == 'http://www.wmmail.ru/index.php?cf=reg-lostpassnum&rnd':
                screenshot_as_bytes = element.screenshot_as_png
                with open('capcha.png', 'wb') as f:
                    f.write(screenshot_as_bytes)

                im = Image.open("capcha.png")  # uses PIL library to open image in memory
                im.save(r'C:\Users\admin\PycharmProjects\WMmail\data\screenshot'+ str(a) + '.png')  # saves new cropped image

        driver.refresh()  # обновить страницу


    print('Done')

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()


if __name__ == "__main__":
    main()