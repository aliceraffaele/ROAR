#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:39:03 2022

@author: Alice Raffaele
"""

from pulp import *

# Inizializzazione del problema assegnando un nome e la direzione dell'ottimizzazione
modello = LpProblem("Grafopoli", LpMinimize)

# Set e parametri
V = ["A","B","C","D","E","F","H","S"]
A = {
     ("A","B"): 9, ("A","F"): 6, ("B","S"): 10, ("C","D"): 5, ("C","E"): 5, ("C","S"): 7, ("D","A"): 5,
     ("D","B"): 7, ("D","S"): 3, ("E","B"): 12, ("E","C"): 5, ("E","F"): 1, ("F","A"): 6, ("F","C"): 8,
     ("F","D"): 2, ("F","E"): 1, ("F","S"): 15, ("H","A"): 9, ("H","C"): 11, ("H","E"): 5, ("H","F"): 6}

sorgente = "H"
destinazione = "S"

# Variabili
x = LpVariable.dicts("x", A.keys(), 0, 1, LpBinary)

# Funzione obiettivo
modello += lpSum(x[i,j]*A[i,j] for i,j in A.keys())

# Vincoli
modello += lpSum(x[i,j] for i,j in A.keys() if i == sorgente) == 1
modello += lpSum(x[i,j] for i,j in A.keys() if j == destinazione) == 1

for v in V:
    if v not in [sorgente, destinazione]:
        modello += lpSum(x[i,j] for i,j in A.keys() if j == v) == lpSum(x[i,j] for i,j in A.keys() if i == v)

# Chiamata al solver
status = modello.solve()

# Stampa soluzione ottima se trovata
if status == 1:
    print("Soluzione ottima:")
    for v in modello.variables():
        print("{} = {}".format(v.name, v.varValue))

    # Valore della funzione obiettivo
    print("\nCammino minimo = {}".format(round(value(modello.objective),2)))

elif status == -1:
    print("Istanza non ammissibile")
