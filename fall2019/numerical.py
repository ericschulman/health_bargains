def calc_price(theta1, theta2, mu1, mu2, cost, listprice):
    """compute each insurer's price (assumes interior solution)"""
    p1 = (2.*theta1*mu1+theta2*mu2)/3. + cost
    p2 = (2.*theta2*mu2+theta1*mu1)/3. + cost
    #return np.clip(p1,0,listprice), np.clip(p2,0,listprice)
    return np.max(p1,0), np.max(p2,0)
  
    
def calc_t(theta1, theta2, mu1, mu2, cost, listprice):
    """compute the proportion of people choosing each insurer
    assumes interior solution"""
    p1, p2 = calc_price(theta1, theta2, mu1, mu2, cost, listprice)
    t_hat = .5 + (p2 - p1)/(2.*cost)
    return t_hat


def calc_eq(theta1, theta2, mu1, mu2, cost, listprice):
    """compute eq profit for each firm and market shares
    Go through each KKT to ensure that we see if the market 
    is covered or not... """

    #interior solution
    p1, p2 = calc_price(theta1, theta2, mu1, mu2, cost, listprice)
    t1 = calc_t(theta1, theta2, mu1, mu2, cost, listprice)
    #check to see if interior makes sense?
        
    #print('eq:',t1,(listprice - p1)/cost, 'price:', p1 ,p2)
    if t1 > (listprice - p1)/cost or t1 < 0: 
        t1 = -1
    
    #solve the local monopoly case
    p0 = (listprice + mu1*theta1)/2
    t0 = (listprice - mu1*theta1)/(2*cost)
    #does monopoly make sense?
    t0_firm2 = (listprice - mu2*theta2)/(2*cost)  
            
    #print('local monop',t0,p0)
    if t0_firm2 + t0 > 1:
        t0 = -1
    
    #find the max profits
    profits =  [t0*(p0-theta1*mu1),t1*(p1-theta1*mu1), 0]
    ind = np.argmax(profits)
    return [t0,t1,0], profits, [p0,p1,0], ind


def calc_profits(theta1,theta2,mu1,mu2,cost, listprice):
    t1, profits1, prices1, index1 = calc_eq(theta1, theta2, mu1, mu2, cost, listprice)
    t2, profits2, prices2, index2 = calc_eq(theta2, theta1, mu2, mu1, cost, listprice)
    hosp_profit = t1[index1]*theta1*mu1 +  t2[index2]*theta2*mu2
    print(listprice,cost, theta1, theta2, mu1, t1[index1], t2[index2], prices1[index1], prices2[index2] ,profits1[index1], profits2[index2], hosp_profit, (index1==0 or index2==0 or index2 ==2 or index1==2),(index1==1 or index2==1 or index2 ==2 or index1==2))
    return hosp_profit, profits1[index1], profits2[index2]

    
def outside_simlt(cost,listprice):
    """outside option in simult case
    assuming listprice high enough"""
    if cost/listprice  > 3/8:
        return 3*listprice**2/(32*cost)
    else:
        return (listprice -cost)/2
    

#arbitrary outside option...
def nash_in_nash(theta1, theta2, mu1, mu2, cost, listprice, outside):
    hosp_profit, profits1, profits2 = calc_profits(theta1, theta2, mu1, mu2, cost, listprice)
    obj = -1*(max(hosp_profit-outside,0)*profits1)**.5
    print(outside,-1*obj)
    return obj


COST = 3
LIST = 7
print(nash_in_nash(COST,COST, .5, .5, COST,LIST, outside_simlt(COST,LIST)))
print('----')
print(nash_in_nash(4.5,4.5,.5, .5, COST,LIST, outside_simlt(COST,LIST)))
print('----')
print(nash_in_nash(LIST-1,LIST-1, .5, .5, COST, LIST, outside_simlt(COST,LIST)))