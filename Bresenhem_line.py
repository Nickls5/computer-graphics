from PIL import Image
import matplotlib.pyplot as plt

# Размер изображения
canvas_size = 500

# Создание пустого изображения
image = Image.new('RGB', (canvas_size, canvas_size))

# Начальные координаты
start_x = 350
start_y = 60
end_x = 1
end_y = 320

def draw_line(x1, y1, x2, y2):
    """Рисует линию на изображении с помощью алгоритма Брезенхэма."""
    # Определение направления движения по осям
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    #  Первое значение эррора
    error = (dx > dy) * (-dx) + (dx <= dy) * (dy)
    
    # Цикл для прорисовки линии
    while True:
        # Проверка на выход за пределы изображения
        if x1 < 0 or x1 >= canvas_size or y1 < 0 or y1 >= canvas_size:
            break
        
        # Помещение пикселя в заданных координатах
        image.putpixel((y1, x1), (255, 255, 255))
        
        # Проверка на достижение конечной точки
        if x1 == x2 and y1 == y2:
            break
        
        # Вычисление следующего пикселя
        e2 = 2 * error
        
        # Выбор следующего пикселя по алгоритму Брезенхэма
        if e2 > -dx:
            error -= dy
            x1 += sx
        if e2 < dy:
            error += dx
            y1 += sy

# Запрос на ввод координат
print("Хотите ввести координаты? 1 - да, любой другой символ - нет")
choice = input()

if choice == "1":
    print("Введите 4 координаты: ")
    start_x, start_y, end_x, end_y = map(int, input().split())

# Вызов функции рисования
draw_line(start_x, start_y, end_x, end_y)

# Показ изображения
plt.imshow(image)
plt.show()

