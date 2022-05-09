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

`pi  (p- phi ) * s`

The hospital has a linear marginal cost, `c` associated with a specific negotiation `t`. Therefore, its payoff is given below. We also experiment with an insurer marginal cost.

`pi_h = phi1*s1 + phi2*s2`

# Linear Demand Model

We solve different versions of the model with linear demand in `linear_demand` folder. We make the following simplifying assumptions to this model. These assumptions are intended to ensure closed form solutions for reimbursements, premiums and other outcomes in the insurance market.

We will assume insurers are symmetric in the Nash bargaining game i.e., the Nash bargaining parameter `beta1=beta2=.5`.

Linear demand specification i.e. 

* This specification is also known as the Hotelling model of demand.
* Consumers have type `t` has a uniform distribution over [0,1].
* Consumer demand depends on 2 parameters: a willingness to pay, `v`. In the cost this is labeled as `wtp` and a Hotelling taste parameter `lambda`. The model parameter `lambda` can be thought of as a travel cost. In the code, cost is labeled as `cost`
* Thus, consumer `i` has the following preferences over insurance. 

- `v - p1 - lambda*t` for insurer 1
- `v - p2 - lambda*(1-t)` for insurer 2
- `0` otherwise

* Consumers pick the option that provides the highest possible utility i.e. the options are insurer 1, insurer 2 or no insurance.
* We assume that consumer's willingness to pay for insurance `v` is high enough so that all consumers purchase insurance. Thus, there is complete coverage of the insurance market.

# Logit Demand Model

We solve different versions of the model with logit demand in `logit_demand` folder.  Consumers have utility given below. In this case, `v` is consumer surplus parameter. `alpha` is the demand elasticity parameter. 

Consumers still have differentiated tastes. However, `t` no longer has a uniform distribution. Now, `t` now has a type I extreme value distribution. As a result, the difference between `t` has a logistic distribution and market shares are given by the logit equation.

`exp( (v- p1 - t)/lambda )/ ( 1 + exp( (v- p1 - t)/lambda ) + exp( (v- p2 - t)/lambda ))`

The price elasticity `alpha = 1/lambda`, is lowered holding other parameters fixed. Increasing the price elasticity `alpha` has the inverse effect of increasing the consumers travel cost `lambda`. If consumers are more price elastic (meaning a higher `alpha`) then their personal preferences for firms are less important.

