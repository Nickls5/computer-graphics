import matplotlib.pyplot as plt
import numpy as np

def cyrus_beck(p1, p2, clip_polygon):
    def compute_t_values(p, q, t_entry, t_exit): #Вычисляет значения t для входной и выходной точек.
        t_num = [q[i] - p[i] for i in range(2)]
        t_denom = [t_exit[i] - t_entry[i] for i in range(2)]

        t_values = [t_num[i] / t_denom[i] if t_denom[i] != 0 else float('inf') for i in range(2)]

        return t_values

    def is_inside(t_values):#Проверяет, находятся ли значения t в пределах от 0 до 1.
        return 0 <= t_values[0] <= 1 and 0 <= t_values[1] <= 1

    def clip_point(t, p1, p2):#Вычисляет точку на отрезке прямой для заданного значения t."""
        return [p1[i] + t * (p2[i] - p1[i]) for i in range(2)]

    n = len(clip_polygon)
    t_entry = [0] * 2
    t_exit = [1] * 2

    for i in range(n):
        normal = [-1 * (clip_polygon[(i + 1) % n][1] - clip_polygon[i][1]),
                  clip_polygon[(i + 1) % n][0] - clip_polygon[i][0]]

        D = np.dot(normal, [p2[0] - p1[0], p2[1] - p1[1]])

        if D == 0:  # Линия параллельна ребру
            if np.dot(normal, [p1[0] - clip_polygon[i][0], p1[1] - clip_polygon[i][1]]) < 0:
                return None  # Линия вне многоугольника
        else:
            t = -np.dot(normal, [p1[0] - clip_polygon[i][0], p1[1] - clip_polygon[i][1]]) / D

            if D > 0:  # Входное ребро
                t_entry = [max(t_entry[j], t) for j in range(2)]
            else:  # Выходное ребро
                t_exit = [min(t_exit[j], t) for j in range(2)]

    if t_entry[0] > t_exit[0] or t_entry[1] > t_exit[1]:
        return None  # Линия полностью вне многоугольника

    t_entry = max(t_entry)
    t_exit = min(t_exit)

    if t_entry > t_exit:
        return None  # Линия полностью вне многоугольника

    entry_point = clip_point(t_entry, p1, p2)
    exit_point = clip_point(t_exit, p1, p2)

    return entry_point, exit_point


def plot_polygon(ax, polygon, color='black'):#Рисует многоугольник.
    polygon.append(polygon[0])  # Замыкаем многоугольник
    polygon = np.array(polygon)
    ax.plot(polygon[:, 0], polygon[:, 1], color=color)


def plot_clipped_segments(ax, segments, clip_polygon):#Рисует отсеченные отрезки.
    for segment in segments:
        result = cyrus_beck(segment[0], segment[1], clip_polygon)
        if result:
            entry_point, exit_point = result
            ax.plot([segment[0][0], entry_point[0]], [segment[0][1], entry_point[1]], color='black')
            ax.plot([exit_point[0], segment[1][0]], [exit_point[1], segment[1][1]], color='black')


clip_polygon = [(3, 2), (7, 3), (7, 6), (5, 5), (3, 4)]
segments = [((1, 4), (8, 4)), ((4, 1), (4, 7)), ((1, 1), (8, 8)), ((2, 6), (6, 3))]

fig, ax = plt.subplots()

plot_polygon(ax, clip_polygon, color='green')


for segment in segments:
    ax.plot([segment[0][0], segment[1][0]], [segment[0][1], segment[1][1]], color='red')

plot_clipped_segments(ax, segments, clip_polygon)

ax.set_xlim(0, 9)
ax.set_ylim(0, 8)
ax.set_aspect('equal', adjustable='box')
plt.show()