
# https://yadi.sk/d/cM0pZWFm3GfRdi - код игры, будет обновляться по ходу урока
# https://yadi.sk/d/K66JVkwO3GfRej - картинки к игре

# SublimeREPL  - плагин для SublimeText,
# который позволяет выполнять код Python'а сразу в Sublim'e


# Подключение модулей
import os

# Модуль tkinter - для создания GUI
from tkinter import *

from random import choice

# Для работы с графикой воспользуемся дополнительной библиотекой - PIL
# Необходимо установить библиотеку Pillow:  pip install Pillow
from PIL import Image, ImageTk


SIDE = 4        # <- величина стороны квадрата (для пятнашек квадрат 4х4)

# PEP8

# Создание собственной функции:

def cmd(event='x'):
    ''' Это тестовая функция.
        Она имеет один аргумент, у которого есть значение по умолчанию.

        Данная многострочная строка является частью кода Python
        и является строкой документации.
        Именно эта строка выдается функцией help()
    '''
    print('Я - простая функция')
    print('event=', event)
    # return - необязателен

# def <lambda> (e): key_press('r')

cmd('xxx')
cmd()


def make_mosaik(filename='test.jpg'):
    ''' Функция разбиения изображения на квадратики
        Возвращает список картинок-квадратиков ImageTk.PhotoImage
    '''
    image = Image.open(filename)
    regions = []
    pixels = image.width // SIDE
    for i in range(SIDE):
        for j in range(SIDE):
            x1 = j * pixels
            y1 = i * pixels
            x2 = j * pixels + pixels
            y2 = i * pixels + pixels
            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.load()
            regions.append(ImageTk.PhotoImage(region))

    return regions        


def grid_x(curr, near):
    ''' Отрисовка расположения двух клеток
    '''
    if near is not None:
        curr.grid(row=curr.row, column=curr.column)
        near.grid(row=near.row, column=near.column)


def exchange(curr, near):
    ''' Обмен местами клеток в общем списке
    '''
    if near is not None:
        ci = curr.row * SIDE + curr.column
        ni = near.row * SIDE + near.column
        labels[ci], labels[ni] = labels[ni], labels[ci]


def label_above(curr):
    ''' Вернуть соседа сверху
    '''
    pass        # <- nop - No Operation  ;;
    return labels[(curr.row-1)*SIDE + curr.column]


def label_under(curr):
    ''' Вернуть соседа снизу
    '''
    return labels[(curr.row+1)*SIDE + curr.column]


def label_left(curr):
    ''' Вернуть соседа слева
    '''
    return labels[curr.row*SIDE + curr.column - 1]


def label_right(curr):
    ''' Вернуть соседа справа
    '''    
    return labels[curr.row*SIDE + curr.column + 1]


# def key_press(btn):
#     pass
#     print(btn)


def key_press(btn):
    ''' Основная логика перемещения на игровом поле.
        Основной элемент логики - пустая клетка - от неё определяем соседа.
        Потом меняем координаты пустой клетки и соседа.
    '''
    near = None         # <- None - специальное значение в Питоне - "ничто"

    # Конструкция if..elif..elif..else заменяет в Питоне оператор выбора switch
    
    if btn == 'r' and curr.column > 0:
        # print('Вправо')
        near = label_left(curr)
        curr.column -= 1
        near.column += 1
    elif btn == 'l'and curr.column < SIDE - 1:
        # print('Влево')    
        near = label_right(curr)
        curr.column += 1
        near.column -= 1
    elif btn == 'u'and curr.row < SIDE - 1:
        # print('Вверх')
        near = label_under(curr)
        curr.row += 1
        near.row -= 1
    elif btn == 'd'and curr.row > 0:
        # print('Вниз')
        near = label_above(curr)
        curr.row -= 1
        near.row += 1

    exchange(curr, near)
    grid_x(curr, near)    


def mix_up():
    ''' Перемешивание клеток
        SIDE ** 4 - взято для лучшего перемешивания,
         т.к. не все вызовы функции нажатия кнопок
         будут приводить клеток к движению на поле
    '''
    buttons = ['d', 'u', 'l', 'r']
    for i in range(SIDE ** 5):
        x = choice(buttons)         # <- choice - функция из модуля random
        key_press(x)



# Списки можно создавать так:
# num_files = []
# for f in os.listdir('nums'):
#     num_files.append(os.path.join('nums', f))



# А можно так:

# Список имён файлов:
num_files = [os.path.join('nums', f) for f in os.listdir('nums')]

# print(num_files)


# Tcl/Tk

# Создаём главное окно приложения
main_window = Tk()

# Задаём заголовок окна
main_window.title('Пятнашки')

# Список объектов-картинок с числами:
nums = [PhotoImage(file=f) for f in num_files]

# Создание списка картинок мозаики
images = make_mosaik()
images[-1] = nums[-1]



# Создание Label-объекта (метка)
# label = Label(main_window, text="Нажми меня")
# label.bind('<Button-1>', cmd)
# label.pack()

# Создание и размещение Label-объектов:

labels = []

for i in range(SIDE):
    for j in range(SIDE):
        label = Label(main_window, image=images[i*SIDE + j])
        label.grid(row=i, column=j)
        label.x = i * SIDE + j
        label.row = i
        label.column = j
        # label.bind('<Button-1>', cmd)
        labels.append(label)

curr = labels[-1]




# Нажатия стрелок на клавиатуре привязываем к главному окну:
main_window.bind('<Right>', lambda e: key_press('r'))
main_window.bind('<Left>', lambda e: key_press('l'))
main_window.bind('<Up>', lambda e: key_press('u'))
main_window.bind('<Down>', lambda e: key_press('d'))



# time.sleep(2)

# Вызов функции через заданный интервал...

# Метод .after вызовет функцию mix_up через 2000 мс
main_window.after(2000, mix_up)

# Запуск главного цикла обработки сообщений графической оболочки:
main_window.mainloop()
