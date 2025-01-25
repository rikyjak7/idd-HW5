import pandas as pd
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Carica il file CSV
try:
    dataframe = pd.read_csv("mediated_schema.csv", encoding='latin1', low_memory=False)
except UnicodeDecodeError as e:
    print(f"Errore nella lettura del file CSV: {e}")
    dataframe = pd.DataFrame()  # Inizializza un DataFrame vuoto in caso di errore

# Converte tutte le colonne in stringhe
dataframe = dataframe.astype(str)

# Pulizia delle stringhe: rimozione degli spazi extra e conversione in minuscolo
if 'Company Name' in dataframe.columns:
    dataframe['Company Name'] = dataframe['Company Name'].str.strip().str.lower()
else:
    print("La colonna 'Company Name' non esiste nel dataset.")

# Inizializza il modello per calcolare gli embedding
model = SentenceTransformer('all-MiniLM-L6-v2')  # Modello leggero ma efficace per embedding semantici

# Calcola gli embedding per i nomi delle compagnie
if 'Company Name' in dataframe.columns:
    company_names = dataframe['Company Name'].tolist()
    embeddings = model.encode(company_names, convert_to_tensor=True)
else:
    print("La colonna 'Company Name' non esiste nel dataset.")
    company_names = []
    embeddings = []

# Soglia di similarità per unione dei gruppi
similarity_threshold = 0.85  # Valore tra 0 e 1

# Costruzione dei gruppi basati sugli embedding
grouped_names = defaultdict(list)
visited = set()

for i, company_name in enumerate(company_names):
    if i in visited:
        continue

    # Gruppo corrente che inizialmente contiene solo l'elemento di partenza
    current_group = [company_name]
    visited.add(i)

    # Calcola le similarità con tutti gli altri nomi
    for j in range(len(company_names)):
        if j not in visited:
            sim_score = cosine_similarity(embeddings[i].unsqueeze(0), embeddings[j].unsqueeze(0))[0][0]
            if sim_score >= similarity_threshold:
                current_group.append(company_names[j])
                visited.add(j)

    # Aggiungi il gruppo finale al dizionario
    grouped_names[company_name].extend(list(set(current_group)))

# Prepara i risultati finali
final_results = []
for key, company_names in grouped_names.items():
    final_results.append((key, company_names))

# Crea un DataFrame con i risultati
similar_matches = pd.DataFrame(final_results, columns=['Representative Name', 'Similar Company Names'])
print("Raggruppamenti semantici basati su embedding:")
print(similar_matches)

# Salva i risultati in un file CSV
output_filename = "merged_similar_matches_embeddings.csv"
similar_matches.to_csv(output_filename, index=False, encoding='utf-8')
print(f"Risultati salvati nel file: {output_filename}")