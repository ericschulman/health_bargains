import matplotlib.pyplot as plt
import sympy as np
import numpy as sp
from sympy.solvers import solve
from sympy import Symbol,S
from matplotlib import rc
# rc('font',**{'family':'serif','serif':['Palatino']})
# rc(text',usetex=True)
# Defining parameters
v = 0
alpha = 0.5
lambda1 = 5
beta = 0.5
costH = 0
# First test: linear demand case. 
# We define market share $s_i$ to proceed this way. With linear demand, we have the Hotelling model solution. We include the price here, since price is rather easy to find in closed form in this linear case. However, when we move to logit, this is no longer the case. I let insurer 1 correspond to insurer i, and insurer 2 correspond to insurer j without loss. 
Phi1 = Symbol('Phi1', real = True)
Phi2 = Symbol('Phi2', real = True)
p1 = Symbol('p1', real = True)
p2 = Symbol('p2', real = True)
# Since we already have the optimal prices in closed form, the inclusion of p1 and p2 as symbols isn't entirely necessary. This approach is simply for generality for the logit case. 
optimalPrice1 = (2 * Phi1 + Phi2) / 3 + lambda1
optimalPrice2 = (2 * Phi2 + Phi1)/ 3 + lambda1
marketshareLinear1 = (1 + (1 / lambda1) * (optimalPrice2 - optimalPrice1)) / 2 #(p2 - p1)) / 2 would be the case used for logit, since we haven't determined p1 or p2 in that case. 
marketshareLinear2 = (1 + (1 / lambda1) * (optimalPrice1 - optimalPrice2)) / 2 #(p1 - p2)) / 2
# Defining profit functions for insurers  1 ($i$) and 2 ($j$), and the hospital $h$. 
profitInsurer1 = marketshareLinear1 * (optimalPrice1 - Phi1)
profitInsurer2 = marketshareLinear2 * (optimalPrice2 - Phi2)
profitHospital = (Phi1 - costH) * marketshareLinear1 + (Phi2 - costH) * marketshareLinear2
# Maximizing these profit functions for insurers leads to the optimal price selection $p1$ and $p2$ in terms of $Phi1$ and $Phi2$. This gives us expressions in terms of $Phi1$ and $Phi2$ to plug into the NiN bargaining function in the next section. This isn't entirely necessary in the linear case, since we already have closed form expressions in the form of optimalPrice1 and optimalPrice 2, but this should work great for the logit case in an approach similar to the one detailed below. 

# Defining disagreement function $\Pi_h(\mathcal{G}\setminus i)$ before proceeding to NiN. I begin with the case of zero recapture, passive beliefs. Namely, if there is a disagreement, the other hospital only captures the market share they previously anticipated. 
disagreementHospital1 = marketshareLinear2 * (Phi2 - costH)
disagreementHospital2 = marketshareLinear1 * (Phi1 - costH)
# The following is the NiN bargaining function for insurer 1. They choose Phi1, which is the element of this function. The function itself, however, parses over Phi2 as a best-response to it. 
# # # maxReimbursement1 = 50
# # # maxReimbursement2 = 50
# # # def NiNFunc1(Phi2): 
# # #     # Capping maximum reimbursement Phi1 at 50 should be sufficient, along with 1000 partitions. 
# # #     reimbursementRange1 = sp.linspace(0,maxReimbursement1,num=1000) 
# # #     # This is really nasty coding practice, but bear with me. This is the objective function for insurer 1 via the Nash-in-Nash bargaining function.  
# # #     f1 = lambda Phi1: ((profitInsurer1)**(beta)) * (profitHospital - disagreementHospital1) ** (1-beta)
# # #     # This is the argmax of the objective function for insurer 1.
# # #     opt1 = max(reimbursementRange1,key=f1)
# # #     if opt1 <= 0: 
# # #         return 0
# # #     if opt1 >= maxReimbursement1:
# # #         return maxReimbursement1
# # #     else:
# # #         return opt1
# # #     return opt1
# # # def NiNFunc2(Phi1):
# # #     # Capping maximum investment at 50 should be sufficient, along with 1000 partitions. 
# # #     reimbursementRange2 = sp.linspace(0,maxReimbursement2,num=1000) 
# # #     # This is really nasty coding practice, but bear with me. This is the objective function for insurer 1 via the Nash-in-Nash bargaining function.  
# # #     f2 = lambda Phi2: ((profitInsurer2)**(beta)) * (profitHospital - disagreementHospital1) ** (1-beta)
# # #     # This is the argmax of the objective function for insurer 1.
# # #     opt2 = max(reimbursementRange2,key=f2)
# # #     if opt2 <= 0: 
# # #         return 0
# # #     if opt2 >= maxReimbursement2:
# # #         return maxReimbursement2
# # #     else:
# # #         return opt2
# # #     return opt2
# # # def plotfunc():
# # #     # The domain for insurer 1 is the best response to any possible reimbursement by insurer 2.
# # #     x1 = list(sp.arange(0,maxReimbursement2+0.01,0.01))
# # #     # The domain for insurer 2 is the best response to any possible reimbursement by insurer 1.
# # #     x2 = list(sp.arange(0,maxReimbursement1+0.01,0.01))
# # #     # Mapping from the domain for insurer 1 to their best-response.
# # #     y1 = list(map(NiNFunc1,x1))
# # #     # Mapping from the domain for insurer 2 to their best-response.
# # #     y2 = list(map(NiNFunc2,x2))
# # #     # Plot for 1's best-response. 
# # #     plt.plot(x1,y1,'r',label='Optimal Reimbursement for Insurer 1')
# # #     # Plot for 2's best-response. This is inverted to y2, x2 in order to show the "right" axes.
# # #     plt.plot(y2,x2,'b',label='Optimal Reimbursement for Insurer 2')
# # #     plt.xlabel('Reimbursement by Insurer 2') 
# # #     # Since these insurers are symmetric, we simply have a fixed point. 
# # #     plt.ylabel('Reimbursement by Insurer 1')
# # #     plt.title('Optimal Reimbursements - Linear Demand, Passive Beliefs, No Recapture')
# # #     plt.grid(True)
# # #     plt.legend(['BR of 1 to 2','BR of 2 to 1'],loc='upper right')
# # #     plt.show()
# # # if __name__=="__main__":
# # #     plotfunc()



# I think that the issue that I'm having as to why this won't compile stems from the fact that I'm using symbolic characters (Phi1, Phi2) and trying to work with them, instead of having them as "variables." I'm not sure how to include these otherwise, though. I'll comment everything above out, and manually enter everything using the "element" aspect, which is certainly tedious, but perhaps necessary. 
maxReimbursement1 = 50
maxReimbursement2 = 50
def NiNFunc1(element): #element is Phi2!
    Phi11 = sp.linspace(0,maxReimbursement1,num=1000)
    # This is the NiN bargaining objective function, only with every element plugged in separately to allow me to use element instead of any sort of symbolic. Notice that I use Phi11 instead of Phi1. 
    # profitinsurer1**beta = (marketshareLinear1 * (optimalPrice1 - Phi1))**beta. Substituting element for Phi2 and Phi11 for Phi1, we have: 
    # ((1 + (1/lambda1)(optimalPrice2 - optimalPrice1))/2) * (optimalPrice1 - Phi1)
    # optimalPrice2 = (2 * element + Phi11) / 3 + lambda1
    # optimalPrice1 = (2 * Phi11 + element) / 3 + lambda1
    # profitinsurer1 = ((1 + (1/lambda1)*((2 * element + Phi11) / 3 + lambda1 - (2 * Phi11 + element) / 3 + lambda1))/2) * ((2 * Phi11 + element) / 3 + lambda1 - Phi11)
    # We then move to hospital profit. 
    # profitHospital = (Phi1 - costH) * marketshareLinear1 + (Phi2 - costH) * marketshareLinear2
    # = (Phi11 - costH) * ((1 + (1/lambda1)((2 * element + Phi11) / 3 + lambda1 - (2 * Phi11 + element) / 3 + lambda1))/2) + (element - costH) * ((1 + (1/lambda1)((2 * Phi11 + element) / 3 + lambda1 - (2 * element + Phi11) / 3 + lambda1))/2)
    # And disagreement payoffs.
    # disagreementHospital1 = marketshareLinear2 * (Phi2 - costH)
    # = ((1 + (1/lambda1)((2 * Phi11 + element) / 3 + lambda1 - (2 * element + Phi11) / 3 + lambda1))/2) * (element - costH)
    insurer1Profit = ((1 + (1/lambda1)*((2 * element + Phi11) / 3 + lambda1 - (2 * Phi11 + element) / 3 + lambda1))/2) * ((2 * Phi11 + element) / 3 + lambda1 - Phi11)
    hospitalProfit = (Phi11 - costH) * ((1 + (1/lambda1) * ((2 * element + Phi11) / 3 + lambda1 - (2 * Phi11 + element) / 3 + lambda1))/2) + (element - costH) * ((1 + (1/lambda1) * ((2 * Phi11 + element) / 3 + lambda1 - (2 * element + Phi11) / 3 + lambda1))/2)
    hospitalDisagreement1 = ((1 + (1/lambda1) * ((2 * Phi11 + element) / 3 + lambda1 - (2 * element + Phi11) / 3 + lambda1))/2) * (element - costH)
    f1 = lambda Phi11: ( (insurer1Profit) ** (beta) ) * ( (hospitalProfit - hospitalDisagreement1) ** (1 - beta))
    # The above is the combined, substituted NiN bargaining function for insurer 1. 
    opt1 = max(Phi11, key = f1)
    if opt1 <= 0:
        return 0
    if opt1 >= maxReimbursement1:
        return maxReimbursement1
    else:
        return opt1
def plotfunc():
    x1 = list(sp.arange(0,maxReimbursement2+0.01,0.01))
    y1 = list(map(NiNFunc1,x1))
    plt.plot(x1,y1,'r',label='Optimal Reimbursement for Insurer 1')
    plt.xlabel('Reimbursement by Insurer 2')
    plt.ylabel('Reimbursement by Insurer 1')
    plt.title('Optimal Reimbursements - Insurer 1 in response to Insurer 2')
    plt.grid(True)
    plt.show()
if __name__=="__main__":
    plotfunc()
# "The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()" is my compiling error. I'm not sure how to account for multiple solutions with this format, since the previous setting I worked with this, there was a singular solution (or, at least, when I plotted best-responses, intersections corresponded to solutions.) This may be the wrong approach. I'm not entirely certain just yet. 