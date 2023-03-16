from pulp import *

model = LpProblem("Problem?", LpMaximize)

indici = [1,2,3]
Parametri={1:150, 2: 320, 3:60}
Valori_1 = {1: 9500, 2: 123}
valori_2 = {
    1: {1: 30, 2: 120, 3: 12},
    2: {1: 0.7, 2: 1, 3: 0.5}}
valori_3 = {1: 0, 2: -1, 3:5}

var_x = LpVariable.dicts("x", indici, 0, None, LpInteger)

model += lpSum(var_x[i] * Parametri[i] for i in indici)

for j in valori_2.keys():
    model += lpSum(var_x[i]*valori_2[j][i] for i in indici) <= Valori_1[j]

model += lpSum(valori_3[k]*var_x[k] for k in indici) >= 0

status = model.solve(PULP_CBC_CMD(msg = 0))
if status == 1 :
    print("Soluzione ottima:")
    for v in model.variables():
            print(v.name, " = ", v.varValue)

    print("Il valore della funzione obiettivo è {}\n\n".format(round(value(model.objective),2)))
else:
    print("Problema non ammissibile")
