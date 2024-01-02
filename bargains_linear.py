import numpy as np
from scipy.optimize import minimize
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
import pandas as pd

##########################################################################
#################### linear simult #######################################
##########################################################################

def calc_price(phi1, phi2, cost, wtp,mc):
    """compute each insurer's price (assumes interior solution)"""
    mc1,mc2 = mc
    p1 = (2*(phi1+mc1)+phi2+mc2)/3. + cost
    p2 = (2*(phi2+mc2)+phi1+mc1)/3. + cost
    return p1, p2
  
    
def calc_s(phi1, phi2, cost, wtp,mc):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    p1, p2 = calc_price(phi1, phi2, cost, wtp,mc)
    t_hat = .5 + (p2 - p1)/(2.*cost)
    return np.clip(t_hat,0,1)


def calc_profits(phi1,phi2,cost, wtp, mc):
    mc1,mc2 = mc
    s= calc_s(phi1, phi2, cost, wtp,mc)
    p1,p2 = calc_price(phi1, phi2, cost, wtp,mc)

    profits1, profits2 = s*(p1-phi1-mc1), (1-s)*(p2-phi2-mc2)
    hosp_profit = s*(phi1) +  (1-s)*(phi2)
    #print(s,'profit')

    if phi1 <= 0 or phi2 <= 0:
        return 1e-8,1e-8,1e-8

    return hosp_profit, profits1, profits2


def outside_simlt(phi1, phi2, cost, wtp,  mc, active=False, recapture = False):
    """outside option in simult case
    assuming listprice high enough"""
    mc1,mc2 = mc

    if active:
        return (wtp-cost)/2  #outside cost is other insurer?

    s_hat = calc_s(phi1, phi2, cost, wtp,mc) # s_hat with no recapture
    p1,p2 = calc_price(phi1, phi2, cost, wtp,mc)

    if recapture:
        s_hat  = np.clip((cost + p2 - wtp)/cost,0,1) #s_hat with recapture
    #print(s_hat,'outside')
    return (1-s_hat)*(phi2)

##########################################################################
#################### linear active #######################################
##########################################################################


#arbitrary outside option...
def nash_in_nash_act(phi1, phi2, cost, wtp, mc, beta=.5,active=True):
    hosp_profit, profits1, profits2 = calc_profits(phi1, phi2,  cost,  wtp, mc)
    #print(phi2,outside_simlt(phi1, phi2,cost, wtp , mc, active=active))
    obj = -1*(np.log(max(hosp_profit-outside_simlt(phi1, phi2,cost, wtp , mc, active=active),1e-8))*(1-beta) 
              + np.log(max(profits1,1e-8))*beta)
    return obj


def bargain_helper_act(phi1, phi2, cost, wtp, mc, beta=.5,active=True):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_act, phi1, args=(phi2,cost, wtp, mc, beta, active),
                      method='Nelder-Mead', options={'disp': False})
    return result.x



def simult_bargain_act(phi1, phi2, cost, wtp, mc, betas=[.5,.5],active=True):
    """solve the bargaining problems seperately and iterate for a solution"""       
    
    #loop variables, check on this...
    diff =  np.maximum(phi1,phi2)
    phi10,phi20 = 0,0
    maxiter = 20
    while maxiter >=0 and diff > 10e-8:
        #seems as though there is a contraction mapping here, need to think more about why
        phi1 = bargain_helper_act(phi1, phi2, cost, wtp, mc, beta=betas[0] ,active=active)
        phi2 = bargain_helper_act(phi2, phi1, cost, wtp, mc[::-1], beta=betas[1],active=active)
        
        #update loop variables
        diff = np.abs(np.maximum(phi1 - phi10,phi2-phi20))[0]
        phi10,phi20 = phi1,phi2
        maxiter = maxiter-1
        
    return phi1, phi2



##########################################################################
#################### linear passive #######################################
##########################################################################



def nash_in_nash_pass(phi1, phi2, cost, wtp, mc, beta=.5,outside=None):
    if outside == None:
        outside = outside_simlt(phi1, phi2,cost, wtp , mc,active=False)

    hosp_profit, profits1, profits2 = calc_profits(phi1, phi2,  cost,  wtp, mc)
    obj = -1*(np.log(max(hosp_profit-outside,1e-8))*(1-beta) 
              + np.log(max(profits1,1e-8))*beta)
    return obj


def bargain_helper_pass(phi1, phi2, cost, wtp, mc, beta=.5,outside=None):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_pass, phi1, args=(phi2,cost, wtp, mc, beta, outside),
                      method='Nelder-Mead', options={'disp': False})
    return result.x


def simult_bargain_pass(phi1, phi2, cost, wtp, mc, betas=[.5,.5]):
    """solve the bargaining problems seperately and iterate for a solution"""       
    
    #loop variables, check on this...
    diff =  np.maximum(phi1,phi2)
    phi10,phi20 = 0,0
    maxiter = 20
    while maxiter >=0 and diff > 10e-8:
        #seems as though there is a contraction mapping here, need to think more about why
        
        outside1 = outside_simlt(phi10, phi20, cost, wtp,  mc, active=False)
        outside2 = outside_simlt(phi20, phi10, cost, wtp, mc[::-1], active=False)
        phi1 = bargain_helper_pass(phi1, phi2, cost, wtp, mc, beta=betas[0],outside=outside1)
        phi2 = bargain_helper_pass(phi2, phi1, cost, wtp, mc[::-1], beta=betas[1],outside=outside2)
        
        #update loop variables
        diff = np.abs(np.maximum(phi1 - phi10,phi2-phi20))[0]
        phi10,phi20 = phi1,phi2
        maxiter = maxiter-1
        
    return phi1, phi2


##########################################################################
#################### linear  #############################################
##########################################################################


def simult_bargain(phi1, phi2, cost, wtp, mc, betas=[.5,.5],active=True):
    if active:
        return simult_bargain_act(phi1, phi2, cost, wtp, mc, betas=betas,active=True)
    else:
        return simult_bargain_pass(phi1, phi2, cost, wtp, mc, betas=betas)




##########################################################################
################### linear seq ###########################################
##########################################################################

#arbitrary outside option...
def nash_in_nash_seq(phi1, phi2, cost, wtp, mc, beta=.5,outside=None):
    if outside == None:
        outside = outside_simlt(phi1, phi2,cost, wtp , mc, active=True)

    hosp_profit, profits1, profits2 = calc_profits(phi1, phi2,  cost,  wtp, mc)
    obj = -1*(np.log(max(hosp_profit-outside,1e-8))*(1-beta) 
              + np.log(max(profits1,1e-8))*beta)
    return obj


def bargain_helper_seq(phi1, phi2, cost, wtp, mc, beta=.5,outside=0):
    """solve each firm 1s optimization holding phi 2 fixed"""
    result = minimize(nash_in_nash_seq, phi1, args=(phi2,cost, wtp, mc, beta,outside),
                      method='Nelder-Mead', options={'disp': False})
    return result.x



def seq_bargain(phi1, cost, wtp, mc, betas=[.5,.5]):
    """solve the bargaining problems seperately and iterate for a solution"""       
    
    #loop variables, check on this...
    phi2 = phi1 +10
    
    diff =  np.maximum(phi1,phi2)
    phi10,phi20 = phi1+.5,phi2+.5
    maxiter = 30
    while maxiter >=0 and diff > 10e-8:
        outside = outside_simlt(phi10, phi20, cost, wtp,  mc, active=True)

        #seems as though there is a contraction mapping here, need to think more about why
        phi1 = bargain_helper_seq(phi10, phi20, cost, wtp, mc, beta=betas[0] ,outside=outside)
        phi2 = bargain_helper_seq(phi20, phi10, cost, wtp, mc[::-1], beta=betas[1],outside=phi10)

        
        #update loop variables
        diff = np.abs(np.maximum(phi1 - phi10,phi2-phi20))[0]
        phi10,phi20 = phi1,phi2
        maxiter = maxiter-1
        
    return phi1, phi2

###################################################################3
################### misc helpers ##################################
####################################################################

def solve_eq(phi1,phi2,cost,wtp,mc):
    phi1,phi2 = phi1[0],phi2[0]
    p1,p2 = calc_price(phi1,phi2,cost,wtp,mc)
    s1 = calc_s( phi1,phi2 ,cost,wtp,mc)
    s1 = s1
    s2 = 1-s1
    return phi1,phi2,p1,p2,s1,s2
