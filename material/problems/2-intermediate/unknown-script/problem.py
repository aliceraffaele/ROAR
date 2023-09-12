from pulp import *

model = LpProblem("Problem?", LpMaximize)

indexes = [1,2,3]
parameters ={1:150, 2: 320, 3:60}
values_1 = {1: 9500, 2: 123}
values_2 = {
    1: {1: 30, 2: 120, 3: 12},
    2: {1: 0.7, 2: 1, 3: 0.5}}
values_3 = {1: 0, 2: -1, 3:5}

var_x = LpVariable.dicts("x", indexes, 0, None, LpInteger)

model += lpSum(var_x[i] * parameters[i] for i in indexes)

for j in values_2.keys():
    model += lpSum(var_x[i]*values_2[j][i] for i in indexes) <= values_1[j]

model += lpSum(values_3[k]*var_x[k] for k in indexes) >= 0

status = model.solve(PULP_CBC_CMD(msg = 0))
if status == 1 :
    print("Optimal solution:")
    for v in model.variables():
            print(v.name, " = ", v.varValue)

    print("The objective function value is {}\n\n".format(round(value(model.objective),2)))
else:
    print("Instance not feasible.")