#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 10:05:28 2022

@author: Alessandro Gobbi
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("TrasportoCaffè", LpMinimize)

# Set e parametri
indici_impianti = [1,2,3,4]
indici_bar = [1,2,3]
capacita_prod = {1: 75, 2: 90, 3: 80, 4: 75}
domanda = {1: 60, 2: 75, 3: 80}
costi = {
    1: {1: 0.4, 2: 0.3, 3: 0.2},
    2: {1: 0.2, 2: 0.3, 3: 0.5},
    3: {1: 0.1, 2: 0.6, 3: 0.2},
    4: {1: 0.5, 2: 0.1, 3: 0.3},
}
num_max_impianti_attivati = 3
costo_attivazione_impianti = 1350

# Variabili
x = LpVariable.dicts("x", (indici_impianti, indici_bar), 0, None, LpContinuous)
y = LpVariable.dicts("y", indici_impianti, 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(x[i][j]*costi[i][j] for i in indici_impianti for j in indici_bar) + lpSum(y[i]*costo_attivazione_impianti for i in indici_impianti)

# Vincoli
for i in indici_impianti:
    model += lpSum(x[i][j] for j in indici_bar) <= capacita_prod[i] * y[i]

for j in indici_bar:
    model += lpSum(x[i][j] for i in indici_impianti) >= domanda[j]

model += lpSum(y[i] for i in indici_impianti) <= num_max_impianti_attivati

# Chiamata al solver
model.solve()

# Per sapere se l'istanza del problema è stata risolta all'ottimo (status == 1)
# oppure se è infeasible (status == -1)
if model.status == 1:
    print("Soluzione ottima trovata\n")

    # Stampa soluzione ottima trovata
    for v in model.variables():
        print(v.name, " = ", v.varValue)

    # Valore della funzione obiettivo
    print("Costo minimo per il trasporto = {}".format(round(value(model.objective),2)))

    # Per sapere quanto caffè è prodotto da ogni impianto
    for i in indici_impianti:
        produzione = 0;
        for j in indici_bar:
            produzione += x[i][j].varValue
        print("L'impianto " + str(i) + " produce " + str(produzione) + " Kg di caffè.")

    # Per sapere il numero di impianti aperti
    numero = 0;
    for i in indici_impianti:
        numero += y[i].varValue
    print("Numero impianti aperti: " + str(numero));
else:
    if model.status == -1:
        print("Infeasible")
