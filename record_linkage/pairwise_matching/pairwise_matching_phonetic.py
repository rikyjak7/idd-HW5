import jellyfish
import csv
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# File di input e output
file_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/all_pairs_metaphone.csv"  # File con le coppie effettive
ground_truth_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/GROUND_TRUTH.csv"  # File con la ground truth (coppie e label)
output_path = "C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/csv_files/output_fonetic_recordLinkage.csv"  # File per salvare i risultati

# Lettura delle coppie effettive dal file principale
effettive = set()  # Usa un set per un lookup veloce
with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        company1 = row["Company_Name_1"]
        company2 = row["Company_Name_2"]
        effettive.add((company1, company2))

# Lettura della ground truth e verifica
y_true = []  # Label della ground truth
y_pred = []  # Previsioni basate sulla similarità
threshold = 0.7  # Soglia per considerare una similarità "alta"

false_positives=0
false_negatives=0
true_positives=0
true_negatives=0

false_positives_pairs=[]
false_negatives_pairs=[]

with open(ground_truth_path, "r", newline="", encoding="utf-8") as gt_file, \
     open(output_path, "w", newline="", encoding="utf-8") as outputfile:
    
    gt_reader = csv.reader(gt_file)
    writer = csv.writer(outputfile)
    
    # Scrivi l'intestazione nel file di output
    writer.writerow(["Company_Name_1", "Company_Name_2", "Ground_Truth", "Similarity", "Prediction", "Result"])
    
    # Salta l'intestazione del file di ground truth
    next(gt_reader, None)
    
    for row in gt_reader:
        if len(row) < 3:  # Salta righe incomplete
            continue
        
        company1, company2, label = row[0], row[1], int(row[2])
        y_true.append(label)  # Aggiungi la label della ground truth
        
        # Verifica se la coppia è presente nel file effettivo
        pair_present = (company1, company2) in effettive
        similarity = 0.0  # Default
        
        if pair_present:
            # Calcola la similarità se la coppia è presente
            similarity = jellyfish.jaro_winkler_similarity(company1, company2)
        
        # Logica di predizione
        if label == 1:
            # Se la coppia deve essere presente
            if pair_present and similarity >= threshold:
                prediction = 1 
                true_positives+=1
            else:
                prediction = 0
                false_negatives+=1
                false_negatives_pairs.append((company1,company2))
        else:
            # Se la coppia non deve essere presente
            if pair_present:
                prediction = 1 
                false_positives+=1
                false_positives_pairs.append((company1,company2))
            else:
                prediction=0
                true_negatives+=1
        
        # Aggiungi la previsione
        y_pred.append(prediction)
        
        # Determina il risultato (match o mismatch con la ground truth)
        result = "Match" if prediction == label else "Mismatch"
        
        
        # Salva i risultati
        writer.writerow([company1, company2, label, f"{similarity:.4f}", prediction, result])

# Calcolo delle metriche
precision = true_positives/(true_positives+false_positives)
recall = true_positives/(true_positives+false_negatives)
f1 = (2*precision*recall)/(precision+recall)
accuracy = accuracy_score(y_true, y_pred)
accuracy1=(true_positives+true_negatives)/(true_positives+true_negatives+false_negatives+false_positives)

# Stampa delle metriche
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy1:.4f}")

print(false_negatives)
print(f"false_negative_pairs:{false_negatives_pairs}")
print(false_positives)
print(f"false_positive_pairs:{false_positives_pairs}")

