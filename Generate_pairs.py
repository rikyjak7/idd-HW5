import csv
from itertools import combinations
from collections import defaultdict

# Funzione per caricare il file CSV e organizzare i dati in un dizionario
def load_csv(file_path):
    clusters = defaultdict(list)
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione del file (se presente)
        for row in reader:
            cluster_id, company_names = row
            # Rimuovi spazi e separa i nomi contenuti tra virgolette
            names_list = [name.strip() for name in company_names.strip('"').split(",")]
            clusters[int(cluster_id)].extend(names_list)
    return clusters

# Funzione per generare tutte le coppie di nomi per ogni cluster
def generate_pairs(clusters):
    pairs = []
    for cluster_id, names in clusters.items():
        for pair in combinations(names, 2):
            pairs.append((cluster_id, pair[0], pair[1]))
    return pairs

# Funzione per salvare le coppie generate in un file CSV
def save_csv(pairs, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Cluster ID", "Company Name 1", "Company Name 2"])
        for cluster_id, name1, name2 in pairs:
            writer.writerow([cluster_id, name1, name2])

# Esempio di utilizzo
if __name__ == "__main__":
    input_file = 'C:/Users/hp/idd-HW5/updated_clusters.csv'  # Inserisci il percorso del file CSV in input
    output_file = 'C:/Users/hp/idd-HW5/All_pairs.csv'  # Inserisci il percorso del file CSV di output

    # Carica i dati dal file CSV
    clusters = load_csv(input_file)

    # Genera le coppie di nomi
    pairs = generate_pairs(clusters)

    # Salva le coppie generate nel file CSV
    save_csv(pairs, output_file)

    print(f"Le coppie generate sono state salvate in: {output_file}")
