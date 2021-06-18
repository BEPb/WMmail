# python3
# цель - провести анализ всех полученных 15281 файла и разложить их по папкам с сответствующими номерами. Выполнено 18.06.2021
# данных скрипт адаптирован к запуску на google colab на один файл требуется около 3 секунд,
# (((15281х3)/60)/60) итого 12,73 часа на всю папку
# страница выгрузки в блокнот google colab под именем analiz_and_sort.ipynb

import os
from PIL import Image
import argparse
import cv2
import pickle
from keras.models import load_model

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
    #output = image.copy()

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
    os.chdir(work_dir)
    model = load_model(args["model"])
    lb = pickle.loads(open(args["label_bin"], "rb").read())
    os.chdir(source_dir)

    # делаем предсказание на изображении
    preds = model.predict(image)

    # находим индекс метки класса с наибольшей вероятностью
    # соответствия
    i = preds.argmax(axis=1)[0]

    label = lb.classes_[i]
    text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
    print(text)  # значение + процент
    #print(preds[0][i] * 100)
    # if (preds[0][i] * 100) <= 90:
    #     label = 'others'
    #     print(label)
    return label

##### for redmebook
# source_dir = r'C:\Users\admin\PycharmProjects\WMmail\test'
# result_dir = r'C:\Users\admin\PycharmProjects\WMmail\result_analiz'
# work_dir = r'C:\Users\admin\PycharmProjects\WMmail'

#### for google colab
source_dir = r'/content/WMmail/test'
result_dir = r'/content/WMmail/result_analiz'
work_dir = r'/content/WMmail'


label = 'others'

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

    image_obj = Image.open(file)
    width = 18
    height = 60
    resized_img = image_obj.resize((width, height), Image.ANTIALIAS)  # изменяем размер одной цифры необх. для анализа


    capcha_analiz(file)

    #result_file = result_dir + "\\" + str(label) + "\\" + str(num) + ".png"  # for redmebook
    result_file = result_dir + "/" + str(label) + "/" + str(num) + ".png"  # for google colab

    resized_img.save(result_file)
    num += 1

