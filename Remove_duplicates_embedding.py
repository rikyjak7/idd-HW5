import csv
from collections import defaultdict

# Funzione per caricare il file CSV e organizzare i dati in un dizionario
def load_csv(file_path):
    clusters = defaultdict(str)
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione del file (se presente)
        for row in reader:
            cluster_id, company_names = row
            clusters[int(cluster_id)] = company_names
    return clusters

# Funzione per rimuovere i duplicati preservando l'ordine
def process_clusters(clusters):
    updated_clusters = {}
    for cluster_id, names in clusters.items():
        # Split dei nomi basato sulle virgole e rimozione di spazi extra
        name_list = [name.strip() for name in names.split(",")]
        # Deduplicazione preservando l'ordine
        seen = set()
        unique_names = []
        for name in name_list:
            if name not in seen:
                unique_names.append(name)
                seen.add(name)
        # Ricostruzione della stringa unendo i nomi con una virgola
        updated_clusters[cluster_id] = ", ".join(unique_names)
    return updated_clusters

# Funzione per salvare i dati aggiornati in un nuovo file CSV
def save_csv(clusters, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Cluster ID", "Company Name"])
        for cluster_id, names in clusters.items():
            writer.writerow([cluster_id, names])

# Esempio di utilizzo
input_file = 'C:/Users/hp/idd-HW5/clustered_companies.csv'  # Inserisci il percorso del file CSV in input
output_file = 'C:/Users/hp/idd-HW5/updated_clusters.csv'  # Inserisci il percorso del file CSV di output

# Carica i dati dal file CSV
clusters = load_csv(input_file)

# Rimuovi i duplicati e processa i cluster
updated_clusters = process_clusters(clusters)

# Salva i dati aggiornati nel file CSV
save_csv(updated_clusters, output_file)

print(f"I cluster aggiornati sono stati salvati in: {output_file}")
