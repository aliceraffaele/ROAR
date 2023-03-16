#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("Assunzioni", LpMinimize)

# Set e parametri
C = [1,2,3]
L = [1,2,3]
num_min_candidati_lavori = {1: 2, 2: 1, 3: 1}
stipendi = {1: 1450, 2: 1600, 3: 1300}
bonus = {
    1: {1: 150, 2: 230, 3: 110},
    2: {1: 100, 2: 90, 3: 150},
    3: {1: 350, 2: 410, 3: 210}}
Assegnazioni = [(i,j) for i in C for j in L]

# Variabili
vars_y = LpVariable.dicts("y", C, 0, 1, LpBinary)
vars_x = LpVariable.dicts("x", (C, L), 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(vars_y[i] * stipendi[i] for i in C) + lpSum(vars_x[i][j]*bonus[i][j] for i in C for j in L)

# Vincoli
for i in C:
    for j in L:
        model += vars_x[i][j] <= vars_y[i]
for j in L:
    model += lpSum(vars_x[i][j] for i in C) >= num_min_candidati_lavori[j]

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata (se esiste)
if LpStatus[model.status] == "Optimal":
    print("Soluzione ottima")
    for v in model.variables():
        print(v.name, " = ", v.varValue)
    # Valore della funzione obiettivo
    print("Costo minimo per la compagnia finanziaria = {}".format(round(value(model.objective),2)))
elif LpStatus[model.status] == "Infeasible":
    print("Istanza impossibile")
