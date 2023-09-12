from pulp import *
import math

# Metodo per leggere un file di testo contenente un'istanza del problema VRP Challenge
def leggi_input(nome_file):
    clienti = {}
    supermercati = {}
    veicoli = {}
    tempi = {}
    num_supermercati = 0
    num_clienti = 0
    num_veicoli = 0
    costo_benzina_minuto = 0
    tempo_servizio = 0
    coto_fisso_veicolo = 0
    
    with open(nome_file, 'r') as file: # Apre il file di testo
        while True: # Ciclo while infinito, almeno fino a quando non c'è un'istruzione break
            riga = file.readline() # Legge una riga
            if not riga:
                break # Se non ci sono più righe da leggere (cioè, se si è letto tutto il testo), allora interrompe il ciclo
            if "CLIENTI :" in riga:
                # riga.split() trasforma la stringa in una lista, spezzettandola dove ci sono degli spazi vuoti
                num_clienti = int(riga.split()[2]) # Legge il numero di clienti come stringa e lo converte a intero
            if "SUPERMERCATI :" in riga:
                num_supermercati = int(riga.split()[2]) # Legge il numero di supermercati
            if "VEICOLI :" in riga:
                num_veicoli = int(riga.split()[2]) # Legge il numero di veicoli
            if "COSTO_BENZINA_MINUTO :" in riga:
                costo_benzina_minuto = float(riga.split()[2]) # Legge il costo della benzina al minuto
            if "TEMPO_SERVIZIO" in riga:
                tempo_servizio = int(riga.split()[2]) # Legge il tempo di servizio
            if "COSTO_FISSO_VEICOLO" in riga:
                costo_fisso_veicolo = int(riga.split()[2]) # Legge il costo fisso di ogni veicolo
            if "ID-DOMANDA :" in riga:
                for i in range(1, num_supermercati+1): # Legge una riga per ogni supermercato
                    riga = file.readline()
                    supermercati[i] = {} # Inizializza un dizionario per ogni “nuovo” supermercato
                    supermercati[i]['num_borse'] = 0 # Per ogni supermercato, il numero di borse è 0
                    supermercati[i]['tempo_servizio'] = 0 # e così anche il tempo di servizio 
                for i in range(num_supermercati+1, num_supermercati+num_clienti+1): # Legge una riga per ogni cliente (la cui numerazione parte da num_supermercati+1)
                    riga = file.readline()
                    clienti[i] = {} # Inizializza un dizionario per ogni “nuovo” cliente
                    clienti[i]['num_borse'] = int(riga.split()[1]) # Legge il numero di borse
                    clienti[i]['tempo_servizio'] = math.ceil(clienti[i]['num_borse']/2)*tempo_servizio # Calcola il tempo totale di servizio del cliente 
            if "NODO1-NODO2-TEMPO :" in riga:
                for i in range(1,num_clienti+num_supermercati+1): # Inizializzazione del dizionario dei tempi
                    tempi[i] = {} # Per ogni nodo i (sia supermercato sia cliente), crea un altro dizionario
                    for j in range(1,num_clienti+num_supermercati+1): # Per ogni nodo j, inizializza il tempo in minuti per percorrere l'arco (i,j) a un valore alto
                        tempi[i][j] = 1999
                riga = file.readline() # Legge l'informazione sul tempo di percorrenza dell'arco (i,j)
                while(riga != "\n"): # Ciclo finché ci sono archi da leggere (finché la riga letta è diversa dal carattere per andare a capo)
                    riga_pezzi = riga.split()
                    nodo_i = int(riga_pezzi[0]) # Il primo pezzo è il nodo i
                    nodo_j = int(riga_pezzi[1]) # Il secondo elemento è il nodo j
                    tempo_ij = int(riga_pezzi[2]) # Il terzo è il tempo in minuti per percorrere (i,j)
                    tempi[nodo_i][nodo_j] = tempo_ij # Salva nel dizionario il tempo 
                    riga = file.readline()
            if "ID-TMAX-CAPACITA-SUPERMERCATO :" in riga:
                for i in range(1, num_veicoli+1):
                    veicoli[i] = {} # Inizializza un dizionario per ogni “nuovo” veicolo
                    riga = file.readline() # Legge le informazioni corrispondenti
                    riga_pezzi = riga.split()
                    veicoli[i]['tempo_max'] = int(riga_pezzi[1]) # Tempo massimo di utilizzo
                    veicoli[i]['capacità'] = int(riga_pezzi[2]) # Capacità massima (massimo numero di borse consentito)
                    veicoli[i]['supermercato'] = int(riga_pezzi[3]) # Supermercato di partenza e arrivo
    file.close() # Chiude il file di testo
    
    return clienti, supermercati, veicoli, tempi, costo_benzina_minuto, tempo_servizio, costo_fisso_veicolo

nome_istanza = 'instance-demo.txt'
clienti, supermercati, veicoli, tempi, costo_benzina_minuto, tempo_servizio, costo_fisso_veicolo = leggi_input(nome_istanza)

# Per comodità da usare nei vincoli, definiamo:
C = list(clienti.keys())
S = list(supermercati.keys())
V = list(veicoli.keys())

# DEFINIZIONE PROBLEMA CON PULP
modello = LpProblem("VRP-Challenge", LpMinimize)

# VARIABILI
u = LpVariable.dicts("u", V, 0, 1, LpBinary) # uso o non uso il veicolo v?
y = LpVariable.dicts("y", (C, V), 0, 1, LpBinary) # assegno o non assegno il cliente c al veicolo v?
x = LpVariable.dicts("x", (S+C, S+C, V), 0, 1, LpBinary) # il tratto (i,j) è percorso o no dal veicolo v?
q = LpVariable.dicts("q", (S+C, S+C, V), 0, None, LpContinuous) # in quale istante giunge il veicolo v nel nodo j partendo da i? (servono per i vincoli di eliminazione dei cicli)

# OBIETTIVO: minimizzare i costi totali (costi fissi di utilizzo veicoli + costi variabili di trasporto)


# VINCOLI
# a) ogni cliente c è assegnato a esattamente un veicolo v


# b) ogni cliente c può essere servito da un veicolo v solo se il veicolo v è effettivamente usato


# c) per ogni veicolo v, la somma del numero di borse dei clienti assegnati a v non può superare la capacità massima di v


# d) ogni veicolo v parte dal suo supermercato per raggiungere un altro nodo solo se è usato
for v in V:
    modello += lpSum(x[veicoli[v]['supermercato']][i][v] for i in S+C if i != veicoli[v]['supermercato']) >= u[v]

# e) ogni veicolo v, se serve un cliente c, deve arrivare in c da almeno un altro nodo
for v in V:
    for c in C:
        modello += lpSum(x[j][c][v] for j in S+C if j != c) >= y[c][v]

# f) per ogni veicolo v e per ogni nodo i, vale la conservazione del flusso
# (il numero di archi k entranti in i che vengono selezionati è uguale al numero di archi j uscenti da i)
for v in V:
    for i in S+C:
        modello += lpSum(x[k][i][v] for k in S+C if i != k) == lpSum(x[i][j][v] for j in S+C if i != j)

# g) per ogni veicolo v, il tempo totale impiegato da quando esce dal suo supermercato di partenza a quando rientra,
# tenendo conto anche dei tempi di servizio ai clienti a lui assegnati, non può superare il suo tempo massimo
for v in V:
      modello += lpSum(x[i][j][v]*tempi[i][j] for i in S+C for j in S+C if i != j) + lpSum(y[c][v]*clienti[c]['tempo_servizio'] for c in C) <= veicoli[v]['tempo_max']

# h) vincoli avanzati per evitare di formare sottocicli e consentire di visitare più volte lo stesso nodo (Sciomachen)
for v in V:
    index_depot = veicoli[v]['supermercato']
    for i in S+C:
        if i != index_depot:
            modello += lpSum(q[i][j][v] for j in S+C if j != i) - lpSum(q[j][i][v] for j in S+C if j != i) == lpSum(tempi[i][j]*x[i][j][v] for j in S+C if j != i) 
            modello += q[index_depot][i][v] == tempi[index_depot][i]*x[index_depot][i][v]
        for j in S+C:
            if j != i:
                modello += q[i][j][v] <= veicoli[v]['tempo_max']*x[i][j][v]
                modello += q[i][j][v] >= tempi[i][j]*x[i][j][v]             

# RISOLUZIONE

status = modello.solve(PULP_CBC_CMD(msg=0))
if status == 1:
    # STAMPA SOLUZIONE OTTIMA
    print("SOLUZIONE OTTIMA TROVATA")
    print("\nValore della funzione obiettivo all'ottimo = {} euro".format(round(value(modello.objective), 2)))
    for v in V:
        if u[v].varValue > 0:
            capacita_sfruttata = 0
            tempo_richiesto = 0
            testo_veicolo = "\nIl veicolo {} è usato e serve i seguenti clienti: ".format(v)
            for c in C:
                #print("y_{}_{} = {}".format(c,v,y[c][v].varValue))
                if y[c][v].varValue > 0:
                    testo_veicolo += str(c) + ' '
                    capacita_sfruttata += clienti[c]['num_borse']
            print(testo_veicolo)
            for i in S+C:
                for j in S+C:
                    if i != j:
                        if x[i][j][v].varValue > 0:
                            print("{} -> {}".format(i,j))
                            #print(x[i][j][v].name, "=", x[i][j][v].varValue)
                            tempo_richiesto += tempi[i][j]
            print("Capacità sfruttata = {}/{} borse".format(capacita_sfruttata, veicoli[v]['capacità']))
            print("Tempo richiesto = {}/{} minuti".format(tempo_richiesto, veicoli[v]['tempo_max']))
