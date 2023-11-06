import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
import pandas as pd


##########################################################################
#################### logit simult ########################################
##########################################################################

#solve nash bargaining with one insurer

def calc_shares1(p1, cost, wtp):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    u1 = (wtp - p1)/cost
    s1 = np.exp(u1)/(np.exp(u1) + 1 )
    return s1
  

def calc_profits_price_shares1(phi1,cost,wtp,mc1):
    pi1 = lambda p : -1*calc_shares1(p, cost, wtp)[0]*(p-phi1 -mc1)
    p1 = minimize(pi1,1,method='Nelder-Mead',tol=1e-6).x
    s1 = calc_shares1(p1,  cost, wtp)
    return p1[0], s1[0], s1[0]*(p1[0]-phi1 -mc1)

def nash_in_nash_obj1(phi1, cost, wtp, mc1, beta=.5):
    p1,s1,profits1 = calc_profits_price_shares1(phi1, cost, wtp, mc1)
    hosp_profit = s1*phi1
    obj = -1*(np.log(hosp_profit)*(1-beta) + np.log(profits1)*beta)

    return obj

def nash_in_nash1(cost,wtp,mc1,outside_option=False):
    obj1 = lambda phi : nash_in_nash_obj1(phi,cost,wtp,mc1)
    result = minimize(obj1,13,method='Nelder-Mead',tol=1e-6)
    
    if outside_option:
        return result.x[0]*calc_shares1(result.x[0], cost, wtp)
    return result.x[0]

#solve nash bargaining with 2 insurers

def calc_shares(p1, p2,  cost, wtp):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    u1 = (wtp[0] - p1)/cost
    u2 = (wtp[1] - p2)/cost
    s1 = np.exp(u1)/(np.exp(u1)+ np.exp(u2) + 1 )
    s2 = np.exp(u2)/(np.exp(u1)+ np.exp(u2) + 1 )
    
    return s1,s2
  

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

        
        p1 = minimize(pi1,p10).x
        p2 = minimize(pi2,p20).x
        
        #update loop variables
        diff = np.abs(np.maximum(p1 - p10,p2-p20))[0]
        p10,p20 = p1,p2
        maxiter = maxiter-1
        
    s1,s2 = calc_shares(p1, p2,  cost, wtp)
    return p1, p2, s1,s2, s1*(p1-phi1 -mc1), s2*(p2-phi2 -mc2)


def nash_in_nash_sim(phi1, phi2, cost, wtp, mc, beta=.5, outside_option=None):
    p1,p2,s1,s2,profits1,profits2 = calc_profits_price_shares(phi1,phi2,cost,wtp,mc)
    hosp_profit = s1*phi1 + s2*phi2
    
    #the passive beliefs case
    if outside_option is None:
        outside_option = s2*phi2
        
    obj = -1*(np.log(max(hosp_profit-outside_option,1e-6))*(1-beta) 
              + np.log(profits1)*beta)
    return obj


def bargain_helper(phi1, phi2, cost, wtp, mc, beta=.5,outside_option=None):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_sim, phi1, args=(phi2,cost, wtp, mc,  beta, outside_option),
                      method='Nelder-Mead', options={'disp': False})
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
        phi1 = bargain_helper(phi1, phi2, cost, wtp, mc, beta=betas[0] ,outside_option=outside_option1)
        phi2 = bargain_helper(phi2, phi1, cost, wtp[::-1], mc[::-1], beta=betas[1],outside_option=outside_option2)
        
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
        
    obj = -1*(np.log(max(hosp_profit-outside_option,1e-6))*(1-beta) 
              + np.log(profits1)*beta)
    return obj



def bargain_helper_seq(phi1, cost, wtp, mc,beta=.5):
    """ solve firm 1s optimization holding theta 2 fixed """
    #figure out mkt shares if p1 is locked in...
    p1,s1,profit1 = calc_profits_price_shares1(phi1,cost,wtp[0],mc[0])

    result = minimize( nash_in_nash_seq, 15., args=(phi1, cost, wtp[::-1], mc[::-1], beta, s1*phi1),
                      method='Nelder-Mead', options={'disp': False} )
    return result.x




def seq_obj(phi1, cost, wtp, mc, betas=np.array([.5,.5]),outside_option=None):
    """ theta1 is a guess for the first stage """
    phi2 = bargain_helper_seq(phi1, cost, wtp, mc,betas[1])
    return nash_in_nash_seq( phi1, phi2, cost, wtp, mc, betas[0], outside_option=outside_option )


def seq_bargain(phi1, cost, wtp, mc, betas=[.5,.5]):
    """solve the bargaining problems seperately,
    then solve for the solution"""   
    #only compute no deal 1x for initial
    outside1 = nash_in_nash1(cost,wtp[1],mc[1],outside_option=True)
    result = minimize(seq_obj, phi1, args=(cost, wtp, mc, betas,outside1),
                      method='Nelder-Mead', options={'disp': False})
    
    phi1 = result.x
    phi2 = bargain_helper_seq(phi1, cost, wtp, mc ,beta=betas[1])
    return phi1, phi2