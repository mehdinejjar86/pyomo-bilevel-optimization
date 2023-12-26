# Pyomo: Bilevel Optimization

The basic components of this scenario define a dynamic inventory model. In reformulating the model to take into account advertising, we get a sequential game. Consider the situation where a manufacturer of $\ n \$ products wishes to determine a production mix, $\ x \in \mathbb{R}^{n \times T} \$, that maximizes his profits over a finite horizon $\ T \$ in the face of $\ q \$ resource constraints. Assume that the demand at time $\ t \, \ d_t \in \mathbb{R}^n \$, is inexact; i.e., known only to lie in the set $\( D_t \)$ whose boundaries are subject to the influences of advertising. For example, $\( D_t \)$ might specify upper and lower bounds on the demand for each product in period $\( t \)$. We now suppose the existence of a sole customer whose demand (requirements) for the \( n \) products is a function of the manufacturer's expenditure on advertising, $\( v \in \mathbb{R}^{n \times T} \)$, where 'advertising' is intended to include all activities such as marketing, the use of extended warranties, and temporary on-site trouble shooting that might sway the customer's purchase decisions. (The particular application we have in mind centers on the manufacture of specialized assemblies for an auto maker by a supplier new to the market. It is not unusual for a startup...

