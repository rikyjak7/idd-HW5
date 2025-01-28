import pandas as pd
import recordlinkage
from recordlinkage import Compare
from sklearn.metrics import precision_score, recall_score, f1_score

# 1. Caricamento dei dati
clusters_df = pd.read_csv('C:/Users/hp/idd-HW5/updated_clusters.csv')  # Percorso del file clusters.csv
ground_truth_df = pd.read_csv('C:/Users/hp/idd-HW5/GROUND_TRUTH.csv', names=['company_name1', 'company_name2', 'label'])  # Percorso del file GROUND_TRUTH.csv

# 2. Preprocessing dei dati
clusters_df = clusters_df.dropna(subset=['Company Name'])
cluster_dict = {}
for _, row in clusters_df.iterrows():
    cluster_id = row['Cluster ID']
    if isinstance(row['Company Name'], str):
        companies = row['Company Name'].split(', ')
    else:
        companies = []  
    cluster_dict[cluster_id] = companies

candidate_pairs = []
max_companies_per_cluster = 50  

for cluster_id, companies in cluster_dict.items():
    if len(companies) > max_companies_per_cluster:
        companies = companies[:max_companies_per_cluster]
    for i in range(len(companies)):
        for j in range(i + 1, len(companies)):
            candidate_pairs.append((companies[i], companies[j], cluster_id))

candidate_df = pd.DataFrame(candidate_pairs, columns=['company_name1', 'company_name2', 'cluster_id'])

# 3. Creazione dei matcher
indexer = recordlinkage.Index()
indexer.block('cluster_id')  
candidate_pairs_index = indexer.index(candidate_df)

comparator = Compare()
comparator.string('company_name1', 'company_name2', method='jaro_winkler', threshold=0.60, label='company_name')  # Soglia abbassata

features = comparator.compute(candidate_pairs_index, candidate_df)

# 4. Calcolo delle previsioni
predictions = features['company_name'] > 0.60  

results_df = pd.DataFrame({
    'company_name1': candidate_df['company_name1'],
    'company_name2': candidate_df['company_name2'],
    'prediction': predictions
})

# Debug: Verifica le prime righe di results_df
print("Prime righe di results_df:")
print(results_df.head())

# Creiamo una colonna di coppie
ground_truth_df['pair'] = list(zip(ground_truth_df['company_name1'], ground_truth_df['company_name2']))
results_df['pair'] = list(zip(results_df['company_name1'], results_df['company_name2']))

# Stampa le dimensioni dei dataframe prima del merge
print(f"Dimensione di results_df: {results_df.shape}")
print(f"Dimensione di ground_truth_df: {ground_truth_df.shape}")
# Debug: Stampa i dati di alcune righe del dataframe ground_truth_df
print(ground_truth_df.head())


# 5. Uniamo i risultati con il ground truth per il calcolo delle metriche
merged_results = pd.merge(ground_truth_df, results_df, on=['pair'], how='left', indicator=True)

# Stampa la dimensione dopo il merge
print(f"Dimensione dopo il merge: {merged_results.shape}")
print("Prime righe del risultato del merge:")
print(merged_results.head())

# 6. Calcolo delle metriche
TP = merged_results[(merged_results['_merge'] == 'both') & (merged_results['label'] == 1)].shape[0]
FP = merged_results[(merged_results['_merge'] == 'right_only') & (merged_results['label'] == 0)].shape[0]
TN = merged_results[(merged_results['_merge'] == 'left_only') & (merged_results['label'] == 0)].shape[0]
FN = merged_results[(merged_results['_merge'] == 'both') & (merged_results['label'] == 0)].shape[0]

precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Output delle metriche
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
