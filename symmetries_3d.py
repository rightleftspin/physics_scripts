import numpy as np

import sympy as sp

def lev_civ(i,j,k):
    if i == j or j == k or i == k:
        return 0
    else:
        return (j-i)*(k-i)*(k-j)/abs(j-i)/abs(k-i)/abs(k-j)

def kron_del(i,j):
    if i == j:
        return 1
    else:
        return 0

def Rn(n,t):
    n /= np.linalg.norm(n)
    c = np.cos(t)
    s = np.sin(t)
    M = np.zeros((4,4))
    for i in range(3):
        for j in range(3):
            M[i,j] += kron_del(i,j)*c + (1-c)*n[i]*n[j] 
            for k in range(3):
                M[i,j] -= s*lev_civ(i,j,k)*n[k]
    M[-1,-1] = 1
    return M

def Pn(n):
    n /= np.linalg.norm(n)
    M = np.zeros((4,4))
    M[:3,:3] = np.identity(3) - 2*np.outer(n,n)
    M[-1,-1] = 1
    return M

def Tn(n):
    M = np.identity(4)
    M[0:3,-1] = n
    return M


n = sp.symbols('n')
L = sp.symbols('L')

coord = np.array([n - (L * (n // L)), 
                  (n // L) - (L * ((n //L) // L)), 
                  ((n // L) // L) - (L * (((n // L) // L) // L)), 
                  1
                  ])

#transform_to_basis = np.array([[0, 1 / 2, 1 / 2, 0], [1/2, 1/2, 0, 0], [1/2, 0, 1/2, 0], [0, 0, 0, 1]]) + np.array([[1, 0, 0, 1/4], [0, 1, 0, 1/4], [0, 0, 1, 1/4], [0, 0, 0, 1]])

#transform_back = np.linalg.inv(np.array([[0, 1 / 2, 1 / 2, 0], [1/2, 1/2, 0, 0], [1/2, 0, 1/2, 0], [0, 0, 0, 1]])) + np.array([[1, 0, 0, -1/4], [0, 1, 0, -1/4], [0, 0, 1, -1/4], [0, 0, 0, 1]]))

translation_left = np.array([[1, 0, 0, L // 2], [0, 1, 0, L // 2], [0, 0, 1, L // 2], [0, 0, 0, 1]])
translation_right = np.array([[1, 0, 0, -(L // 2)], [0, 1, 0, -(L // 2)], [0, 0, 1, -(L // 2)], [0, 0, 0, 1]])

x, y, z = np.array([1, 0, 0], dtype=np.float64), np.array([0, 1, 0], dtype=np.float64), np.array([0, 0, 1], dtype=np.float64)

# Identity
ident = np.identity(4)

# C2 - pi rotations about x, y and z axes
rotate_180X = Rn(x, np.pi)
rotate_180Y = Rn(y, np.pi)
rotate_180Z = Rn(z, np.pi)
c2 = [rotate_180X, rotate_180Y, rotate_180Z]

# C2' - pi rotation about x + y, x + z, y + z, cubic face diagonals
rotate_180xyp = Rn(x + y, np.pi)
rotate_180xzp = Rn(x + z, np.pi)
rotate_180yzp = Rn(y + z, np.pi)
rotate_180xym = Rn(x - y, np.pi)
rotate_180xzm = Rn(x - z, np.pi)
rotate_180yzm = Rn(y - z, np.pi)
c2p = [
        rotate_180xyp,
        rotate_180xzp,
        rotate_180yzp,
        rotate_180xym,
        rotate_180xzm,
        rotate_180yzm
        ]

# C3 - 2pi/3 rotations about 1, 1, 1 cubic body diagonals
rotate_2pi3pxpypz = Rn(x + y + z, 2 * np.pi / 3)
rotate_2pi3pxpymz = Rn(x + y - z, 2 * np.pi / 3)
rotate_2pi3pxmypz = Rn(x - y + z, 2 * np.pi / 3)
rotate_2pi3mxpypz = Rn(-x + y + z, 2 * np.pi / 3)
rotate_2pi3mxmypz = Rn(-x - y + z, 2 * np.pi / 3)
rotate_2pi3mxpymz = Rn(-x + y - z, 2 * np.pi / 3)
rotate_2pi3pxmymz = Rn(x - y - z, 2 * np.pi / 3)
rotate_2pi3mxmymz = Rn(-x - y - z, 2 * np.pi / 3)
c3 = [
    rotate_2pi3pxpypz,
    rotate_2pi3pxpymz,
    rotate_2pi3pxmypz,
    rotate_2pi3mxpypz,
    rotate_2pi3mxmypz,
    rotate_2pi3mxpymz,
    rotate_2pi3pxmymz,
    rotate_2pi3mxmymz
    ]

# C4 pi/2 rotation
rotate_90X = Rn(x, np.pi/2)
rotate_90Y = Rn(y, np.pi/2)
rotate_90Z = Rn(z, np.pi/2)
rotate_270X = Rn(x, 3 * np.pi/2)
rotate_270Y = Rn(y, 3 * np.pi/2)
rotate_270Z = Rn(z, 3 * np.pi/2)
c4 = [rotate_90X, rotate_90Y, rotate_90Z, rotate_270X, rotate_270Y, rotate_270Z]

# Inversion operator
inv = np.diag([-1, -1, -1, 1])

# Inversion times group operators
# S4 pi/2 rotation about x, y, z, then inversion
s4 = [inv @ x for x in c4]

# S6 pi/3 rotations about 1 1 1 cubic body diagonal, then reflection
s6 = [inv @ x for x in c3]

# sigma h reflection through the planes normal to the C4 rotations (rotate by c2, then flip)
sih = [inv @ x for x in c2]

# sigma d reflections through c2' rotations
sid = [inv @ x for x in c2p]

group = [[ident], c2, c2p, c3, c4, [inv], s4, s6, sih, sid]
full_group = []
for elem in group:
    full_group.extend(elem)

collapse = np.array([1, L, L ** 2, 0])
#print("[")
for i, elem in enumerate(full_group):
                 if sp.nsimplify(collapse @ translation_left @ elem @ translation_right @ coord, tolerance=1e-10,rational=True) != sp.nsimplify(collapse @ transform_back @ translation_left @ elem @ translation_right @ transform_to_basis @ coord, tolerance=1e-10,rational=True):
                    print("failed")
    #print(f"{sp.nsimplify(collapse @ translation_left @ elem @ translation_right @ coord, tolerance=1e-10,rational=True)},")

#print("]")
