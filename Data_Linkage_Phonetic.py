import pandas as pd
from metaphone import doublemetaphone
from collections import defaultdict
from rapidfuzz import fuzz

# Carica il file CSV
try:
    dataframe = pd.read_csv("mediated_schema.csv", encoding='latin1', low_memory=False)
except UnicodeDecodeError as e:
    print(f"Errore nella lettura del file CSV: {e}")
    dataframe = pd.DataFrame()  # Inizializza un DataFrame vuoto in caso di errore

# Converte tutte le colonne in stringhe
dataframe = dataframe.astype(str)

# Pulizia delle stringhe: rimozione degli spazi extra e conversione in minuscolo
if 'Company Name' in dataframe.columns:
    dataframe['Company Name'] = dataframe['Company Name'].str.strip().str.lower()
else:
    print("La colonna 'Company Name' non esiste nel dataset.")

# Genera codici Double Metaphone per i nomi delle compagnie
if 'Company Name' in dataframe.columns:
    # Applica la funzione doublemetaphone a ciascun nome
    dataframe['Primary_Metaphone'], dataframe['Secondary_Metaphone'] = zip(
        *dataframe['Company Name'].apply(doublemetaphone)
    )
else:
    print("La colonna 'Company Name' non esiste nel dataset.")

# Combiniamo Primary e Secondary Metaphone per formare un unico codice (se esistono entrambi)
dataframe['CompanyName_Metaphone'] = dataframe['Primary_Metaphone'].combine_first(dataframe['Secondary_Metaphone'])

# Raggruppiamo i nomi delle compagnie per codice Metaphone con controllo della similarità
if 'CompanyName_Metaphone' in dataframe.columns:
    # Raggruppa i nomi per codice Metaphone
    metaphone_groups = defaultdict(list)
    for i, row in dataframe.iterrows():
        metaphone_groups[row['CompanyName_Metaphone']].append(row['Company Name'])

    # Confronta i codici Metaphone tra loro
    threshold = 90  # Soglia di similarità tra codici fonetici
    merged_groups = defaultdict(list)  # Gruppi finali uniti

    metaphone_list = list(metaphone_groups.keys())  # Lista dei codici Metaphone
    visited = set()  # Per evitare confronti duplicati

    for i, metaphone1 in enumerate(metaphone_list):
        if metaphone1 in visited:
            continue
        temp_group = metaphone_groups[metaphone1]  # Inizia con i nomi relativi al primo codice
        visited.add(metaphone1)

        for j, metaphone2 in enumerate(metaphone_list):
            if i != j and metaphone2 not in visited:
                # Confronta i codici fonetici
                similarity = fuzz.ratio(metaphone1, metaphone2)
                if similarity >= threshold:
                    # Unisci i gruppi relativi ai due codici
                    temp_group.extend(metaphone_groups[metaphone2])
                    visited.add(metaphone2)

        # Rimuovi duplicati nei nomi e aggiungi al gruppo finale
        temp_group = list(set(temp_group))
        merged_groups[metaphone1].extend(temp_group)

    # Prepara i risultati finali
    final_results = []
    for key, company_names in merged_groups.items():
        final_results.append((key, company_names))

    # Crea un DataFrame con i risultati
    similar_matches = pd.DataFrame(final_results, columns=['Merged Metaphone Code', 'Company Names'])
    print("Raggruppamenti fonetici con merge basato su similarità:")
    print(similar_matches)

    # Salva i risultati in un file CSV
    output_filename = "merged_similar_matches_metaphone.csv"
    similar_matches.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"Risultati salvati nel file: {output_filename}")
else:
    print("La colonna 'CompanyName_Metaphone' non è stata generata correttamente.")


'''
import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
from streamlit import cache_data,cache_resource 

cache_data.clear()
cache_resource.clear()

# Carica il file CSV
try:
    dataframe = pd.read_csv("mediated_schema.csv", encoding='latin1', low_memory=False)
except UnicodeDecodeError as e:
    print(f"Errore nella lettura del file CSV: {e}")
    dataframe = pd.DataFrame()  # Inizializza un DataFrame vuoto in caso di errore

# Converte tutte le colonne in stringhe
dataframe = dataframe.astype(str)

# Pulizia dei dati sulle colonne stringa
for column in dataframe.select_dtypes(include=["object"]):
    dataframe[column] = recordlinkage.preprocessing.clean(dataframe[column])

# Aggiunge la colonna fonetica per il Company Name
if 'Company Name' in dataframe.columns:
    dataframe['CompanyName_Soundex'] = recordlinkage.preprocessing.phonetic(dataframe['Company Name'], method='soundex')
else:
    print("La colonna 'Company Name' non esiste nel dataset.")

# Effettua il blocking sulla colonna CompanyName_Soundex
if 'CompanyName_Soundex' in dataframe.columns:
    # Crea l'indice utilizzando il valore fonetico di Company Name
    block_indexer= recordlinkage.Index()
    block_indexer.block(left_on="CompanyName_Soundex")
    candidate_links= block_indexer.index(dataframe)
    print("Blocking completato con successo.")
    print(f"Numero di coppie create: {len(candidate_links)}")

    # Ora facciamo la comparazione sul valore esatto della company_name
    comparator= recordlinkage.Compare()
    comparator.exact('Company Name', 'Company Name')
    features = comparator.compute(candidate_links, dataframe)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
        print(features)
else:
    print("La colonna 'CompanyName_Soundex' non è stata generata correttamente.")
'''



# Mostra il DataFrame risultante
#with pd.option_context('display.max_rows', 50, 'display.max_columns', None, 'display.precision', 3):
#    print(dataframe)