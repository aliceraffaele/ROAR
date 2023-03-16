#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
model = LpProblem("DietaMediterranea", LpMinimize)

# Set e parametri
C = ["Pane", "Pasta", "Latte", "Uova", "Pollo", "Tonno", "Cioccolato", "Verdure"]
N = ["Kcal", "Carboidrati", "Proteine", "Grassi", "Calcio"]
quantita_minime = {"Kcal": 1700, "Carboidrati": 200, "Proteine": 70, "Grassi": 60, "Calcio": 700}
valori = {
    "Pane": {"Kcal": 150, "Carboidrati": 30, "Proteine": 5, "Grassi": 2, "Calcio": 52},
    "Pasta": {"Kcal": 390, "Carboidrati": 75, "Proteine": 11, "Grassi": 3, "Calcio": 5},
    "Latte": {"Kcal": 70, "Carboidrati": 5, "Proteine": 5, "Grassi": 3, "Calcio": 150},
    "Uova": {"Kcal": 70, "Carboidrati": 0, "Proteine": 6, "Grassi": 6, "Calcio": 50},
    "Pollo": {"Kcal": 150, "Carboidrati": 2, "Proteine": 36, "Grassi": 5, "Calcio": 22},
    "Tonno": {"Kcal": 150, "Carboidrati": 0, "Proteine": 25, "Grassi": 15, "Calcio": 4},
    "Cioccolato": {"Kcal": 112, "Carboidrati": 7, "Proteine": 2, "Grassi": 10, "Calcio": 11},
    "Verdure": {"Kcal": 45, "Carboidrati": 8, "Proteine": 3, "Grassi": 2, "Calcio": 50},
    }

porzioni_minime = {"Pane": 0, "Pasta": 0, "Latte": 0, "Uova": 0, "Pollo": 0, "Tonno": 0,
                   "Cioccolato": 0, "Verdure": 2}
porzioni_massime = {"Pane": 2, "Pasta": 2, "Latte": 2, "Uova": 1, "Pollo": 1, "Tonno": 2,
                   "Cioccolato": 2, "Verdure": 6}
costo_porzione = {"Pane": 0.5, "Pasta": 3.5, "Latte": 1, "Uova": 1.5, "Pollo": 4.5, "Tonno": 2,
                   "Cioccolato": 1.5, "Verdure": 4}
max_porzioni_pane_pasta = 3
min_porzioni_latte_pollo_tonno = 4

# Variabili
vars = LpVariable.dicts("x", C, 0, None, LpInteger)

# Funzione obiettivo
model += lpSum(vars[c] * costo_porzione[c] for c in C)

# Vincoli
for n in N:
    model += lpSum(vars[c]*valori[c][n] for c in C) >= quantita_minime[n]

for c in C:
    model += vars[c] >= porzioni_minime[c]
    model += vars[c] <= porzioni_massime[c]

model += vars["Pane"] + vars["Pasta"] <= max_porzioni_pane_pasta
model += vars["Latte"] + vars["Pollo"] + vars["Tonno"] >= min_porzioni_latte_pollo_tonno

# Chiamata al solver
model.solve()

# Stampa soluzione ottima trovata
for v in model.variables():
    print(v.name, " = ", round(v.varValue,2))

# Valore della funzione obiettivo
print("Costo minimo dieta = {}".format(round(value(model.objective),2)))
