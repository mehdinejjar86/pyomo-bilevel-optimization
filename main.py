import pao
from pao.pyomo import *
from pyomo.environ import *


model = ConcreteModel()

n_products = 2
n_periods = 4
n_resources = 6

model.J = RangeSet(1, n_products)
model.T = RangeSet(1, n_periods)  # Time periods
model.I = RangeSet(1, n_resources)

model.p_jt = Param(model.J, model.T, initialize=model_data['p_jt'])
model.c_jt = Param(model.J, model.T, initialize=model_data['c_jt'])
model.h_jt = Param(model.J, model.T, initialize=model_data['h_jt'])
model.s_jt = Param(model.J, model.T, initialize=model_data['s_jt'])
model.f_jt = Param(model.J, model.T, initialize=model_data['f_jt'])
model.r_t = Param(model.T, initialize=model_data['r_t'])
model.M = Param(initialize=1000000)
model.a_ijt = Param(model.I, model.J, model.T, initialize=model_data['a_ijt'])
model.b_it = Param(model.I, model.T, initialize=model_data['b_it'])

# Decision variables for the upper level (leader's problem)
model.x_jt = Var(model.J, model.T, within=NonNegativeReals, initialize=0)  # Manufactured product quantity
model.v_jt = Var(model.J, model.T, within=NonNegativeReals, initialize=0)  # Advertising expenditure
#model.y_t = Var(model.T, within=Binary, initialize=1)  # Inventory space renting decision
model.y_t = Param(model.T, initialize=model_data['y_t'])
#model.z_jt = Var(model.J, model.T, within=Binary, initialize=1)  # Setup cost incurring decision
model.z_jt = Param(model.J, model.T, initialize=model_data['z_jt'])

model.submodel = SubModel(fixed=[model.x_jt, model.v_jt])

# Define the variables for the lower level model
model.submodel.d_jt = Var(model.J, model.T, within=NonNegativeReals)  # Demand for product j in period t
model.submodel.I_jt = Var(model.J, model.T, within=NonNegativeReals)  # Inventory level for product j in period t
model.submodel.S_jt = Var(model.J, model.T, within=NonNegativeReals)  # Shortage for product j in period t

# Upper level objective function to maximize the profit
def upper_level_profit(model):
    revenue = sum(model.p_jt[j, t] * model.submodel.d_jt[j, t] for j in model.J for t in model.T)
    production_cost = sum(model.c_jt[j, t] * model.x_jt[j, t] for j in model.J for t in model.T)
    holding_cost = sum(model.h_jt[j, t] * model.submodel.I_jt[j, t] for j in model.J for t in model.T)
    shortage_cost = sum(model.s_jt[j, t] * model.submodel.S_jt[j, t] for j in model.J for t in model.T)
    advertising_cost = sum(model.v_jt[j, t] for j in model.J for t in model.T)
    renting_cost = sum(model.r_t[t] * model.y_t[t] for t in model.T)
    setup_cost = sum(model.f_jt[j, t] * model.z_jt[j, t] for j in model.J for t in model.T)

    return revenue - (production_cost + holding_cost + shortage_cost + advertising_cost) - renting_cost - setup_cost

# Set the objective in the model
model.UpperLevelObjective = Objective(rule=upper_level_profit, sense=maximize)

# Lower level objective function to maximize the profit
def lower_level_objective(submodel):
    # Minimize the cost of demand and inventory shortages
    demand_cost = sum(model.p_jt[j, t] * submodel.d_jt[j, t] for j in model.J for t in model.T)
    return demand_cost

# Set the objective in the submodel
model.submodel.LowerLevelObjective = Objective(rule=lower_level_objective, sense=minimize)

# Set the constraints
def resource_constraint(model, i, t):
    constraint = sum(model.a_ijt[i, j, t] * model.x_jt[j, t] for j in model.J) <= model.b_it[i, t]
    if type(constraint) == bool:
        if constraint == True:
            return Constraint.Feasible
        else:
            return Constraint.Infeasible
    else:
        return sum(model.a_ijt[i, j, t] * model.x_jt[j, t] for j in model.J) <= model.b_it[i, t]
model.ResourceConstraint = Constraint(model.I, model.T, rule=resource_constraint)

def setup_cost_constraint(model, j, t):
    return model.M * model.z_jt[j, t] - model.x_jt[j, t] >= 0
model.SetupCostConstraint = Constraint(model.J, model.T, rule=setup_cost_constraint)

def material_balance_constraint(submodel, j, t):
    if t == 1:
        return submodel.I_jt[j, t] == model.x_jt[j, t] - submodel.d_jt[j, t] + submodel.S_jt[j, t]
    else:
        return submodel.I_jt[j, t] == submodel.I_jt[j, t-1] + model.x_jt[j, t] - submodel.d_jt[j, t] + submodel.S_jt[j, t]
model.submodel.MaterialBalanceConstraint = Constraint(model.J, model.T, rule=material_balance_constraint)

def shortage_product_constraint(submodel, j, t):
    return submodel.S_jt[j, t] >= 0
model.submodel.ShortageProductConstraint = Constraint(model.J, model.T, rule=shortage_product_constraint)

def inventory_product_constraint(submodel, j, t):
    return submodel.I_jt[j, t] >= 0
model.submodel.InventoryProductConstraint = Constraint(model.J, model.T, rule=inventory_product_constraint)

model.submodel.Dt_c1 = Constraint(expr=(model.submodel.d_jt[1,1] + model.submodel.d_jt[1,2] + model.submodel.d_jt[1,3] + model.submodel.d_jt[1,4]) >= 100)
model.submodel.Dt_c2 = Constraint(expr=(model.submodel.d_jt[2,1] + model.submodel.d_jt[2,2] + model.submodel.d_jt[2,3] + model.submodel.d_jt[2,4]) >= 100)
model.submodel.Dt_c3 = Constraint(expr=(2*model.submodel.d_jt[1,1] - 3*model.submodel.d_jt[1,2]) <= 0)
model.submodel.Dt_c4 = Constraint(expr=(model.submodel.d_jt[1,2] - 2*model.submodel.d_jt[1,3]) <= 0)
model.submodel.Dt_c5 = Constraint(expr=(3*model.submodel.d_jt[1,3] - 4*model.submodel.d_jt[1,4]) <= 0)
model.submodel.Dt_c6 = Constraint(expr=(model.submodel.d_jt[2,1] - 2*model.submodel.d_jt[2,2]) <= 0)
model.submodel.Dt_c7 = Constraint(expr=(model.submodel.d_jt[2,2] - 4*model.submodel.d_jt[2,3]) <= 0)
model.submodel.Dt_c8 = Constraint(expr=(3*model.submodel.d_jt[2,3] - 5*model.submodel.d_jt[2,4]) <= 0)
model.submodel.Dt_c9 = Constraint(expr=(100*model.submodel.d_jt[1,1] - 5*model.v_jt[1,1]) >= 0)
model.submodel.Dt_c10 = Constraint(expr=(100*model.submodel.d_jt[1,2] - 3*model.v_jt[1,1] - 3.5*model.v_jt[1,2]) >= 0)
model.submodel.Dt_c11 = Constraint(expr=(100*model.submodel.d_jt[1,3] - 1.5*model.v_jt[1,1] - 2*model.v_jt[1,2] - 3.25*model.v_jt[1,3]) >= 0)
model.submodel.Dt_c12 = Constraint(expr=(100*model.submodel.d_jt[1,4] - 0.5*model.v_jt[1,1] - model.v_jt[1,2] - 1.75*model.v_jt[1,3] - 3.7*model.v_jt[1,4]) >= 0)
model.submodel.Dt_c13 = Constraint(expr=(100*model.submodel.d_jt[2,1] - 8*model.v_jt[2,1]) >= 0)
model.submodel.Dt_c14 = Constraint(expr=(100*model.submodel.d_jt[2,2] - 2*model.v_jt[2,1] - 4*model.v_jt[2,2]) >= 0)
model.submodel.Dt_c15 = Constraint(expr=(100*model.submodel.d_jt[2,3] - 1.5*model.v_jt[2,1] - 2*model.v_jt[2,2] - 3.1*model.v_jt[2,3]) >= 0)
model.submodel.Dt_c16 = Constraint(expr=(100*model.submodel.d_jt[2,4] - 0.5*model.v_jt[2,1] - model.v_jt[2,2] - 1.9*model.v_jt[2,3] - 3.9*model.v_jt[2,4]) >= 0)

# Try solving the model
solver = pao.Solver("pao.pyomo.FA")
solution = solver.solve(model, tee=True)
