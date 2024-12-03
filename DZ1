import numpy as np
import time
from threading import Thread
import pygame
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

def create_polygon_image(vertices, shape=(1000, 1000)):
    time1 = time.time()
    fig, ax = plt.subplots()
    fig.set_size_inches(shape[0] / fig.dpi, shape[1] / fig.dpi)
    ax.set_xlim(0, shape[1])
    ax.set_ylim(0, shape[0])
    ax.invert_yaxis()
    ax.axis('off')

    # Рисуем многоугольник
    polygon = Polygon(vertices, closed=True, edgecolor='black', facecolor='white')
    ax.add_patch(polygon)

    # Преобразуем в массив
    canvas = FigureCanvas(fig)
    canvas.draw()
    image = np.frombuffer(canvas.buffer_rgba(), dtype='uint8').reshape(shape[0], shape[1], 4)
    plt.close(fig)
    time2 = time.time()
    print(f"Polygon created in {time2 - time1:.4f} seconds")
    return image[:, :, :3].copy()

def is_background(color, threshold=68):
    # Считаем белыми пиксели с яркостью выше 68
    return np.mean(color) > threshold

def boundary_fill(image, x, y, fill_color):
    counter = 0
    time1 = time.time()
    if not is_background(image[x, y]):
        return

    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()
        if is_background(image[cx, cy]):
            image[cx, cy] = fill_color

            counter += 1
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < image.shape[0] and 0 <= ny < image.shape[1] and is_background(image[nx, ny]):
                    stack.append((nx, ny))

    time2 = time.time()
    differ = (time2 - time1) * 10000
    print(f"Polygon fill completed in {differ / 10000:.4f} seconds")
    print(f"Filled pixels count: {counter}")
    print(f"Fill speed: {counter / (differ / 10000):.2f} pixels/sec")

def draw_circle(radius, x, y):
    time1 = time.time()
    glBegin(GL_LINE_LOOP)
    for i in range(radius):
        angle = 2 * 3.14159 * i / radius
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()
    time2 = time.time()
    print(f"Circle outline drawn in {time2 - time1:.4f} seconds")
    
def fill_circle(radius, x, y):
    time1 = time.time()
    glBegin(GL_TRIANGLE_FAN)
    for i in range(radius):
        angle = 2 * 3.14159 * i / radius
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
        pixel_num = abs(3.14159 * radius * radius)//1
    glEnd()
    time2 = time.time()
    differ = (time2 - time1) * 10000
    print(f"Circle fill completed in {differ / 10000:.4f} seconds")
    print(f"Estimated pixels in filled circle: {pixel_num}")
    print(f"Fill speed: {pixel_num / (differ / 10000):.2E} pixels/sec")

def pyopengl():

    width, height = 10000, 10000
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    glOrtho(0, width, height, 0, -1, 1)

    radius = 4000
    x, y = 5000, 5000

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    draw_circle(radius, x, y)

    fill_circle(radius, x, y)

def our_method():
    vertices = []
    num_vertices = random.randint(3, 15)  # Рандомное число вершин от 3 до 15

    # Определяем вершины многоугольника
    for _ in range(num_vertices):
        x = random.randint(1, 1000)
        y = random.randint(1, 1000)
        vertices.append((x, y))
        
    image = create_polygon_image(vertices)

    fill_color = np.array([150, 0, 0], dtype=np.uint8)

    # Убираем темные серые пиксели между границей и заливкой
    gray_threshold = 100
    image[np.all((image[:, :, 0] < gray_threshold) & 
                (image[:, :, 1] < gray_threshold) & 
                (image[:, :, 2] < gray_threshold), axis=-1)] = [255, 255, 255]

    # Применяем Boundary Fill с начальной точкой внутри многоугольника
    boundary_fill(image, 50, 50, fill_color)
    
if __name__ == "__main__":
    our_method()
    pyopengl()
    Thread(target=our_method).start()
    Thread(target=pyopengl).start()
