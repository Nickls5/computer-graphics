from PIL import Image
from z_buffer import point3, fill3D, update_buffer, draw_buffer, get_plane

# Класс для определения 3D-точки
class point3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

# Функция для расчета рассеянного света
def diffuse_light(light_point, point, color, A, B, C):
	# Направление света
	light_direction = point3(light_point.x - point.x, light_point.y - point.y, light_point.z - point.z)
	# Расчет интенсивности света
	light = (light_direction.x * A + light_direction.y * B + light_direction.z * C) / ((light_direction.x**2 + light_direction.y**2 + light_direction.z**2)**0.5) / ((A**2 + B**2 + C**2)**0.5)
	if light < 0:  # Если интенсивность отрицательная, то света нет
		light = 0

	# Цвет рассеянного света
	diffuse_light = point3(light * color[0] * 1, light * color[1] * 1, light * color[2] * 1)
	return diffuse_light

# Функция для расчета бликов
def specular_light(view_point, normal, light_point, point, color):
	# Нормализация нормали
	norm = point3(normal[0] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5,
				  normal[1] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5,
				  normal[2] / (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5)
	# Направление света
	light_direction = point3(light_point.x - point.x, light_point.y - point.y, light_point.z - point.z)
	# Скалярное произведение для расчета отражения
	scalar = norm.x * light_direction.x + norm.y * light_direction.y + norm.z * light_direction.z

	# Направление отраженного света
	reflection_point = point3(2 * norm.x * scalar - light_direction.x,
							  2 * norm.y * scalar - light_direction.y,
							  2 * norm.z * scalar - light_direction.z)

	# Интенсивность блика
	light = (reflection_point.x * view_point.x + reflection_point.y * view_point.y + reflection_point.z * view_point.z) / ((reflection_point.x**2 + reflection_point.y**2 + reflection_point.z**2)**0.5) / ((view_point.x**2 + view_point.y**2 + view_point.z**2)**0.5)
	light *= (light_direction.x * norm.x + light_direction.y * norm.y + light_direction.z * norm.z) / ((light_direction.x**2 + light_direction.y**2 + light_direction.z**2)**0.5) / ((norm.x**2 + norm.y**2 + norm.z**2)**0.5)

	# Цвет блика
	specular_light = point3(light * color[0] * 1, light * color[1] * 1, light * color[2] * 1)
	return specular_light

# Функция для отображения освещения
def draw_light(image, points, color, z_buffer, light_point, norm):
	for point in points:
		# Проверяем Z-буфер
		if point.z <= z_buffer[800 * point.y + point.x]:
			# Расчет рассеянного света
			lightd = diffuse_light(light_point, point, color, norm[0], norm[1], norm[2])
			# Расчет бликов
			lights = specular_light(point3(400, 300, 0), norm, light_point, point, color)
			# Отображение света на пикселе
			image.putpixel((int(point.x), int(point.y)), (int(lightd.x + lights.x), int(lightd.y + lights.y), int(lightd.z + lights.z)))

if __name__ == '__main__':
	# Измененные вершины первого треугольника
	vertexes1 = [
		point3(250, 250, 120),  # Смещение ближе к центру и изменение высоты
		point3(400, 350, 150),
	 	point3(520, 180, 280)
	]

	# Измененные вершины второго треугольника
	vertexes2 = [
		point3(180, 120, 50),   # Смещение ближе к нижней части
		point3(380, 450, 220),
		point3(530, 210, 180)
	]

	# Открываем изображение
	with Image.open('light.png') as im:
		# Очищаем изображение (черный фон)
		im.paste((0, 0, 0), (0, 0, im.size[0], im.size[1]))

		# Создаем Z-буфер
		z_buffer = [1000] * 800 * 600

		# Заполняем треугольники
		points1 = fill3D(vertexes1)
		points2 = fill3D(vertexes2)

		# Обновляем Z-буфер
		update_buffer(points1, z_buffer)
		update_buffer(points2, z_buffer)

		# Отрисовываем освещение (зеленый и синий цвета)
		draw_light(im, points2, (0, 0, 255), z_buffer, point3(400, 300, 50), get_plane(vertexes2[0], vertexes2[1], vertexes2[2]))
		draw_light(im, points1, (0, 255, 0), z_buffer, point3(400, 300, 50), get_plane(vertexes1[0], vertexes1[1], vertexes1[2]))
		
		# Сохраняем итоговое изображение
		im.save('light_with_spec_new_coords.png')
