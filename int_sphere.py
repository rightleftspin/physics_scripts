import numpy as np

def find_integer_coordinates_in_sphere(diameter):
    radius = diameter / 2
    coords = []
    for x in range(-int(radius), int(radius) + 1):
        for y in range(-int(radius), int(radius) + 1):
            for z in range(-int(radius), int(radius) + 1):
                if x**2 + y**2 + z**2 <= radius**2:
                    coords.append((x, y, z))
    return coords

coords = find_integer_coordinates_in_sphere(18)

print(len(coords))
