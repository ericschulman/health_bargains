# Insurance Market Bargaining
Numerical examples involving bargaining in insurance markets with 2 insurers, 1 hospital. In the files below, we solve different numerical examples of the model.

# Description of the bargaining game

* **Players** -1 hospital and 2 insurers. We will call the hospital hospital `h` and the insurers `i_1` and `i_2`.

* **Actions** The hospital has 1 decision. It bargains over a reimbursement rate for each insurer. The reimbursement paid by insurer `i` is `phi`.


 Insurers have 2 decisions. They bargain with the hospital about reimbursements `phi` and they choose prices `p` in the insurance market. 

* **Information sets** - The set of negotiating parties, called `G`, is revealed. Given this information, the hospital begins a cooperative bargaining game with the insurers in `G`. This will determine reimbursement rates. 

Insurers have 2 information sets. The set of negotiations is revealed at the first information set. At the second  decision point, the information set is  the vector of reimbursements `phi` which is used to choose prices.



* **Strategies** - The hospital's strategy `sigma_h` determines the reimbursements `phi`.

Insurers' strategies `sigma` decide the reimbursements `phi` when the negotiating parties are revealed. Finally,  the insurers' strategies determine prices `p` after reimbursements are set.


* **Payoffs** - The payoffs depend on the vector of reimbursements and premiums.

The market share of each insurer in the insurance market `s` is determined by premiums in the insurance market and consumer's demand for insurance. 

The insurers' regard their reimbursements as their linear marginal costs. Thus, hospital profits are given by the following expression below. 

![equation](https://latex.codecogs.com/svg.image?pi_i(mathcal{G},phi,p))

The hospital has a linear marginal cost, `c_{it}` associated with a specific negotiation `t`. Therefore, its payoff is given below. We also experiment with an insurer marginal cost.

![equation](https://latex.codecogs.com/svg.image?pi_h(mathcal{G},phi,p)&space;=&space;sum_{i=1,2}&space;(phi_i&space;-&space;c_{it})s_i)

# Linear Demand Model

We solve different versions of the model with linear demand in `linear_demand` folder. We make the following simplifying assumptions to this model. These assumptions are intended to ensure closed form solutions for reimbursements, premiums and other outcomes in the insurance market.

We will assume insurers are symmetric in the Nash bargaining game i.e., the Nash bargaining parameter `beta1=beta2=.5`.

Linear demand specification i.e. 

* This specification is also known as the Hotelling model of demand.
* Consumers have type `t` has a uniform distribution over [0,1].
* Consumer demand depends on 2 parameters: a willingness to pay, `v`. In the cost this is labeled as `wtp` and a Hotelling taste parameter `lambda`. The model parameter `lambda` can be thought of as a travel cost. In the code, cost is labeled as `cost`
* Thus, consumer `i` has the following preferences over insurance. 

![equation](https://latex.codecogs.com/svg.image?&space;begin{matrix}&space;v&space;-&space;p_1&space;-&space;&space;&space;lambda&space;t_i&space;&space;&&space;i_1=1,i_2=0&space;v&space;-&space;&space;p_2&space;-&space;lambda(1-t_i)&space;&&space;i_1=0,i_2=1&space;0&space;&&space;o.w.&space;end{matrix})

* Consumers pick the option that provides the highest possible utility i.e. the options are insurer 1, insurer 2 or no insurance.
* We assume that consumer's willingness to pay for insurance `v` is high enough so that all consumers purchase insurance. Thus, there is complete coverage of the insurance market.

# Logit Demand Model

We solve different versions of the model with logit demand in `logit_demand` folder.  Consumers have utility given below. In this case, `v` is consumer surplus parameter. `alpha` is the demand elasticity parameter. 

Consumers still have differentiated tastes. However, `t` no longer has a uniform distribution. Now, `t` now has a type I extreme value distribution. As a result, the difference between `t` has a logistic distribution and market shares are given by the logit equation.

![equation](https://latex.codecogs.com/svg.image?s_i&space;=&space;dfrac{exp(&space;(v&space;&space;-&space;&space;p_i)/lambda&space;)}{1&plus;&space;sum_{j=1}^2&space;exp(&space;(v&space;-&space;&space;p_j)/lambda&space;&space;)&space;})

The price elasticity `alpha = 1/lambda`, is lowered holding other parameters fixed. Increasing the price elasticity `alpha` has the inverse effect of increasing the consumers travel cost `lambda`. If consumers are more price elastic (meaning a higher `alpha`) then their personal preferences for firms are less important.

