import pandas as pd
import recordlinkage

# Carica i dati delle aziende
df = pd.read_csv("C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/mediated_schema.csv")
# Aggiungi un indice numerico temporaneo al DataFrame delle aziende

# Carica i due CSV
df1 = pd.read_csv('C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/df1.csv')  # Assicurati di avere il percorso corretto
df2 = pd.read_csv('C:/Users/crist/OneDrive/Documenti/GitHub/idd-HW5/df2.csv')

# Assicurati che le colonne siano corrette e non abbiano spazi indesiderati
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Crea il MultiIndex con le coppie da confrontare
# Ogni Cluster ID deve essere confrontato tra df1 e df2
pairs = pd.merge(df1[['Cluster ID']], df2[['Cluster ID']], on='Cluster ID', how='inner', suffixes=('_1', '_2'))

# Crea il MultiIndex con gli indici dei DataFrame
multi_index = pd.MultiIndex.from_frame(df1[['Cluster ID']].join(df2[['Cluster ID']], lsuffix='_df1', rsuffix='_df2'))
'''
print(multi_index.shape)
print(multi_index[1])
print(df1.head())
print(df2.head())
print(df1.index)
print(df2.index)
print(multi_index)
'''

print("artem")
print(multi_index)

# Controlla che gli indici di df1 e df2 siano validi per il multi_index
valid_indices_df1 = multi_index.get_level_values(0).isin(df1.index)
valid_indices_df2 = multi_index.get_level_values(1).isin(df2.index)



df1_selected = df1.loc[multi_index.get_level_values(0)]
df2_selected = df2.loc[multi_index.get_level_values(1)]

# Stampa il risultato
print(f"df1_selected shape: {df1_selected.shape}")
print(f"df2_selected shape: {df2_selected.shape}")
print("dovbyk")


# Crea l'oggetto Compare
comp = recordlinkage.Compare()

# Aggiungi le caratteristiche da confrontare. Ad esempio, usa 'jarowinkler' per confrontare i nomi delle aziende.
comp.string('Company_Name_1', 'Company_Name_2', method='jarowinkler', label='name_similarity')

# Esegui il confronto
features = comp.compute(multi_index, df1, df2)

# Salva i risultati in un file CSV
features.to_csv('pairwise_comparison_results.csv')

# Mostra i risultati
print(features.head())
