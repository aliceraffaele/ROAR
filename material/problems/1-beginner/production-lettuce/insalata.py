#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:15:32 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("InsalataPomodori", LpMinimize)

# Variabili
x_INS = LpVariable("Num_ettari_lattuga", lowBound=0, cat=LpContinuous)
x_POM = LpVariable("Num_ettari_pomodori", lowBound=0, cat=LpContinuous)

# Vincoli
model += 1*x_INS + 2*x_POM <= 100
model += 2000*x_INS + 4500*x_POM >= 50000

# Funzione obiettivo
model += x_INS + x_POM

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", round(v.varValue,2))

# Valore della funzione obiettivo
print("Numero minimo di ettari richiesti = {}".format(round(value(model.objective),2)))
