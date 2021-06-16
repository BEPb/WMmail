# python3
# бот по просмотру писем и выполнению заданий

import cv2  # библиотека  OpenCV обработки изображений и видео
import os
from pathlib import Path
import sys
from PIL import Image


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
   # cropped_image = cv2.resize(cropped_image, (18, 60))  # изменяем размер одной цифры необх. для анализа
    cropped_image.save(saved_location)


def process_files(files):
    for file in files:
        with open(file, 'rb+') as file_opend:
            coords = (16, 0, 100, 40)
            print(file_opend)
            print(coords)
            print(result_dir)
            crop(file_opend, coords, result_dir)



# C:\Users\admin\PycharmProjects\WMmail\data\cropd_capcha
source_dir = r'C:\Users\admin\PycharmProjects\WMmail\data'
result_dir = r'/cropd_capcha'
os.chdir(source_dir) # смена текущей директории

files = os.listdir(path=".")
#print(files)
process_files(files)

# coords = (16, 0, 100, 40)  # Обрезка пяти цифр из общей капчи 115х40 (отрезаем лишние квадраты в начале и конеце капчи)
# coords_c1 = (0, 0, 16, 40)  # задаем координаты  цифры №1 17x40
# coords_c2 = (17, 0, 34, 40)  # задаем координаты  цифры №2 17x40
# coords_c3 = (35, 0, 51, 40)  # задаем координаты  цифры №3 17x40
# coords_c4 = (52, 0, 68, 40)  # задаем координаты  цифры №4 17x40
# coords_c5 = (69, 0, 85, 40)  # задаем координаты  цифры №5 17x40
#
# #            im = Image.open("capcha.png")  # uses PIL library to open image in memory
# #            im.save('screenshot.png')  # saves new cropped image
# crop("capcha.png", coords, 'crop_capcha.png')  # вырезаем 5 цифр
# time.sleep(2)
# crop('crop_capcha.png', coords_c1, 'number_c1.png') # вырезаем цифру №1
# crop('crop_capcha.png', coords_c2, 'number_c2.png') # вырезаем цифру №2
# crop('crop_capcha.png', coords_c3, 'number_c3.png')  # вырезаем цифру №3
# crop('crop_capcha.png', coords_c4, 'number_c4.png')  # вырезаем цифру №4
# crop('crop_capcha.png', coords_c5, 'number_c5.png')  # вырезаем цифру №5

