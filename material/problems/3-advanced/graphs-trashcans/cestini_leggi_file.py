#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:03:57 2022

@author: Alice Raffaele
"""
from pulp import *

def leggi_input(nome_file):
    V = []
    E = []
    costo_cestino = 0
    costo_pattumiera = 0
    budget = 0
    V_speciali = []
    num_minimo_cestini_speciali = 0

    with open(nome_file, 'r') as file:
       while True:
           riga = file.readline()
           if not riga:
               break
           if "PUNTI" in riga:
               riga_pezzi = riga.split()
               V = riga_pezzi[2:] # dal terzo elemento in poi (scartiamo "PUNTI" e "=")
           if "NUM_LATI" in riga:
               riga_pezzi = riga.split()
               num_lati = int(riga_pezzi[2])
               for i in range(num_lati):
                   riga_pezzi = file.readline().split()
                   lato = (riga_pezzi[0], riga_pezzi[1])
                   E += [lato]
           if "COSTO_CESTINO" in riga:
               riga_pezzi = riga.split()
               costo_cestino = int(riga_pezzi[2])
           if "COSTO_PATTUMIERA" in riga:
               riga_pezzi = riga.split()
               costo_pattumiera = int(riga_pezzi[2])
           if "BUDGET" in riga:
               riga_pezzi = riga.split()
               budget = int(riga_pezzi[2])
           if "SPECIALI" in riga:
               riga_pezzi = riga.split()
               V_speciali = riga_pezzi[2:]
           if "NUMERO_MINIMO_CESTINI_SPEC" in riga:
               riga_pezzi = riga.split()
               num_minimo_cestini_speciali = int(riga_pezzi[2])
    file.close()
    return V, E, costo_cestino, costo_pattumiera, budget, V_speciali, num_minimo_cestini_speciali

V, E, costo_cestino, costo_pattumiera, budget, V_speciali, num_minimo_cestini_speciali = leggi_input('cestini_file.txt')

# Definizione del modello
modello = LpProblem('CestiniPattumiere', LpMaximize)

# Variabili
xC = LpVariable.dicts('xC', V, lowBound=0, upBound=1, cat=LpBinary)
xP = LpVariable.dicts('xP', V, lowBound=0, upBound=1, cat=LpBinary)

# Vincoli

# Al più un cestino/pattumiera in ogni strada
for (i,j) in E:
    modello += xC[i] + xP[i] + xC[j] + xP[j] <= 1

# Almeno num_minimo_cestini_speciali tra i punti speciali
modello += lpSum(xC[i] for i in V_speciali) >= num_minimo_cestini_speciali

# Budget
modello += lpSum(xC[i]*costo_cestino + xP[i]*costo_pattumiera for i in V) <= budget

# Funzione obiettivo
modello += lpSum(xC[i] + xP[i] for i in V)

# Ottimizzazione
status = modello.solve(PULP_CBC_CMD(msg=0))

if status == 1:
    print("Numero massimo di cestini/pattumiere posizionabili:", round(value(modello.objective)))
    print("\nIn particolare:")
    spese = 0
    for i in V:
        if xC[i].varValue > 0:
            print(i + ' – cestino all-in-one')
            spese += costo_cestino
        if xP[i].varValue > 0:
            print(i + ' – pattumiera')
            spese += costo_pattumiera
    print("\nBudget speso: " + str(spese) + " €")
