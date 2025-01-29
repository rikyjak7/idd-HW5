import pandas as pd

csv_path = "/home/vboxuser/Documents/GitHub/idd-HW5/csv_files/model_testing/unified_metaphone.csv"
df = pd.read_csv(csv_path)

# Aggiunge un identificatore univoco
df.insert(0, 'id', range(1, 1 + len(df)))

# Salva il nuovo file con ID
new_csv_path = "/home/vboxuser/Documents/GitHub/idd-HW5/csv_files/model_testing/unified_metaphone_with_id.csv"
df.to_csv(new_csv_path, index=False)

print(f"Nuovo file salvato in: {new_csv_path}")