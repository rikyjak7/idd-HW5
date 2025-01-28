import pandas as pd
from sklearn.cluster import DBSCAN
from sentence_transformers import SentenceTransformer
from collections import defaultdict

# Carica il file CSV
dataframe = pd.read_csv("C:/Users/hp/idd-HW5/csv_files/mediated_schema.csv", encoding='latin1', low_memory=False)

# Converte tutte le colonne in stringhe
dataframe = dataframe.astype(str)

# Pulizia delle stringhe: rimozione degli spazi extra e conversione in minuscolo
if 'Company Name' in dataframe.columns:
    dataframe['Company Name'] = dataframe['Company Name'].str.strip().str.lower()

# Inizializza il modello per calcolare gli embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Calcola gli embedding per i nomi delle compagnie
company_names = dataframe['Company Name'].tolist()
embeddings = model.encode(company_names)

# Esegui DBSCAN direttamente sui vettori di embedding senza ridurre le dimensioni (PCA non necessaria)
db = DBSCAN(eps=0.18, min_samples=1, metric='cosine')  # Prova con un valore più grande di eps per una similarità più generale
labels = db.fit_predict(embeddings)

# Crea un dizionario per raggruppare le compagnie per cluster
grouped_names = defaultdict(list)
for i, label in enumerate(labels):
    if label != -1:  # Escludi i punti considerati rumore
        grouped_names[label].append(company_names[i])

# Crea il DataFrame finale con Cluster ID e Nomi delle Compagnie
final_results = []
for cluster_id, companies in grouped_names.items():
    final_results.append([cluster_id, ", ".join(companies)])  # Unisci i nomi in una stringa separata da virgole

# Salva i risultati in un file CSV
output_df = pd.DataFrame(final_results, columns=['Cluster ID', 'Company Names'])
output_df.to_csv("C:/Users/hp/idd-HW5/csv_files/clustered_embedding.csv", index=False, encoding='utf-8')

print("Clustering completato. Risultati salvati in 'clustered_companies.csv'.")
