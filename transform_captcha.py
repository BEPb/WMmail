# python3
# цель - провести начальную обработку капч из папки data в папку cropd_capcha обрезая лишние пустые поля.  Выполнено 17.06.2021

import os
from PIL import Image


def crop(image, coords, saved_location):  # функция обрезки
    image_obj = Image.open(image)
    cropped_image = image_obj.crop(coords)
   # cropped_image = cv2.resize(cropped_image, (18, 60))  # изменяем размер одной цифры необх. для анализа
    cropped_image.save(saved_location)


source_dir = r'C:\Users\admin\PycharmProjects\WMmail\data'
result_dir = r'C:\Users\admin\PycharmProjects\WMmail\cropd_capcha'
coords = (16, 0, 100, 40)
os.chdir(source_dir)  # смена текущей директории


def files(path):  # функция получения списка файлов в папке (текущем каталоге)
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


for file in files("."):
    print(file)
    curDir = os.getcwd()
    fn = curDir + "\\" + file
    result_file = result_dir + "\\" + file
    print(fn)
    crop(file, coords, result_file)




    #with open('capcha.png', 'wb') as f:
       # f.write(screenshot_as_bytes)

# def process_files(files):
#     for file in files:
#         with open(file, 'w+b') as file_opend:
#             coords = (16, 0, 100, 40)
#             print(file_opend)
#             print(coords)
#             print(result_dir)
#             myimage = Image.open(file)
#             myimage.load()
#             #crop(file_opend, coords, result_dir)


# print("Формат, Размер и тип изображения:")
# print(original.format, original.size, original.mode)

# file_opend = Image.open(fn)
# file_opend.show()


# try:
#     original = Image.open(fn)
# except FileNotFoundError:  # создаем обработчик ошибок, если файл не найден
#     print("Файл не найден")


# print(coords)
    # print(result_dir)

    #myimage = Image.open(file_opend)
    #myimage.load()




    # with open(file, 'w+b') as file_opend:
    #     coords = (16, 0, 100, 40)
    #     print(file_opend)
    #     print(coords)
    #     print(result_dir)
    #
    #     myimage = Image.open(file_opend)
    #     myimage.load()
    #     crop(file_opend, coords, result_dir)


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

