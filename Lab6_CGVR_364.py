import numpy as np
import matplotlib.pyplot as plt

width = 800
height = 600

z_buffer = np.full((height, width), np.inf)
color_buffer = np.ones((height, width, 3))

def draw_triangle(vertices, color):
    x1, y1, z1 = vertices[0]
    x2, y2, z2 = vertices[1]
    x3, y3, z3 = vertices[2]

    min_x = max(0, int(min(x1, x2, x3)))
    max_x = min(width - 1, int(max(x1, x2, x3)))
    min_y = max(0, int(min(y1, y2, y3)))
    max_y = min(height - 1, int(max(y1, y2, y3)))

    denominator = ((y2 - y3) * (x1 - x3) +
                   (x3 - x2) * (y1 - y3))

    if denominator == 0:
        return

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):

            a = ((y2 - y3) * (x - x3) +
                 (x3 - x2) * (y - y3)) / denominator

            b = ((y3 - y1) * (x - x3) +
                 (x1 - x3) * (y - y3)) / denominator

            c = 1 - a - b

            if a >= 0 and b >= 0 and c >= 0:

                z = a * z1 + b * z2 + c * z3

                if z < z_buffer[y, x]:
                    z_buffer[y, x] = z
                    color_buffer[y, x] = color

triangle1 = [
    (150, 100, 5),
    (650, 150, 5),
    (400, 550, 5)
]

triangle2 = [
    (200, 200, 2),
    (700, 250, 2),
    (450, 580, 2)
]

draw_triangle(triangle1, [0, 0, 1])
draw_triangle(triangle2, [1, 0, 0])

plt.figure(figsize=(10, 7))
plt.imshow(color_buffer, origin="lower")
plt.title("Z-Buffer Algorithm - Hidden Surface Removal")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.axis("on")
plt.show()