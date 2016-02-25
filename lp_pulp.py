# Solving an LP with Python

import pulp

prob = pulp.LpProblem("Motorcycles and Delivery Carts", pulp.LpMaximize)

x1 = pulp.LpVariable("motorcycles", lowBound=0)
x2 = pulp.LpVariable("delivery carts")

# Add the objective
prob += 60*x1 + 80*x2, "Total Profit"
prob += x2  >= 0.0, "Non-negativity constraint"
prob += x1 <= 30, "Motorcycle Assembly facility"
prob += x2 <= 15, "Delivery Cart facility"
prob += x1 + 2*x2 <= 40, "Metal Stamping facility"

prob.writeLP("motorcycles_delivery_carts_model.lp")
prob.solve()

print "Status:", pulp.LpStatus[prob.status]

for v in prob.variables():
    print v.name, '=', v.varValue

print "Total Profit:", pulp.value(prob.objective)
