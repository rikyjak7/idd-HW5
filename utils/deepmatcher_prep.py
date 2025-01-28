import pandas as pd
import jellyfish

# Funzione per calcolare la similarità usando Jaro-Winkler
def calculate_similarity(name1, name2, threshold=0.70):
    name1 = str(name1) if name1 is not None else ''
    name2 = str(name2) if name2 is not None else ''
    similarity = jellyfish.jaro_winkler_similarity(name1, name2)
    return 1 if similarity >= threshold else 0

# Carica il CSV
input_file = "/home/trabbo/Documents/GitHub/idd-HW5/csv_files/all_pairs_embedding.csv"  # Sostituisci con il tuo file
output_file = "/home/trabbo/Documents/GitHub/idd-HW5/csv_files/train_pairs_embedding.csv"  # Il file di output con la nuova colonna "label"

# Carica i dati nel DataFrame
df = pd.read_csv(input_file)

# Aggiungi la colonna 'label' calcolata tramite la funzione di similarità
df['label'] = df.apply(lambda row: calculate_similarity(row['Company_Name_1'], row['Company_Name_2']), axis=1)

label_counts = df['label'].value_counts()
# Stampa il conteggio delle etichette 0 e 1
print(f"Numero di label 1: {label_counts.get(1, 0)}")
print(f"Numero di label 0: {label_counts.get(0, 0)}")

# Seleziona solo le colonne richieste per l'output
output_df = df[['Company_Name_1', 'Company_Name_2', 'label']]

# Salva il DataFrame con la nuova colonna in un nuovo file CSV
output_df.to_csv(output_file, index=False)


