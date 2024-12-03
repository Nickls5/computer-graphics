import matplotlib.pyplot as plt
import numpy as np

def fill_polygon(vertices, fill_color='red', edge_color='black'):
    # Создание пустого поля
    x_min, x_max = min(vertices[:, 0]), max(vertices[:, 0])
    y_min, y_max = min(vertices[:, 1]), max(vertices[:, 1])
    
    # Список для заполнения
    fill_points = []
    
    # Проход по горизонтальным линиям
    for y in range(int(y_min), int(y_max) + 1):
        intersections = []
        
        # Находим пересечения с рёбрами
        for i in range(len(vertices)):
            v1, v2 = vertices[i], vertices[(i + 1) % len(vertices)]
            if (v1[1] > y) != (v2[1] > y):  # Проверка пересечения
                x = (v2[0] - v1[0]) * (y - v1[1]) / (v2[1] - v1[1]) + v1[0]
                intersections.append(x)
        
        # Сортируем пересечения
        intersections.sort()
        
        # Заполняем область
        for i in range(0, len(intersections), 2):
            for x in range(int(intersections[i]), int(intersections[i + 1]) + 1):
                fill_points.append((x, y))
    
    return fill_points

# Вершины многоугольника
vertices = np.array([(1, 1), (5, 0.5), (4, 4), (2, 3), (1, 4)])
fill_points = fill_polygon(vertices)

# Визуализация
plt.fill(vertices[:, 0], vertices[:, 1], color='lightgrey', edgecolor='black', linewidth=1)  # Многоугольник
plt.scatter(*zip(*fill_points), color='red', s=2, label="Точки заполнения")  # Точки заполнения

plt.xlim(0, 6)
plt.ylim(0, 5)
plt.gca().set_aspect('equal', adjustable='box')  # Одинаковое соотношение осей
plt.legend()
plt.title("Заполнение многоугольника методом горизонтального сканирования")
plt.show()
