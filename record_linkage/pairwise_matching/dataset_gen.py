import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(input_csv, train_csv, validation_csv, test_csv, train_size=0.6, val_size=0.2, test_size=0.2, random_state=42):
    """
    Legge un file CSV contenente coppie di nomi di aziende con etichette,
    estrae il 60% per il training, 20% per la validazione e 20% per il test.
    
    :param input_csv: Percorso del file CSV di input
    :param train_csv: Percorso del file CSV di output per il training set
    :param validation_csv: Percorso del file CSV di output per il validation set
    :param test_csv: Percorso del file CSV di output per il test set
    :param train_size: Percentuale dei dati da usare per il training (default: 0.6)
    :param val_size: Percentuale dei dati da usare per la validazione (default: 0.2)
    :param test_size: Percentuale dei dati da usare per il test (default: 0.2)
    :param random_state: Seed per la riproducibilità (default: 42)
    """
    # Carica il dataset
    df = pd.read_csv(input_csv)
    
    # Verifica che il file contenga le colonne necessarie
    required_columns = {'left_name', 'right_name', 'label'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Il file CSV deve contenere le colonne {required_columns}, ma ha {df.columns.tolist()}")
    
    # Suddivide il dataset in training e temp (validation + test)
    train_data, temp_data = train_test_split(df, test_size=(val_size + test_size), random_state=random_state)
    
    # Suddivide temp_data in validation e test
    validation_data, test_data = train_test_split(temp_data, test_size=(test_size / (val_size + test_size)), random_state=random_state)
    
    # Salva i nuovi dataset
    train_data.to_csv(train_csv, index=False)
    validation_data.to_csv(validation_csv, index=False)
    test_data.to_csv(test_csv, index=False)
    
    print(f"Training set salvato in: {train_csv}")
    print(f"Validation set salvato in: {validation_csv}")
    print(f"Test set salvato in: {test_csv}")

# Esempio di utilizzo
split_dataset(
    input_csv='csv_files/model_testing/unified_embedding.csv',
    train_csv='csv_files/model_testing/train_pairs_embedding.csv',
    validation_csv='csv_files/model_testing/validation_pairs_embedding.csv',
    test_csv='csv_files/model_testing/test_pairs_embedding.csv'
)
