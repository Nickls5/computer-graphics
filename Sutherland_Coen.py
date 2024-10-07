import matplotlib.pyplot as plt

# Коды для классификации конечных точек отрезка
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def compute_outcode(x, y, xmin, ymin, xmax, ymax):#Вычисляет код для точки относительно прямоугольника.
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):#Aлгоритм отсечения отрезков прямой по алгоритму Сазерленда-Коэна.
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        # Оба конца отрезка внутри окна
        if outcode1 == INSIDE and outcode2 == INSIDE:
            accept = True
            break
        # Оба конца отрезка вне окна, отрезок полностью наружу
        elif (outcode1 & outcode2) != 0:
            break
        else:
            # Выбираем конец отрезка, который находится снаружи окна
            outcode_out = outcode1 if outcode1 != INSIDE else outcode2

            # Находим пересечение отрезка с границами окна
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Обновляем координаты отрезка, которые находятся снаружи окна
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        plt.plot([x1, x2], [y1, y2], color='blue')
    else:
        print("Отрезок полностью находится вне окна")

xmin, ymin, xmax, ymax = 5, 15, 75, 55

x1, y1, x2, y2 = 1, 25, 90, 45
x3, y3, x4, y4 = 40, 65, 60, 10

plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], color='#f75216', linestyle='--')

plt.plot([x1, x2], [y1, y2], color='green', label='Исходный отрезок 1')
plt.plot([x3, x4], [y3, y4], color='orange', label='Исходный отрезок 2')

cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax)
cohen_sutherland(x3, y3, x4, y4, xmin, ymin, xmax, ymax)

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Отсечение отрезков Сазерленда-Коэна')
plt.legend()
plt.grid(True)
plt.show()

