# Pyomo: Bilevel Optimization

The basic components of this scenario define a dynamic inventory model. In reformulating the model to take into account advertising, we get a sequential game. Consider the situation where a manufacturer of $\( n \)$ products wishes to determine a production mix, $\ x \in \mathbb{R}^{n \times T} \$, that maximizes his profits over a finite horizon $\( T \)$ in the face of $\( q \)$ resource constraints. Assume that the demand at time $\ t \, \ d_t \in \mathbb{R}^n \$, is inexact; i.e., known only to lie in the set $\( D_t \)$ whose boundaries are subject to the influences of advertising. For example, $\( D_t \)$ might specify upper and lower bounds on the demand for each product in period $\( t \)$. We now suppose the existence of a sole customer whose demand (requirements) for the $\( n \)$ products is a function of the manufacturer's expenditure on advertising, $\( v \in \mathbb{R}^{n \times T} \)$, where 'advertising' is intended to include all activities such as marketing, the use of extended warranties, and temporary on-site trouble shooting that might sway the customer's purchase decisions. (The particular application we have in mind centers on the manufacture of specialized assemblies for an auto maker by a supplier new to the market. It is not unusual for a startup firm producing specialized parts to have a single customer in its first few years of operation.)

In the model, the manufacturer is assigned the role of Ieader and begins by selecting a production mix and advertising strategy for each point in time. It is assumed that the customer is rational and will react to these choices by meeting his demand at minimum cost. The customer can therefore be viewed as a follower in the game whose purchase decisions come after the manufacturer announces his full set of plans for the current period. The nature of the market rules out cooperation. An additional assumption isthat all demand must be met. As a consequence, the customer effectively controls inventory and shortages. This can be seen from the material balance equation (11.1f) below which indicates that once the production and advertising decisions are taken, demand must be satisfied from a combination of inventory and subcontracting. This raises a number of modeling issues, depending upon whether subcontracting is permitted in a period when adequate production capacity and inventory exist. Only allowing subcontracting at tim es when shortages occur has some practical justification because some uncertainty usually surrounds future demand. Nevertheless, building inventory is compatible with the situation where the manufacturer can anticipate the customer's decision. In the developments, we make use of the following notation.

## Parameters

$$
\begin{align*}
a_{ijt} & : \text{amount of resource } i \text{ required to make a unit of product } j \text{ in period } t \\
b_{it} & : \text{amount of resource } i \text{ available in period } t \\
p_{jt} & : \text{selling price of product } j \text{ in period } t \\
c_{jt} & : \text{unit cost of manufacturing product } j \text{ in period } t \\
h_{jt} & : \text{unit holding cost of product } j \text{ in period } t \\
s_{jt} & : \text{unit cost of subcontracting product } j \text{ in period } t \\
r_{t} & : \text{cost of renting warehouse space in period } t \\
f_{jt} & : \text{setup cost for product } j \text{ in period } t \\
B_{j} & : \text{relative measure of space occupied by product } j \text{ normalized to product 1} \\
\bar{I}_{t} & : \text{maximum amount of free inventory space available in period } t \\
M & : \text{large constant}
\end{align*}
$$


$$
\begin{align*}
\max_{x,u,v} \quad & F = \sum_{j=1}^{n}\sum_{t=1}^{T} p_{jt}d_{jt} - \sum_{j=1}^{n}\sum_{t=1}^{T}\left[c_{jt}x_{jt} + h_{jt}l_{jt} + s_{jt}S_{jt} + v_{jt}\right] \\
& \qquad - \sum_{t=1}^{t} r_{t}y_{t} - \sum_{j=1}^{n}\sum_{t=1}^{T} f_{jt}z_{jt} \\
\text{subject to} \quad & \sum_{j=1}^{n} a_{ijt}x_{jt} \leq b_{it}, \quad \forall i, t \\
& Mz_{jt} - x_{jt} \geq 0, \quad \forall j,t \\
& x_{jt} \geq 0, \quad v_{j} = (v_{j1}, \ldots, v_{jT}) \in V_{j}, \quad z_{jt} \in \{0, 1\}, \quad \forall j,t \\
& \min_{d,I,S,y} \quad \sum_{j=1}^{n}\sum_{t=1}^{T} p_{jt}d_{jt} \\
& \text{subject to} \quad I_{jt} - I_{j,t-1} + d_{jt} - S_{jt} = x_{jt}, \quad \forall j,t \\
& Mt_{y} + I_{t} - \sum_{j=1}^{n} B_{t}l_{jt} \geq 0, \quad \forall t \\
& S_{jt} \geq 0, \quad I_{jt} \geq 0, \quad I_{j0} = 0, \quad \forall j,t \\
& d_{t} = (d_{1t}, \ldots, d_{nt}) \in D_{t}(v), \quad \forall t
\end{align*}
$$

