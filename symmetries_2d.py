import numpy as np

import sympy as sp

n = sp.symbols('n')
#n = 5

L = 17

coord = np.array([n - (L * (n // L)), n // L, 1])

translation_left = np.array([[1, 0, L // 2], [0, 1, L // 2], [0, 0, 1]])
translation_right = np.array([[1, 0, -(L // 2)], [0, 1, -(L // 2)], [0, 0, 1]])

ident = np.identity(3)
rotate_90CCW = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
rotate_180CCW = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
rotate_270CCW = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

collapse = np.array([1, L, 0])

final = collapse @ translation_left @ rotate_270CCW @ translation_right @ coord


for i in range(288):
    f = final.subs(n, i)
    #r = ((17 * i) - (290 * (i // 17)) + 16)
    #r = 288 - i
    r = (-17 * i) + (290 * (i // 17)) + 272
    if not(f == r):
        print("Failed")

print(final)
