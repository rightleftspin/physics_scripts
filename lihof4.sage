from sage.all import *
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

full_hamil = v_c + -B_x * jx + wx * jx_m * jx + wx * jy_m * jy + wz * jz_m * jz

# For B_x = 0
Z = exp(-beta * full_hamil.substitute(jx_m = 0, jy_m = 0, B_x = 0)).trace()

mag = ((1/Z) * (jz * exp(-beta * full_hamil.substitute(jx_m = 0, jy_m = 0, B_x = 0))).trace()).substitute(alpha = 5.53, wz = -5e-2, delta=11.5)

mag_func(jz_m, beta) = mag - jz_m

mag_func_output = [[], []]

for j in srange(0, 6, 0.01):
	for t in srange(0.01, 2, 0.01):
		if abs(mag_func(j, (1/t))) < 1e-6:
			mag_func_output[0].append(t)
			mag_func_output[1].append(j)

plt.plot(mag_func_output[0], mag_func_output[1], 'k.')
plt.savefig('m_plot.pdf')

