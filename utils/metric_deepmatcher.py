import csv
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# File di input
#file_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/model_testing/deepmatch_predictions_embedding.csv"  # File con le coppie effettive
file_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/model_testing/deepmatch_predictions_metaphone.csv"
ground_truth_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/GROUND_TRUTH.csv"  # File con la ground truth (coppie e label)

# Lettura delle coppie effettive dal file principale
effettive = {}  # Usa un dizionario per associare la similarità alle coppie
with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        company1 = row["Name1"]
        company2 = row["Name2"]
        similarity = float(row["Similarity"])  # Legge la similarità direttamente dal file
        effettive[(company1, company2)] = similarity

# Lettura della ground truth e verifica
y_true = []  # Label della ground truth
y_pred = []  # Previsioni basate sulla similarità
threshold = 0.7  # Soglia per considerare una similarità "alta"

false_positives = 0
false_negatives = 0
match_counter = 0

false_positives_pairs = []
false_negatives_pairs = []

with open(ground_truth_path, "r", newline="", encoding="utf-8") as gt_file:
    gt_reader = csv.reader(gt_file)
    
    # Salta l'intestazione del file di ground truth
    next(gt_reader, None)
    
    for row in gt_reader:
        if len(row) < 3:  # Salta righe incomplete
            continue
        
        company1, company2, label = row[0], row[1], int(row[2])
        y_true.append(label)  # Aggiungi la label della ground truth
        
        # Verifica se la coppia è presente nel file effettivo
        similarity = effettive.get((company1, company2), 0.0)  # Ottiene la similarità o 0.0 se la coppia non è presente
        pair_present = (company1, company2) in effettive
        
        # Logica di predizione
        if label == 1:
            # Se la coppia deve essere presente
            if pair_present and similarity >= threshold:
                prediction = 1 
            else:
                prediction = 0
                false_negatives += 1
                false_negatives_pairs.append((company1, company2))
        else:
            # Se la coppia non deve essere presente
            if pair_present:
                prediction = 1 
                false_positives += 1
                false_positives_pairs.append((company1, company2))
            else:
                prediction = 0
        
        # Aggiungi la previsione
        y_pred.append(prediction)
        
        # Determina il risultato (match o mismatch con la ground truth)
        if prediction == label:
            match_counter += 1

# Calcolo delle metriche
precision = match_counter / 120
recall = match_counter / (match_counter + false_positives)
f1 = (2 * precision * recall) / (precision + recall)
accuracy = accuracy_score(y_true, y_pred)

# Stampa delle metriche
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"Accuracy: {accuracy:.4f}")

print(false_negatives)
print(false_positives)

print(f"false_negative_pairs: {false_negatives_pairs}")
print(f"false_positive_pairs: {false_positives_pairs}")
