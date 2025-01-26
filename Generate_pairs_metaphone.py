import csv
import ast  # Per interpretare stringhe come liste
from itertools import combinations
import re

# Funzione per caricare il file CSV e organizzare i dati in un dizionario
def load_csv(file_path):
    clusters = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cluster_id, company_names = row
            # Normalizza e interpreta la stringa come lista
            try:
                # Gestisce vari formati di liste (apici singoli o doppi)
                normalized_names = re.sub(r'[\"\']', '"', company_names)
                names_list = ast.literal_eval(normalized_names)
                if isinstance(names_list, list):
                    clusters[cluster_id] = [name.strip() for name in names_list]
            except (ValueError, SyntaxError):
                print(f"Formato non valido nella riga: {row}")
    return clusters

# Funzione per generare tutte le coppie di nomi per ogni cluster
def generate_pairs(clusters):
    pairs = []
    for cluster_id, names in clusters.items():
        if len(names) > 1:  # Genera coppie solo se ci sono almeno due nomi
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
    input_file = 'C:/Users/hp/idd-HW5/merged_similar_matches_metaphone.csv'  # Inserisci il percorso del file CSV in input
    output_file = 'C:/Users/hp/idd-HW5/All_pairs_metaphone.csv'  # Inserisci il percorso del file CSV di output

    # Carica i dati dal file CSV
    clusters = load_csv(input_file)

    # Genera le coppie di nomi
    pairs = generate_pairs(clusters)

    # Salva le coppie generate nel file CSV
    save_csv(pairs, output_file)

    print(f"Le coppie generate sono state salvate in: {output_file}")
