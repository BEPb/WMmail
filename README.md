![Profile views](https://gpvc.arturio.dev/BEPb) 
![GitHub top language](https://img.shields.io/github/languages/top/BEPb/WMmail) 
![GitHub language count](https://img.shields.io/github/languages/count/BEPb/WMmail)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BEPb/WMmail)
![GitHub repo size](https://img.shields.io/github/repo-size/BEPb/WMmail) 
![GitHub](https://img.shields.io/github/license/BEPb/WMmail) 
![GitHub last commit](https://img.shields.io/github/last-commit/BEPb/WMmail)

![GitHub User's stars](https://img.shields.io/github/stars/BEPb?style=social)

## Бот Wmail.ru

____
![](./wmmail.jpg)


В автоматическом режиме запускает приложение hrome под ОС windows, входит в аккаунт
wmail.ru, обходит валидацию. Выполняет все задания в раздел платные письма, на основе машинного
обучения с точностью 98% определяет капчи контроля бота, а также выполняет платное задание в по просмотру, 
с обходом похожей капчи, но уже из 5-ти цифр.

____
Цель проекта создать на основе машинного обучения анализ капчи и применить ее.

___
Содержание проекта:
- папка data - место хранения исходных капч (5 цифр)
- папка cropd capcha - место хранения отредактированной капчи
- папка output - место хранения обученной модели
- папка test - место хранения подготовленных к анализу капч (по 1 цифре)
- папка result analiz - место хранения уже проанализрованных цифр (каждая в свей папке).

- analiz_and_sort.ipynb - файл прогона анализа в google colab с результатами
- analiz_and_sort.py - файл анализа составлен в pycharm, но для того что бы не нагружать машину и время, адаптирован под colab
- data_collection.py - файл который собирал капчи, пользуясь уязвимостью WMmail
- main.py - стартовый бот, который использовал те же библиотке selenium, для тренировки
- mydatabase.db -  база на sqllite3 для сохранения результатов работы
- parcer.py - основной файл бота, который применяет обученную модель
- README.md - описание проекта
- task.py -  задания, выполняемый по отдельному алгоритму
- transform_captcha.py - преобразование исходной капчи и ее сохраниние для дальнейше обработки
- transform_captcha_step_2.py -  конечное преобразование капчи для анализа
____

Библиотеки применяемые в боте:
- selenium - основная библиотека работы с браузером и элементами сайта
- time - работа с временными переменными
- PIL, cv2 - работа с изображениями
- keras, argparse, pickle - машинное обучение капчи и ее применение

 
