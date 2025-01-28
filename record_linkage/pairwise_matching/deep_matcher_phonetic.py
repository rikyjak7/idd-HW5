import deepmatcher as dm

import pandas as pd
 
# ===== 1. PRE-ELABORAZIONE DEI DATI =====

# Carica e processa i dati di training

print("Pre-elaborazione dei dati di training e validation...")

train, validation = dm.data.process(

    path='/home/trabbo/Documents/GitHub/idd-HW5/csv_files/train_pairs_metaphone.csv',           # Percorso al file train.csv

    validation_split=0.2,       # Suddivide il 20% dei dati di training in un set di validazione

    ignore_columns=('label',),  # Ignora la colonna "label" durante la pre-elaborazione

    left_prefix='left_',        # Prefisso per le colonne "left_name"

    right_prefix='right_'       # Prefisso per le colonne "right_name"

)
 
# Carica e processa i dati di test

print("Pre-elaborazione dei dati di test...")

test = dm.data.process(

    path='/home/trabbo/Documents/GitHub/idd-HW5/csv_files/validation_pairs_metaphone.csv',            # Percorso al file test.csv

    ignore_columns=('label',),  # Ignora la colonna "label"

    left_prefix='left_',        # Prefisso per le colonne "left_name"

    right_prefix='right_'       # Prefisso per le colonne "right_name"

)
 
# ===== 2. CREAZIONE DEL MODELLO =====

# Inizializza il modello DeepMatcher

print("Creazione del modello...")

model = dm.MatchingModel(attr_summarizer='rnn')  # Usa RNN come attributo sintetizzatore
 
# ===== 3. ADDESTRAMENTO DEL MODELLO =====

# Addestra il modello usando i dati di training e validation

print("Addestramento del modello...")

model.run_train(

    train,

    validation,

    epochs=5,                  # Numero di epoche (configurabile)

    batch_size=32,             # Dimensione del batch (configurabile)

    best_save_path='best_model.pth'  # Salva il miglior modello durante l'addestramento

)
 
# ===== 4. VALUTAZIONE DEL MODELLO =====

# Valuta il modello usando i dati di test

print("Valutazione del modello...")

results = model.run_eval(test)

print("Risultati sul set di test:")

print(results)
 
# ===== 5. SALVATAGGIO DEL MODELLO =====

# Salva lo stato del modello addestrato per usi futuri

print("Salvataggio del modello...")

model.save_state('final_model.pth')

print("Modello salvato in 'final_model.pth'.")
 
# Usa il modello addestrato per fare previsioni

print("Esecuzione delle previsioni...")

predictions = model.run_prediction(unlabeled)
 
# Salva le previsioni in un file CSV

predictions.to_csv('/home/trabbo/Documents/GitHub/idd-HW5/csv_files/deepmatch_predictions_phonetic.csv', index=False)

print("Previsioni salvate in 'predictions.csv'.")

 