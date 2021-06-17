# python3
# цель - провести вторичную обработку капч из папки cropd_capcha в папку test обрезая кажду цифру под новым именем. Выполнено 17.06.2021
# в итоге получили 15281 номеров

import os
from PIL import Image


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)


source_dir = r'C:\Users\admin\PycharmProjects\WMmail\cropd_capcha'
result_dir = r'C:\Users\admin\PycharmProjects\WMmail\test'
os.chdir(source_dir)  # смена текущей директории
num = 1

def files(path):  # функция получения списка файлов в папке (текущем каталоге)
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


for file in files("."):
    print(file)
    curDir = os.getcwd()
    fn = curDir + "\\" + file
    result_file = result_dir + "\\" + str(num) + ".png"
    print(fn)
    coords_c1 = (0, 0, 16, 40)  # задаем координаты  цифры №1 17x40
    crop(file, coords_c1, result_file)

    num += 1
    result_file = result_dir + "\\" + str(num) + ".png"
    coords_c2 = (17, 0, 34, 40)  # задаем координаты  цифры №2 17x40
    crop(file, coords_c2, result_file)

    num += 1
    result_file = result_dir + "\\" + str(num) + ".png"
    coords_c3 = (35, 0, 51, 40)  # задаем координаты  цифры №3 17x40
    crop(file, coords_c3, result_file)

    num += 1
    result_file = result_dir + "\\" + str(num) + ".png"
    coords_c4 = (52, 0, 68, 40)  # задаем координаты  цифры №4 17x40
    crop(file, coords_c4, result_file)

    num += 1
    result_file = result_dir + "\\" + str(num) + ".png"
    coords_c5 = (69, 0, 85, 40)  # задаем координаты  цифры №5 17x40
    crop(file, coords_c5, result_file)
