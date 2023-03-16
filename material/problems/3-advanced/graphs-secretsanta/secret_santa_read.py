#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 09:50:41 2022

@author: Alice Raffaele
"""

from pulp import *


def leggi_input(nome_file):
    PARTECIPANTI = []
    NON_PREFERITI = []
    FISSATI = []
    costo_base = 0
    penalità_non_preferiti = 0
    with open(nome_file, 'r') as file:
       while True:
           riga = file.readline()
           if not riga:
               break
           if "PARTECIPANTI" in riga:
               riga_pezzi = riga.split()
               PARTECIPANTI = riga_pezzi[2:]
           if "NUM_NON_PREFERITI" in riga:
               riga_pezzi = riga.split()
               num_non_preferiti = int(riga_pezzi[2])
               for i in range(num_non_preferiti):
                   riga = file.readline()
                   riga_pezzi = riga.split()
                   coppia = (riga_pezzi[0], riga_pezzi[1])
                   NON_PREFERITI += [coppia]
           if "NUM_FISSATI" in riga:
               riga_pezzi = riga.split()
               num_fissati = int(riga_pezzi[2])
               for i in range(num_fissati):
                   riga = file.readline()
                   riga_pezzi = riga.split()
                   coppia = (riga_pezzi[0], riga_pezzi[1])
                   FISSATI += [coppia]
           if "COSTO_BASE" in riga:
               riga_pezzi = riga.split()
               costo_base = int(riga_pezzi[2])
           if "PENALITA_NON_PREFERITI" in riga:
               riga_pezzi = riga.split()
               penalità_non_preferiti = int(riga_pezzi[2])

    return PARTECIPANTI, NON_PREFERITI, FISSATI, costo_base, penalità_non_preferiti

PARTECIPANTI, NON_PREFERITI, FISSATI, costo_base, penalità_non_preferiti = leggi_input('secret_santa_instance.txt')

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

for (i,j) in FISSATI:
    modello += x[i][j] == 1

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
