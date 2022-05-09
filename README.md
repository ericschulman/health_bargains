# Insurance Market Bargaining
Numerical examples involving bargaining in insurance markets with 2 insurers, 1 hospital. In the files below, we solve different numerical examples of the model.

# Description of the bargaining game

* **Players** -1 hospital and 2 insurers. We will call the hospital hospital $h$ and the insurers $i_1$ and $i_2$.

* **Actions** The hospital has 1 decision. It bargains over a reimbursement rate for each insurer. The reimbursement paid by insurer $i$ is $\phi_i$.
 % The decision about bargaining is labeled as $e_{h,i_1} \in \{0,1\}$ and $e_{h,i_2} \in \{0,1\}$. 

 Insurers have 2 decisions. They bargain with the hospital about reimbursements $\phi_i$ and they choose prices $p_i$ in the insurance market. 

* **Information sets** - The set of negotiating parties, called $\mathcal{G}$, is revealed. Given this information, the hospital begins a cooperative bargaining game with the insurers in $\mathcal{G}$. This will determine reimbursement rates. 

Insurers have 2 information sets. The set of negotiations is revealed at the first information set. At the second  decision point, the information set is  the vector of reimbursements $\phi_i$ which is used to choose prices.



* **Strategies** - The hospital's strategy $\sigma_h$ determines the reimbursements $\phi$.

Insurers' strategies $\sigma_i$ decide the reimbursements $\phi_i$ when the negotiating parties are revealed. Finally,  the insurers' strategies determine prices $p_i$ after reimbursements are set


* **Payoffs** - The payoffs depend on the vector of reimbursements and premiums.

The market share of each insurer in the insurance market $s_i$ is determined by premiums in the insurance market and consumer's demand for insurance. %This demand can be linear or logit. %The probability of a member becoming sick $\mu_i$ is exogenous. Like in \cite{ho-lee:2019}, there is a linear marginal cost $c_i$

The insurers' regard their reimbursements as their linear marginal costs. Thus, hospital profits are given by the following expression below. 

$$\pi_i(\mathcal{G},\phi,p) =  (p_i - \phi_i ) s_i  $$

The hospital has a linear marginal cost, $c_{it}$ associated with a specific negotiation $t$. Therefore, its payoff is given below. We also experiment with an insurer marginal cost.

$$\pi_h(\mathcal{G},\phi,p) = \sum_{i=1,2} (\phi_i - c_{it})s_i$$

# Linear Demand Model

We solve different versions of the model with linear demand in `linear_demand` folder. We make the following simplifying assumptions to this model. These assumptions are intended to ensure closed form solutions for reimbursements, premiums and other outcomes in the insurance market.

\begin{itemize}
\item We will assume insurers are symmetric in the Nash bargaining game i.e., the Nash bargaining parameter $\beta_1 = \beta_2$ and further $\beta_i = 1/2$ and $c_i = 0$. We relax this assumption at future points in the paper. % $\mu_1 = \mu_2$ and 

Linear demand specification i.e. 

* This specification is also known as the Hotelling model of demand.
* Consumers have type $t_i$. $t_i$ has a uniform distribution over $[0,1]$.
* Consumer demand depends on 2 parameters: a willingness to pay, $v$. In the cost this is labeled as `wtp` and a Hotelling taste parameter $\lambda$. The model parameter $\lambda$ can be thought of as a travel cost. In the code, cost is labeled as `cost`
* Thus, consumer $i$ has the following preferences over insurance. 

$$ u_i =  \begin{cases} 
v - p_1 -   \lambda t_i  & i_1=1,i_2=0 \\
v -  p_2 - \lambda(1-t_i) & i_1=0,i_2=1 \\
0 & o.w.
 \end{cases}$$

* Consumer $i$ picks the option that provides the highest possible utility i.e. the options are insurer 1 $i_1$, insurer 2 $i_2$ or no insurance.
* We assume that consumer's willingness to pay for insurance $v$ is high enough so that all consumers purchase insurance. Thus, there is complete coverage of the insurance market.

# Logit Demand Model

We solve different versions of the model with logit demand in `logit_demand` folder.  Consumers have utility given below. In this case, $v$ is consumer surplus parameter. $\alpha$ is the demand elasticity parameter. 

$$ u_i =  \begin{cases} 
v -  p_1 +   \lambda t_{i1}  & i_1=1,i_2=0 \\
v -  p_2 + \lambda t_{i2}  & i_1=0,i_2=1 \\\
t_{i0} & o.w.
 \end{cases}$$

Consumers still have differentiated tastes. However, $t_{i}$ no longer has a uniform distribution. Now, $t_{i}$ now has a type I extreme value distribution. As a result, the difference between $t_{i1}$ and $t_{i2}$ has a logistic distribution and market shares are given by the logit equation.

$$s_i = \dfrac{exp( (v  -  p_i)/\lambda )}{1+ \sum_{j=1}^2 exp( (v -  p_j)/\lambda  ) }$$

The price elasticity $\alpha = 1/\lambda$, is lowered holding other parameters fixed. Increasing the price elasticity $\alpha$ has the inverse effect of increasing the consumers travel cost $\lambda$. If consumers are more price elastic (meaning a higher $\alpha$) then their personal preferences for firms are less important.

