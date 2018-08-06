from sympy import *
init_printing(use_unicode=True)

def simult(t1=Symbol('t_1'),
           t2=Symbol('t_2'),
           l=Symbol('l'),
           q=Symbol('q'),
           m1=Symbol('m_1'),
           m2=Symbol('m_2'),
           b1=Symbol('b_1'),
           b2=Symbol('b_2')):
    
    #profits
    pi1 = .5*( (t2-t1)/3 +q)*(1 + (t2-t1)/(3*q) )
    pi2 = .5*( (t1-t2)/3 +q)*(1 + (t1-t2)/(3*q) )
    #nash bargaining objectives
    v1 = (pi1 - pi1.subs(t1,l) )**b1 * (m1*t1 +m2*t2)**(1-b1)
    v2 = (pi2 - pi2.subs(t2,l) )**b2 * (m1*t1 +m2*t2)**(1-b2)
    #simultaneous bargaining
    v1_foc = diff(v1,t1)
    v2_foc = diff(v2,t2)
    #solve for t2 as a function of t1
    t2_param = solve(v2_foc,t2)
    
    #focus on positive solution
    t2_param = t2_param[-1]

    #substitute back into foc
    v1_foc1 = v1_foc.subs(t2,t2_param)
    t1_param = solve(v1_foc1,t1)
    t1_param = t1_param[-1] 

    #sovle for t2
    t2_param = t2_param.subs(t1, t1_param)

    #solve for pi
    pi1_param = pi1.subs({t1:t1_param, t2:t2_param})
    pi2_param = pi2.subs({t1:t1_param, t2:t2_param})
    
    return (l,q,m1,m2,b1,b2,t1_param,t2_param,pi1_param,pi2_param)


def seq(t1=Symbol('t_1'),
           t2=Symbol('t_2'),
           l=Symbol('l'),
           q=Symbol('q'),
           m1=Symbol('m_1'),
           m2=Symbol('m_2'),
           b1=Symbol('b_1'),
           b2=Symbol('b_2')):
    #profits
    pi1 = .5*( (t2-t1)/3 +q)*(1 + (t2-t1)/(3*q) )
    pi2 = .5*( (t1-t2)/3 +q)*(1 + (t1-t2)/(3*q) )

    #use SPE/backward induction to solve game
    v2 = (pi2 - pi2.subs(t2,l) )**b2 * (m1*t1 +m2*t2)**(1-b2)
    v2_foc = diff(v2,t2)

    #solve for t1 as a function of t2
    h1 = solve(v2_foc,t2)
    h1 = h1[-1]
    h1 = simplify(h1)
    
    #susbitute h1 for t2, then substitute l into the second term for t1
    pi1_h = pi1.subs(t2,h1)
    pi1_l = pi1_h.subs(t1,l)
    v1 = (pi1.subs(t2,h1) - pi1_l )**(b1) * (m1*t1 + m2*h1)**(1-b1)
    v1_foc = diff(v1,t1)
    t1_param = solve(v1_foc,t1,rational=False)[-1]
    
    t2_param = h1.subs(t1,t1_param) 
    pi1_param = pi1.subs({t1:t1_param, t2:t2_param})
    pi2_param = pi2.subs({t1:t1_param, t2:t2_param})
    
    return (l,q,m1,m2,b1,b2,t1_param,t2_param,pi1_param,pi2_param)
    

def plotter(fname, game, ranger, scaler):
    out = open(fname,"w+")
    out.write('l,lambda,mu_1,mu_2,beta_1,beta_2,theta_1,theta_2,pi_1,pi_2\n')
    for l in ranger:
        l = l/scaler
        result = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%game(l = l,q = 1, m1 = .5, m2 = .5, b1 = .5,b2 = .5)
        out.write(result)
    out.close()

plotter('test.csv',simult,range(50,100,2),10.0)