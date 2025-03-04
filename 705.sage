from sage.all import *
from sage.symbolic.integration.integral import definite_integral
import numpy as np
from sympy import lambdify, sympify
import sympy
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def printa(thing_to_print):
	print(ascii_art(thing_to_print))


r, u = var('r u', domain = 'positive')

intgrand = e ** ((i * x * r) - ((x ** 2) * u))
printa(intgrand)

printa(definite_integral(intgrand,x,-infinity,infinity))
