import numpy as np
import pulp
stocks = ['WMT', 'XOM']
returns = [
    [
        0.99374805, 1.00833595, 0.99703634, 1.02158949, 1.01408882,
        0.96949562, 1.01588785, 1.01901257, 1.02452603, 0.99280364,
        1.02455621,  1.00736356,  1.0209259 ,  1.02835884,  0.99658703,
        1.00958904,  1.00257802,  1.0014887 ,  0.98702703,  0.99288061,
        0.96800883,  1.01994302,  0.98086592,  0.98177417,  1.013343  ,
        1.00973236,  1.03217576,  1.00576765,  0.9989077 ,  1.00970476,
        0.98240152,  0.96375913,  0.9908493 ,  0.99379509,  0.99462756,
        1.02437956,  1.01980904,  0.98057574,  0.97905088,  1.02780204,
        1.01189633,  1.00475857,  1.01309375,  1.01154957,  1.01617507,
        1.00735688,  1.01513743,  0.99254415,  0.9766737 ,  0.99163406,
        1.01347122,  1.00281955
    ],
    [
        1.00731284,  1.01328904,  1.0103218 ,  0.98149038,  0.9904482,
        0.99715628,  1.00954743,  1.00257922,  0.99485483,  1.00443295,
        0.99914184,  1.00920245,  0.98772036,  0.99987691,  0.98264188,
        1.00626409,  1.02303287,  1.00815383,  1.01798648,  0.99750978,
        0.98846885,  1.01082381,  0.99048186,  0.98786787,  1.00972763,
        1.01348748,  1.01996198,  1.01898882,  0.99599863,  0.97004132,
        0.99337357,  0.96902918,  0.99557468,  0.99592542,  1.00099182,
        1.01325242,  1.00293363,  0.98013406,  0.99328525,  1.00738608,
        1.00683485,  1.00481363,  1.02100479,  1.03946102,  1.02731481,
        0.99729608,  0.98395843,  1.02319173,  0.99640934,  1.03536036,
        1.02871438,  0.99693381
    ]
]

means = list(np.mean(returns, axis=1))
# Don't bound allocations
allocations = [0.0, 2.0]

m = 1.001

x = pulp.LpVariable.dicts("allocations", stocks, 0)

y = pulp.LpVariable.dicts("y", ['return_%d'%i for i in range(len(returns[0]))], 0)

prob = pulp.LpProblem('MAD LP', pulp.LpMinimize)

prob += (1.0/len(stocks)) * pulp.lpSum(y), "MAD of an allocation"
prob += pulp.lpSum(x) == 1.0, "Allocate everything"

#prob += pulp.lpDot(means, x) >= m, "Expected rate of return constraint"
#prob += pulp.lpSum([pulp.lpDot(e1,e2) for e1,e2 in zip(means,x)]), "Expected rate of return constraint"

for i, x_i in enumerate(x):
    prob += x_i <= allocations[i], "Make sure we don't allocate more than a_i to x_i"

#for i, y_t in enumerate(y):
#    prob += pulp.lpSum([(returns[i][j]-means[i])*x[stocks[i]] for j in range(len(returns[i]))]) <= y_t, "Constraint on y_t 1"
#    prob += pulp.lpSum([(means[i]-returns[i][j])*x[stocks[i]] for j in range(len(returns[i]))]) <= y_t, "Constraint on y_t 2"
prob.writeLP('test.lp')
pulp.pulpTestAll()
prob.solve()

print "Status:", pulp.LpStatus[prob.status]
for v in prob.variables():
    print v.name, '=', v.varValue

print "Minimum MAD =", pulp.value(prob.objective)

