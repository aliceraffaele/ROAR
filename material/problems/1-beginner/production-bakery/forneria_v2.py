#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:17:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("InForneria-v2", LpMaximize)

# Variabili
xF = LpVariable("Kg_Focaccia", lowBound=0, cat=LpContinuous)
xP = LpVariable("Kg_Pizza", lowBound=0, cat=LpContinuous)

# Vincoli
model += 25*xP + 20*xF <= 180
model += 15*xP + 35*xF <= 240
model += xF >= 1.5

# Funzione obiettivo
model += 6*xF + 8*xP

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", round(v.varValue,2))

# Valore della funzione obiettivo
print("Ricavo max giornaliero per pizza e focaccia = {}".format(round(value(model.objective),2)))
