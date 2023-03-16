#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:33:59 2022

@author: Alice Raffaele
"""
from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("ParitàGenere", LpMinimize)

# Set e parametri
N = ["Anna", "Zeno"]
M = ["Spesa", "Cucinare", "Piatti", "Bucato", "Ferro", "Rifiuti"]

tempi = {
    "Anna":
        {"Spesa": 25, "Cucinare": 30, "Piatti": 10, "Bucato": 8.5, "Ferro": 42, "Rifiuti": 6},
    "Zeno":
        {"Spesa": 37, "Cucinare": 20, "Piatti": 12, "Bucato": 13, "Ferro": 35, "Rifiuti": 4}
    }
Assegnamenti = [(i,j) for i in N for j in M]

# Variabili
vars = LpVariable.dicts("x", (N, M), 0, 1, LpBinary)

# Funzione obiettivo
model += lpSum(vars[i][j] * tempi[i][j] for (i,j) in Assegnamenti)

# Vincoli
for i in N:
    model += lpSum(vars[i][j] for j in M) == int(len(M)/len(N))

for j in M:
    model += lpSum(vars[i][j] for i in N) == 1

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", v.varValue)

# Valore della funzione obiettivo
print("Tempo totale minimo richiesto = {} minuti".format(round(value(model.objective),2)))
