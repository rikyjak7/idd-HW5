import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import random

# Carica i dati dal file CSV
df = pd.read_csv('C:/Users/hp/idd-HW5/csv_files/cleaned_clustered_embedding.csv')

# Crea il grafo vuoto
G = nx.Graph()

# Aggiungere nodi per ciascun cluster
cluster_dict = {}

for _, row in df.iterrows():
    cluster = row['cluster']
    companies = row['name'] if isinstance(row['name'], str) else ""
    
    if companies:
        companies = companies.split(", ")
    
    if cluster not in cluster_dict:
        cluster_dict[cluster] = []
    cluster_dict[cluster].extend(companies)

# Parametro per selezionare 20 cluster casuali con al massimo 20 nodi
random_clusters = True  # Imposta a True per selezionare 20 cluster casuali con al massimo 20 nodi
max_nodes_per_cluster = 20

# Filtrare i cluster che hanno più di un nodo e al massimo 20 nodi
filtered_clusters = {cluster: companies for cluster, companies in cluster_dict.items() if 1 < len(companies) <= max_nodes_per_cluster}

# Seleziona 20 cluster casuali
if random_clusters:
    selected_clusters = random.sample(list(filtered_clusters.keys()), min(20, len(filtered_clusters)))
else:
    # Seleziona solo i primi 20 cluster se random_clusters è False
    selected_clusters = list(filtered_clusters.keys())[:20]

# Filtriamo i nodi da visualizzare (cluster selezionati)
clusters_to_keep = {cluster: companies for cluster, companies in filtered_clusters.items() if cluster in selected_clusters}

# Aggiungi i nodi al grafo con un attributo 'cluster'
for cluster, companies in clusters_to_keep.items():
    for company in companies:
        G.add_node(company, cluster=cluster)

# Crea una posizione random per ciascun cluster con maggiore separazione
pos = {}
for cluster, companies in clusters_to_keep.items():
    # Posizione casuale per il centro del cluster con maggiore separazione
    center_x = random.uniform(-20, 20)  # Maggiore separazione tra i cluster
    center_y = random.uniform(-20, 20)  # Maggiore separazione tra i cluster
    
    # Assegna le posizioni ai nodi di ciascun cluster, rendendoli vicini tra loro
    for i, company in enumerate(companies):
        pos[company] = (center_x + random.uniform(-1, 1), center_y + random.uniform(-1, 1))

# Parametro per visualizzare o meno i nomi dei nodi
show_labels = True  # Imposta a True per visualizzare i nomi, False per non visualizzarli

# Disegna il grafo
plt.figure(figsize=(15, 15))

# Colori distinti per ciascun cluster
unique_colors = plt.cm.tab20.colors
cluster_colors = {cluster: unique_colors[i % len(unique_colors)] for i, cluster in enumerate(clusters_to_keep)}

# Disegna i nodi con colori distinti per ciascun cluster
node_colors = [cluster_colors[G.nodes[node]['cluster']] for node in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=120, node_color=node_colors, alpha=0.8)

# Disegna le etichette dei nodi (azienda), se show_labels è True
if show_labels:
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='black')

# Aggiungi una legenda con i veri ID dei cluster
import matplotlib.patches as mpatches
handles = [mpatches.Patch(color=color, label=f'Cluster {cluster}') for cluster, color in cluster_colors.items()]
plt.legend(handles=handles, loc='upper left', fontsize=8)

# Mostra il grafo
plt.title("Visualizzazione dei Cluster con Separazione Maggiore")
plt.axis('off')
plt.show()
