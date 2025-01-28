import csv

# Funzione per leggere il file delle coppie effettive e convertirlo in un set
def load_actual_pairs(file_path):
    actual_pairs = set()
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione del file
        for row in reader:
            cluster_id, name1, name2 = row
            # Aggiungi le coppie in ordine canonico per confronto
            actual_pairs.add(tuple(sorted([name1.strip(), name2.strip()])))
    return actual_pairs

# Funzione per calcolare la metrica richiesta
def calculate_metric(hypothetical_file, actual_pairs):
    total_contributions = 0
    counter = 0

    with open(hypothetical_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name1, name2, flag = row
            flag = int(flag.strip())
            pair = tuple(sorted([name1.strip(), name2.strip()]))

            total_contributions += 1

            if pair in actual_pairs and flag == 1:
                counter += 1
            elif pair not in actual_pairs and flag == 0:
                counter += 1

    # Calcola il rapporto
    accuracy = counter / total_contributions if total_contributions > 0 else 0
    return accuracy


hypothetical_file = 'C:/Users/hp/idd-HW5/csv_files/GROUND_TRUTH.csv'  # File con tutte le coppie effettive
actual_pairs_file = 'C:/Users/hp/idd-HW5/csv_files/all_pairs_embedding.csv'  # File con le coppie ipotetiche

# Carica le coppie effettive
actual_pairs = load_actual_pairs(actual_pairs_file)

# Calcola la metrica
accuracy = calculate_metric(hypothetical_file, actual_pairs)

print(f"L'accuracy calcolata è: {accuracy:.4f}")