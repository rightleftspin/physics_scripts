from sage.all import *
import numpy as np
from sympy import lambdify, sympify
import sympy
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
def printa(thing_to_print):
	print(ascii_art(thing_to_print))

delta, g_l, mu_b, B_x, alpha, rho, beta = var('delta g_l mu_b B_x alpha rho beta', domain='positive')

jz_m, jx_m, jy_m = var('jz_m jx_m jy_m', domain='positive')

wx, wz = var('wx wz', domain='real')

jz = Matrix(((-alpha, 0, 0), (0, alpha, 0), (0, 0, 0)))
jx = Matrix(((0, 0, rho), (0, 0, rho), (rho, rho, 0)))
jy = Matrix(((0, 0, -I * rho), (0, 0, I * rho), (I * rho, -I * rho, 0)))

v_c = Matrix(((0, 0, 0), (0, 0, 0), (0, 0, delta)))

full_hamil = v_c + -mu_b * g_l * B_x * jx + wx * jx_m * jx + wx * jy_m * jy + wz * jz_m * jz

jy_m = 0
alpha = 5.53 
wz = -5e-2 
rho = 2.34 
mu_b = 0.6717
g_l = 5/4
delta = 11.5

full_hamil = full_hamil.substitute(jy_m = jy_m, alpha = alpha, wz = wz, rho = rho, mu_b = mu_b, g_l = g_l, delta = delta)

####################
# B_x = 0 
#B_x = 0 
#wx = 0
#hamil = full_hamil.substitute(B_x = B_x, wx = wx)
#hamil_exp = exp(-beta * hamil)
#
#Z = hamil_exp.trace()
#mag = (1/Z) * (((jz.substitute(alpha = alpha) * hamil_exp).trace()))
#
## Convert to numpy callable
#mag_func = fast_callable(mag - jz_m, vars=[jz_m, beta])
#
#step = 0.001
#temp, jz_m = np.meshgrid(srange(step, 2, step), srange(0.01, 6, step))
#
#mag_out = mag_func(jz_m, 1/temp)
#
#matching_mask = (abs(mag_out) < 1e-4)
#
#mag_func_output = [temp[matching_mask], jz_m[matching_mask]]
#
#plt.plot(mag_func_output[0], mag_func_output[1], 'k.')
#plt.xlabel("T (K)")
#plt.ylabel("m")
#plt.title("<j_z> @ B_x=0")
#plt.savefig('j_z_b_0.pdf')

####################
# B_x = 2 
B_x = 2 
wx = 0

hamil = -beta * full_hamil.substitute(B_x = B_x, wx = wx)

step = 0.01
jz_m_array, temp_array = srange(step, 3, step), srange(step, 1.25, step)
jz_m_mesh, temp_mesh = np.meshgrid(jz_m_array, temp_array)
all_hamils = []

for temp in temp_array:
	row = []
	for jz_m in jz_m_array:
		row.append(hamil.substitute(beta=1/temp, jz_m=jz_m))
	all_hamils.append(row)

all_hamils_exp = sp.linalg.expm(np.array(all_hamils))

mags_z = ((1/np.einsum('...ii->...', all_hamils_exp)) * np.einsum('ij, lkji->lk', jz.substitute(alpha=alpha), all_hamils_exp))
mags_x = ((1/np.einsum('...ii->...', all_hamils_exp)) * np.einsum('ij, lkji->lk', jx.substitute(rho=rho), all_hamils_exp))

mag_out = abs(mags_z - jz_m_mesh) < 5e-4

plt.plot(temp_mesh[mag_out], jz_m_mesh[mag_out], 'k.', label='<j_z>')
plt.plot(temp_mesh[mag_out], mags_x[mag_out], 'r.', label='<j_x>')
plt.xlabel("T (K)")
plt.ylabel("m")
plt.title("<j_z> and <j_x> @ B_x=2")
plt.legend()
plt.savefig('j_z_b_2.pdf')
