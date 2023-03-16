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
    "Anna": [25, 30, 10, 8.5, 42, 6],
    "Zeno": [37, 20, 12, 13, 35, 4]}

# Variabili
xAS = LpVariable("Anna-Spesa", 0, 1, LpBinary)
xAC = LpVariable("Anna-Cucinare", 0, 1, LpBinary)
xAP = LpVariable("Anna-Piatti", 0, 1, LpBinary)
xAB = LpVariable("Anna-Bucato", 0, 1, LpBinary)
xAF = LpVariable("Anna-Ferro", 0, 1, LpBinary)
xAR = LpVariable("Anna-Rifiuti", 0, 1, LpBinary)

xZS = LpVariable("Zeno-Spesa", 0, 1, LpBinary)
xZC = LpVariable("Zeno-Cucinare", 0, 1, LpBinary)
xZP = LpVariable("Zeno-Piatti", 0, 1, LpBinary)
xZB = LpVariable("Zeno-Bucato", 0, 1, LpBinary)
xZF = LpVariable("Zeno-Ferro", 0, 1, LpBinary)
xZR = LpVariable("Zeno-Rifiuti", 0, 1, LpBinary)

# Funzione obiettivo
model += 25*xAS + 30*xAC + 10*xAP + 8.5*xAB + 42*xAF + 6*xAR + 37*xZS + 20*xZC + 12*xZP + 13*xZB + 35*xZF + 4*xZR

# Vincoli
model += xAS + xAC + xAP + xAB + xAF + xAR == 3
model += xZS + xZC + xZP + xZB + xZF + xZR == 3
model += xAS + xZS == 1
model += xAC + xZC == 1
model += xAP + xZP == 1
model += xAB + xZB == 1
model += xAF + xZF == 1
model += xAR + xZR == 1

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", v.varValue)

# Valore della funzione obiettivo
print("Tempo totale minimo richiesto = {} minuti".format(round(value(model.objective),2)))
