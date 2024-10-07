from PIL import Image
import matplotlib.pyplot as plt

# Создаем новое изображение размером 500x500 пикселей
image = Image.new('RGB', (500, 500))

# Задаем координаты центра окружности и ее радиус
x_center = 250
y_center = 220
radius = 47

def draw_circle(x, y, r):
    """
    Рисует окружность на изображении с помощью алгоритма средней точки.

    Args:
        x (int): Координата x центра окружности.
        y (int): Координата y центра окружности.
        r (int): Радиус окружности.
    """
    # Инициализируем начальные координаты и значение эррора
    x_t = -r
    y_t = 0
    error = (3 - 2 * r)

    # Цикл, повторяющийся до тех пор, пока y_t <= -x_t
    while y_t <= -x_t:
        # Ставим пиксели для всех 8 симметричных точек
        image.putpixel((x + x_t, y + y_t), (255, 255, 255))
        image.putpixel((x + y_t, y + x_t), (255, 255, 255))
        image.putpixel((x + x_t, y - y_t), (255, 255, 255))
        image.putpixel((x + y_t, y - x_t), (255, 255, 255))
        image.putpixel((x - x_t, y + y_t), (255, 255, 255))
        image.putpixel((x - y_t, y + x_t), (255, 255, 255))
        image.putpixel((x - x_t, y - y_t), (255, 255, 255))
        image.putpixel((x - y_t, y - x_t), (255, 255, 255))

        # Обновляем значение эррора
        if error < 0:
            error += 4 * y_t + 6
        else:
            error += 4 * x_t + 4 * y_t + 10
            x_t += 1
        y_t += 1

# Запрашиваем у пользователя ввод координат
print("Хотите ввести координаты? 1 - да, любой другой символ - нет")
user_input = input()

if user_input == "1":
    print("Вводите через пробел координаты центра (x y) и радиус (r):")
    try:
        x_center, y_center, radius = [int(x) for x in input().split()]
    except ValueError:
        print("Некорректный ввод. Введите три числа через пробел.")
        exit() 

# Рисуем окружность с заданными параметрами
draw_circle(x_center, y_center, radius)

# Отображаем полученное изображение с помощью matplotlib
plt.imshow(image)
plt.show()

