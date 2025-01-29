import deepmatcher as dm
import pandas as pd
import torch
import os

# ===== 1. CARICAMENTO DEL MODELLO PRE-ADDESTRATO =====
MODEL_PATH = '/home/vboxuser/Documents/GitHub/idd-HW5/best_model.pth'
print(f"Caricamento del modello da {MODEL_PATH}...")
model = dm.MatchingModel(attr_summarizer='rnn')
model.load_state(MODEL_PATH)
print("Modello caricato con successo!")

# ===== 2. PRE-ELABORAZIONE DEI DATI DI TEST =====
TEST_DATA_PATH = '/home/vboxuser/Documents/GitHub/idd-HW5/csv_files/model_testing/unified_embedding_with_id.csv'
print(f"Pre-elaborazione dei dati di test da {TEST_DATA_PATH}...")

# Verifica che il file esista
if not os.path.exists(TEST_DATA_PATH):
    print(f"Errore: Il file {TEST_DATA_PATH} non esiste!")
else:
    # Disabilita la cache per evitare l'errore di serializzazione
    predict_data = dm.data.process(
        path='',
        test=TEST_DATA_PATH,
        cache=False
    )

# ===== 3. ESECUZIONE DELLE PREVISIONI =====
predictions = model.run_prediction(predict_data, output_attributes=True)

# Debug: Stampa le colonne di `predictions`
print("Colonne disponibili in predictions:", predictions.columns)

# Prepara il DataFrame per l'output
output_df = pd.DataFrame({
    'Name1': predictions['left_name'],  # Colonna disponibile per il nome a sinistra
    'Name2': predictions['right_name'],  # Colonna disponibile per il nome a destra
    'Similarity': predictions['match_score']  # Score di corrispondenza
})

# ===== 4. SALVATAGGIO DELLE PREVISIONI =====
output_path='/home/vboxuser/Documents/GitHub/idd-HW5/csv_files/model_testing/deepmatch_predictions_embedding.csv'
output_df.to_csv(output_path, index=False)
print(f"Predizioni DeepMatcher salvate in: {output_path}")
