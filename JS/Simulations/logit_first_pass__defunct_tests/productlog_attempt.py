import matplotlib.pyplot as plt
import sympy as np
import numpy as sp
from sympy.solvers import solve
from sympy import Symbol,S
# In this particular draft, I'll take a stab at using the previously defined productlog expression I've already defined. This involves using the Lambert W function, which is a scipy package. 
from scipy.special import lambertw
w = lambertw(1)
print(w)
# What does this mean? Namely, the value of W(z) is such that z = W(z) * exp (W(z)) for any complex number z. That is, it is the solution for z=1: z = w exp(w). Since we have 1, this occurs for 0.567143. 
#
# We now move to the case of interest from the previous derivation from Mathematica. I arrived at the following expression for the optimal price set by insurer $i$. A HUGE item to note is that Mathematica's notation is productlog[k,z], whereas SciPy's notation is productlog[z,k].
# The Mathematica solution is ProductLog[C_1,(e^{-1+v+\alpha p_j - \alpha \phi_i})/(e^v+e^{\alpha*p_j})], where C_1 is the k of choice. We simply swap these around. I'll choose k=0 for now: the default from SciPy. The notation is then lambertw((e^{-1+v+\alpha p_j - \alpha \phi_i})/(e^v+e^{\alpha*p_j})). I first define our parameters of interest, and then define price. 
v = 0
alpha = 0.5
priceJ = Symbol('priceJ')
phiI = Symbol('phiI')
priceI = (1 + lambertw((sp.exp(-1 + v + alpha * priceJ - alpha * phiI)) / (sp.exp(v) + sp.exp(alpha * pJ)), k = 0) + alpha * phiI) / alpha
print(priceI)
# Error: loop of ufunc does not support argument 0 of type Add which has no callable exp method.
# I'm completely lost here. This is probably stemming from my use of a ton of symbols in an already complicated expression. I likely need to iterate this over each of these items. 