import numpy as np
from sympy.interactive import printing
printing.init_printing(use_latex=True)
import sympy as sp

delta = sp.symbols('delta')

func = sp.sin(sp.cos(sp.tan(delta)))

diul = sp.diff(func,delta)

print(diul)