import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
import pandas as pd


##########################################################################
#################### logit simult ########################################
##########################################################################

maxiter = 50
#solve nash bargaining with one insurer

def calc_shares1(p1, cost, wtp):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    u1 = (wtp - p1)/cost
    s1 = 2*np.exp(u1)/(2*np.exp(u1) + 1 )
    return s1
  

def calc_profits_price_shares1(phi1,cost,wtp,mc1):
    pi1 = lambda p : -1*calc_shares1(p, cost, wtp)[0]*(p-phi1 -mc1)
    p1 = minimize(pi1,1,method='Nelder-Mead',options={'maxiter':maxiter,'disp': False}).x
    s1 = calc_shares1(p1,  cost, wtp)
    return p1[0], s1[0], s1[0]*(p1[0]-phi1 -mc1)

def nash_in_nash_obj1(phi1, cost, wtp, mc1, beta=.5):
    p1,s1,profits1 = calc_profits_price_shares1(phi1, cost, wtp, mc1)
    hosp_profit = s1*phi1
    obj = -1*(np.log(max(hosp_profit,1e-6))*(1-beta) + np.log(max(profits1,1e-6))*beta)

    return obj

def nash_in_nash1(cost,wtp,mc1,outside_option=False):
    obj1 = lambda phi : nash_in_nash_obj1(phi,cost,wtp,mc1)
    result = minimize(obj1,13,method='Nelder-Mead',options={'maxiter':maxiter,'disp': False})
    
    if outside_option:
        return result.x[0]*calc_shares1(result.x[0], cost, wtp)
    return result.x[0]

#solve nash bargaining with 2 insurers

def calc_shares(p1, p2,  cost, wtp):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    u1 = (wtp[0] - p1)/cost
    u2 = (wtp[1] - p2)/cost
    if  ~np.isinf(np.exp(u1)) & ~np.isinf(np.exp(u2)):
        s1 = np.exp(u1)/ (np.exp(u1)+ np.exp(u2) + 1 )
        s2 = np.exp(u2)/ (np.exp(u1)+ np.exp(u2) + 1 )
        return s1,s2
    else:
        return 1.*(u1 > u2), 1.*(u2 > u1)
    

def calc_profits_price_shares(phi1,phi2,cost,wtp,mc):
    mc1,mc2 = mc
    
    p1,p2 = 1,2
    diff =  np.maximum(p1,p1)
    p10,p20 = 0,0
    maxiter = 10
    while maxiter >=0 and diff > 10e-7:
        #seems as though there is a contraction mapping here, need to think more about why
        
        pi1 = lambda p : -1*calc_shares(p, p20,  cost, wtp)[0]*(p-phi1 -mc1)
        pi2 = lambda p :  -1*calc_shares(p10, p,  cost, wtp)[1]*(p-phi2 -mc2)

        
        p1 = minimize(pi1,p10,method='Nelder-Mead',options={'maxiter':maxiter,'disp': False}).x
        p2 = minimize(pi2,p20,method='Nelder-Mead',options={'maxiter':maxiter,'disp': False}).x
        
        #update loop variables
        diff = np.abs(np.maximum(p1 - p10,p2-p20))[0]
        p10,p20 = p1,p2
        maxiter = maxiter-1
        
    s1,s2 = calc_shares(p1, p2,  cost, wtp)
    return p1, p2, s1,s2, s1*(p1-phi1 -mc1), s2*(p2-phi2 -mc2)

def solve_eq(phi1,phi2,cost,wtp,mc):
    p1, p2, s1,s2, _, _ = calc_profits_price_shares(phi1,phi2,cost,wtp,mc)
    return phi1[0],phi2[0],p1[0],p2[0],s1[0],s2[0]


##########################################################################
#################### logit sim ###########################################
##########################################################################

def nash_in_nash_sim(phi1, phi2, cost, wtp, mc, beta=.5, outside_option=None):
    p1,p2,s1,s2,profits1,profits2 = calc_profits_price_shares(phi1,phi2,cost,wtp,mc)
    hosp_profit = s1*phi1 + s2*phi2
    
    #the passive beliefs case
    if outside_option is None:
        outside_option = s2*phi2
        
    obj = -1*(np.log(max(hosp_profit-outside_option,1e-6))*(1-beta) 
              + np.log(profits1)*beta)
    return obj


def bargain_helper_sim(phi1, phi2, cost, wtp, mc, beta=.5,outside_option=None):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_sim, phi1, args=(phi2,cost, wtp, mc,  beta, outside_option),
                      method='Nelder-Mead', options={'maxiter':maxiter,'disp': False})
    return result.x


def simult_bargain(phi1, phi2, cost, wtp, mc, betas=[.5,.5],active=False):
    """solve the bargaining problems seperately and iterate for a solution"""       
    
    #loop variables, check on this...
    diff =  np.maximum(phi1,phi2)
    phi10,phi20 = 0,0
    maxiter = 10
    
    outside_option1 = None
    outside_option2 = None
    if active:
        outside_option1 = nash_in_nash1(cost,wtp[0],mc[0],outside_option=True)
        outside_option2 = nash_in_nash1(cost,wtp[1],mc[1],outside_option=True)
        
    while maxiter >=0 and diff > 10e-7:
        #seems as though there is a contraction mapping here, need to think more about why
        phi1 = bargain_helper_sim(phi1, phi2, cost, wtp, mc, beta=betas[0] ,outside_option=outside_option1)
        phi2 = bargain_helper_sim(phi2, phi1, cost, wtp[::-1], mc[::-1], beta=betas[1],outside_option=outside_option2)
        
        #update loop variables
        diff = np.abs(np.maximum(phi1 - phi10,phi2-phi20))[0]
        phi10,phi20 = phi1,phi2
        maxiter = maxiter-1
        
    return phi1, phi2


##########################################################################
#################### logit seq ###########################################
##########################################################################

#arbitrary outside option...
def nash_in_nash_seq(phi1, phi2, cost, wtp, mc, beta=.5, outside_option=None):
    p1,p2,s1,s2,profits1,profits2 = calc_profits_price_shares(phi1,phi2,cost,wtp,mc)
    hosp_profit = s1*phi1 + s2*phi2
    
    #the passive beliefs case
    if outside_option is None:
        outside_option = s2*phi2
        
    obj = -1*(np.log(max(hosp_profit-outside_option,1e-6))*(1-beta) 
              + np.log(max(profits1,1e-6))*beta)
    return obj


def bargain_helper_seq(phi1, phi2, cost, wtp, mc, beta=.5,outside_option=None):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_seq, phi1, args=(phi2,cost, wtp, mc,  beta, outside_option),
                      method='Nelder-Mead', options={'maxiter':maxiter,'disp': False})
    return result.x


def seq_bargain(phi1, cost, wtp, mc, betas=[.5,.5]):
    """solve the bargaining problems seperately and iterate for a solution"""
    outside = nash_in_nash1(cost,wtp[1],mc[1],outside_option=True)
    
    phi2 = phi1 + 2
    
    diff =  np.maximum(phi1,phi2)
    phi10,phi20 = phi1+.5,phi2+.5
    maxiter = 20
    
    while maxiter >=0 and diff > 10e-7:
        
        p10,p20,_,_,_,_ = calc_profits_price_shares(phi10,phi20,cost,wtp,mc)
        s10 = calc_shares1(p10[0],cost,wtp[0])

        phi2 = bargain_helper_seq(phi20, phi10, cost, wtp[::-1], mc[::-1], beta=betas[1],outside_option=phi10*s10)
        phi1 = bargain_helper_seq(phi10, phi20, cost, wtp, mc, beta=betas[0] ,outside_option=outside)

        diff = np.abs(np.maximum(phi1 - phi10,phi2-phi20))[0]
        phi10,phi20 = phi1,phi2
        maxiter = maxiter-1
        
    return phi1, phi2
