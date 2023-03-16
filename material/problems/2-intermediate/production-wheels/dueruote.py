#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("2Ruote", LpMaximize)

# Set e parametri
P = ["Biciclette", "Ciclomotori", "Tricicli"]
profitti = {"Biciclette": 100, "Ciclomotori": 300, "Tricicli": 50}
costi = {"Biciclette": 300, "Ciclomotori": 1200, "Tricicli": 50}
storage = {"Biciclette": 0.5, "Ciclomotori": 1, "Tricicli": 0.5}
capitale = 93000
storage_max = 101

# Variabili
vars = LpVariable.dicts("x", P, 0, None, LpContinuous)

# Funzione obiettivo
model += lpSum(vars[i] * profitti[i] for i in P)

# Vincoli
model += lpSum(vars[i]*costi[i] for i in P) <= capitale
model += lpSum(vars[i]*storage[i] for i in P) <= storage_max

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", v.varValue)

# Valore della funzione obiettivo
print("Profitto massimo = {}".format(round(value(model.objective),2)))
