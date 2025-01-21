import os
import importlib
import pandas as pd

# Lista delle colonne dello schema mediato
mediated_schema_columns = [
    "Company ID", "Company Name", "Rank/Merit", "2010 Rank", "Annual Revenue", "Net Income", "Annual Results Year End", 
    "Total Assets", "Total Liabilities", "Net Equity", "Headquarters Address", "Headquarters City", 
    "Headquarters Country", "Headquarters Sub Region", "Headquarters Continent", "Headquarters Region", "Industry",
    "Business Sector(s)", "SIC Code", "EMTAK Code", "NACE Code", "Legal Form", "Foundation Date", "Join Date",
    "Company Number", "HHID", "CEO", "Founders", "Investors","Official Website", "Market Valuation",
    "Share Price", "Change 1 Day", "Change 1 Year", "Total Raised", 
    "Company National ID", "Number of Employees", "Company Status", "Social Media - Facebook","Social Media - Twitter", 
    "Social Media - Instagram", "Social Media - Pinterest", "Ownership", "Main Market", "Notes", "Source", "Trade Name", "Postalcode"
]

# Percorso alla cartella File_Mappers
folder_path = "File_Mappers"

# Lista per raccogliere i DataFrame
dataframes = []

# Itera su tutti i file nella cartella
for filename in os.listdir(folder_path):
    if filename.endswith("_Mapper.py"):  # Filtra solo i file _Mapper.py
        module_name = f"{folder_path}.{filename[:-3]}"  # Rimuovi ".py" dal nome del file
        
        try:
            # Importa dinamicamente il modulo
            module = importlib.import_module(module_name)
            
            # Verifica che il modulo abbia il metodo mapper
            if hasattr(module, "mapper"):
                # Esegui il metodo mapper
                mapper_function = getattr(module, "mapper")
                df = mapper_function(mediated_schema_columns)
                
                # Aggiungi il DataFrame alla lista
                if isinstance(df, pd.DataFrame):  # Assicurati che il risultato sia un DataFrame
                    dataframes.append(df)
                else:
                    print(f"Il metodo mapper in {filename} non ha restituito un DataFrame.")
        
        except Exception as e:
            print(f"Errore nell'importazione o esecuzione del mapper in {filename}: {e}")

# Concatenazione di tutti i DataFrame
if dataframes:
    final_dataframe = pd.concat(dataframes, ignore_index=True)
else:
    final_dataframe = pd.DataFrame(columns=mediated_schema_columns)

# Visualizzazione del risultato
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.precision', 3):
    print(final_dataframe.info())

final_dataframe.to_csv('mediated_schema.csv')