# Pyomo: Bilevel Optimization

The basic components of this scenario define a dynamic inventory model. In reformulating the model to take into account advertising, we get a sequential game. Consider the situation where a manufacturer of $\( n \)$ products wishes to determine a production mix, $\ x \in \mathbb{R}^{n \times T} \$, that maximizes his profits over a finite horizon $\( T \)$ in the face of $\( q \)$ resource constraints. Assume that the demand at time $\ t \, \ d_t \in \mathbb{R}^n \$, is inexact; i.e., known only to lie in the set $\( D_t \)$ whose boundaries are subject to the influences of advertising. For example, $\( D_t \)$ might specify upper and lower bounds on the demand for each product in period $\( t \)$. We now suppose the existence of a sole customer whose demand (requirements) for the $\( n \)$ products is a function of the manufacturer's expenditure on advertising, $\( v \in \mathbb{R}^{n \times T} \)$, where 'advertising' is intended to include all activities such as marketing, the use of extended warranties, and temporary on-site trouble shooting that might sway the customer's purchase decisions. (The particular application we have in mind centers on the manufacture of specialized assemblies for an auto maker by a supplier new to the market. It is not unusual for a startup firm producing specialized parts to have a single customer in its first few years of operation.)

In the model, the manufacturer is assigned the role of Ieader and begins by selecting a production mix and advertising strategy for each point in time. It is assumed that the customer is rational and will react to these choices by meeting his demand at minimum cost. The customer can therefore be viewed as a follower in the game whose purchase decisions come after the manufacturer announces his full set of plans for the current period. The nature of the market rules out cooperation. An additional assumption isthat all demand must be met. As a consequence, the customer effectively controls inventory and shortages. This can be seen from the material balance equation (11.1f) below which indicates that once the production and advertising decisions are taken, demand must be satisfied from a combination of inventory and subcontracting. This raises a number of modeling issues, depending upon whether subcontracting is permitted in a period when adequate production capacity and inventory exist. Only allowing subcontracting at tim es when shortages occur has some practical justification because some uncertainty usually surrounds future demand. Nevertheless, building inventory is compatible with the situation where the manufacturer can anticipate the customer's decision. In the developments, we make use of the following notation.

## Parameters

- `a_{ijt}`: amount of resource i required to make a unit of product j in period t
- `b_{it}`: amount of resource i available in period t
- `p_{jt}`: selling price of product j in period t
- `c_{jt}`: unit cost of manufacturing product j in period t
- `h_{jt}`: unit holding cost of product j in period t
- `s_{jt}`: unit cost of subcontracting product j in period t
- `r_{t}`: cost of renting warehouse space in period t
- `f_{jt}`: setup cost for product j in period t
- `B_{j}`: relative measure of space occupied by product j normalized to product 1
- `I̅_{t}`: maximum amount of free inventory space available in period t
- `M`: large constant


