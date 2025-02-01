import pandas as pd
import recordlinkage
import recordlinkage.preprocessing
from streamlit.runtime.caching import cache_data,cache_resource 



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

    #ora facciamo la comparazione sul valore esatto della company_name
    comparator= recordlinkage.Compare()
    comparator.exact('Company Name', 'Company Name')
    features = comparator.compute(candidate_links, dataframe)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
        print(features)
else:
    print("La colonna 'CompanyName_Soundex' non è stata generata correttamente.")



# Mostra il DataFrame risultante
#with pd.option_context('display.max_rows', 50, 'display.max_columns', None, 'display.precision', 3):
#    print(dataframe)