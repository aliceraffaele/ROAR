#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:45:37 2022

@author: Alice Raffaele
"""

from pulp import *

PARTECIPANTI = ['Alessandra', 'Bruna', 'Carlo', 'Daniela', 'Elisa', 'Fabio', 'Germana',
                'Katia', 'Luca', 'Mariangela', 'Nicola', 'Roberta', 'Simone', 'Vilma', 'William']

NON_PREFERITI = [('Alessandra', 'Elisa'),
                ('Bruna', 'Nicola'),
                ('Carlo', 'Simone'),
                ('Daniela', 'Katia'),
                ('Elisa', 'Fabio'),
                ('Fabio', 'Germana'),
                ('Katia', 'Alessandra'),
                ('Luca', 'William')]

costo_base = 1
penalità_non_preferiti = 1000

# Definizione del modello
modello = LpProblem('SecretSanta', LpMinimize)

# Variabili
x = LpVariable.dicts('x', (PARTECIPANTI, PARTECIPANTI), lowBound=0, upBound=1, cat=LpBinary)

# Vincoli

for i in PARTECIPANTI:
    modello += lpSum(x[i][j] for j in PARTECIPANTI if j != i) == 1 # ognuno regala un libro a qualcun altro
    modello += lpSum(x[k][i] for k in PARTECIPANTI if k != i) == 1 # ognuno riceve un libro da qualcun altro

for i in PARTECIPANTI:
    for j in PARTECIPANTI:
        if i != j:
            modello += x[i][j] + x[j][i] <= 1 # due persone non possono essere assegnate l'uno all'altra

modello += x['Fabio']['Alessandra'] == 1 # Fabio regala un libro ad Alessandra

# Funzione obiettivo
modello += lpSum(x[i][j] for i in PARTECIPANTI for j in PARTECIPANTI)*costo_base + lpSum(x[i][j] for (i,j) in NON_PREFERITI)*penalità_non_preferiti

status = modello.solve(PULP_CBC_CMD(msg=0))

if status == 1:
    print("Funzione obiettivo:", round(value(modello.objective)))
    print("\nAssegnamenti:")
    for i in PARTECIPANTI:
        for j in PARTECIPANTI:
           if x[i][j].varValue > 0:
               print("{} --> {}".format(i,j))