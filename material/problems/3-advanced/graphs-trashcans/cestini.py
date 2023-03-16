#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 18:03:57 2022

@author: Alice Raffaele
"""
from pulp import *


V = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'A', 'B', 'C', 'SP']
E = [('P1', 'P2'),
    ('P1', 'P5'),
    ('P1', 'C'),
    ('P2', 'P3'),
    ('P2', 'P8'),
    ('P2', 'SP'),
    ('P3', 'P6'),
    ('P3', 'P7'),
    ('P3', 'P9'),
    ('P3', 'C'),
    ('P4', 'B'),
    ('P4', 'C'),
    ('P6', 'A'),
    ('P7', 'P9'),
    ('P7', 'A'),
    ('P9', 'P10'),
    ('P9', 'B'),
    ('P9', 'C'),
    ('P10', 'P11')]

costo_cestino = 190
costo_pattumiera = 20
budget = 1000

# Definizione del modello
modello = LpProblem('CestiniPattumiere', LpMaximize)

# Variabili
xC = LpVariable.dicts('xC', V, lowBound=0, upBound=1, cat=LpBinary)
xP = LpVariable.dicts('xP', V, lowBound=0, upBound=1, cat=LpBinary)

# Vincoli

# Al più un cestino/pattumiera in ogni strada
for (i,j) in E:
    modello += xC[i] + xP[i] + xC[j] + xP[j] <= 1

# Almeno tre cestini in A, B, C, SP
modello += xC['A'] + xC['B'] + xC['C'] + xC['SP'] >= 3

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
