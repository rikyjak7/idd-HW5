import os
import pandas as pd
import matplotlib.pyplot as plt

def leggi_file(file_path):
    """Legge un file in base alla sua estensione e restituisce un DataFrame."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.csv':
            return pd.read_csv(file_path, encoding='utf-8')  # Tentativo con utf-8
        elif file_extension == '.json':
            return pd.read_json(file_path)
        elif file_extension == '.jsonl':
            return pd.read_json(file_path, lines=True)
        elif file_extension in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Tipo di file non supportato: {file_extension}")
    except UnicodeDecodeError as e:
        # Se c'è un errore di decodifica, proviamo una codifica alternativa
        print(f"Errore di decodifica per il file {file_path}. Tentiamo con 'ISO-8859-1'.")
        if file_extension == '.csv':
            return pd.read_csv(file_path, encoding='ISO-8859-1')  # Tentativo con ISO-8859-1
        else:
            raise e
    except Exception as e:
        print(f"Errore nel leggere il file {file_path}: {e}")
        raise e


def calcola_utilita_file(directory):
    """Calcola la percentuale di utilità dei file nella directory."""
    risultati = []

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Consideriamo solo i file supportati (csv, json, jsonl, xls)
        if file_name.endswith(('.csv', '.json', '.jsonl', '.xls', '.xlsx')):
            try:
                # Leggi il file in un DataFrame
                df = leggi_file(file_path)
                
                # Calcola il numero di colonne nel DataFrame
                num_colonne = len(df.columns)
                risultati.append((file_name, num_colonne))
            except Exception as e:
                print(f"Errore nel leggere il file {file_name}: {e}")

    return risultati

def salva_utilita_excel(risultati, file_excel):
    """Salva i risultati in un file Excel con grafico."""
    df_risultati = pd.DataFrame(risultati, columns=["File", "Numero di Colonne"])

    # Troviamo il numero massimo di colonne
    max_colonne = df_risultati["Numero di Colonne"].max()

    # Calcoliamo la percentuale di utilità
    df_risultati["Percentuale di Utilità"] = (df_risultati["Numero di Colonne"] / max_colonne) * 100

    # Salviamo i dati in un file Excel
    with pd.ExcelWriter(file_excel, engine='xlsxwriter') as writer:
        df_risultati.to_excel(writer, sheet_name='Utilità', index=False)

        # Aggiungiamo un grafico a barre delle percentuali di utilità
        workbook  = writer.book
        worksheet = writer.sheets['Utilità']
        
        # Creiamo il grafico
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Percentuale di Utilità',
            'categories': f'=Utilità!$A$2:$A${len(df_risultati) + 1}',
            'values': f'=Utilità!$C$2:$C${len(df_risultati) + 1}',
        })
        
        # Aggiungiamo il grafico alla cella D2
        worksheet.insert_chart('D2', chart)

# Directory dove sono contenuti i file
directory = "C:/Users/hp/idd-HW5/Files"  # Sostituisci con il percorso corretto

# Calcoliamo la percentuale di utilità dei file
risultati = calcola_utilita_file(directory)

# Nome del file Excel di output
file_excel = "utilita_sorgenti.xlsx"

# Salviamo i risultati in un file Excel con il grafico
salva_utilita_excel(risultati, file_excel)

print(f"I risultati sono stati salvati in {file_excel}")



'''
# Schema mediato
mediated_schema_columns = [
    "Company ID", "Company Name", "Rank/Merit", "2010 Rank", "Annual Revenue", "Net Income", "Annual Results Year End", 
    "Total Assets", "Total Liabilities", "Net Equity", "Headquarters Address", "Headquarters City", 
    "Headquarters Country", "Headquarters Sub Region", "Headquarters Continent", "Headquarters Region", "Industry",
    "Business Sector(s)", "SIC Code", "EMTAK Code", "NACE Code", "Legal Form", "Foundation Date", "Join Date",
    "Company Number", "HHID", "CEO", "Founders", "Investors","Official Website", "Market Valuation",
    "Share Price", "Change 1 Day", "Change 1 Year", "Total Raised", "Company National ID", "Number of Employees", 
    "Company Status", "Social Media - Facebook","Social Media - Twitter", "Social Media - Instagram", "Social Media - Pinterest", 
    "Ownership", "Main Market", "Notes", "Source", "Trade Name", "Postalcode"
]

attribute_mapping = {
    "Company Name": ["Company Name", "name", "Name", "BRAND NAME", "NAME", "company", "Company"],
    "Foundation Date": ["Foundation Date", "Foundation Year", "founded", "est_of_ownership", "company_creation_date", "Registration Date"],
    "Rank/Merit": ["Rank/Merit", "RANK", "rank"],
    "Business Sector(s)": ["Business Sector(s)", "CATEGORY", "categories", "Sector", "nature_of_business", "Area of Activity"],
    "Main Market": ["Main Market", "MAIN MARKET"],
    "2010 Rank": ["2010 Rank", "2010 RANK"],
    "Market Valuation": ["Market Valuation", "market_cap", "valuation", "Market Value"],
    "Share Price": ["Share Price", "share_price"],
    "Change 1 Day": ["Change 1 Day", "change_1_day"],
    "Change 1 Year": ["Change 1 Year", "change_1_year"],
    "Headquarters Country": ["Headquarters Country", "country", "Country", "headquarters"],
    "Headquarters City": ["Headquarters City", "city", "Headquarters"],
    "Headquarters Address": ["Headquarters Address", "address", "registered_office_address", "Address Name"],
    "Social Media - Facebook": ["Social Media - Facebook", "Facebook"],
    "Social Media - Twitter": ["Social Media - Twitter", "Twitter"],
    "Social Media - Instagram": ["Social Media - Instagram", "Instagram"],
    "Social Media - Pinterest": ["Social Media - Pinterest", "Pinterest"],
    "Join Date": ["Join Date", "dateJoined"],
    "Industry": ["Industry", "industry"],
    "Investors": ["Investors", "investors"],
    "Founders": ["Founders"],
    "Company Status": ["Company Status", "stage", "company_status", "Status"],
    "Total Raised": ["Total Raised", "totalRaised"],
    "Official Website": ["Official Website", "website", "link", "company_website", "URL"],
    "Number of Employees": ["Number of Employees", "size", "employees", "number_of_employees"],
    "CEO": ["CEO", "ceo"],
    "Annual Revenue": ["Annual Revenue", "revenue", "Sales", "Revenue", "annual_revenue_in_usd"],
    "Company Number": ["Company Number", "id", "company_number"],
    "Company National ID": ["Company National ID", "nation"],
    "Company ID": ["Company ID", "ID azienda", "ID", "id"],
    "SIC Code": ["SIC Code", "sic_code"],
    "Legal Form": ["Legal Form", "type", "company_type"],
    "Net Income": ["Net Income", "Profit", "annual_net_income_in_usd"],
    "Total Assets": ["Total Assets", "Assets", "total_assets_in_usd"],
    "Total Liabilities": ["Total Liabilities", "total_liabilities_in_usd"],
    "Net Equity": ["Net Equity", "total_equity_in_usd"],
    "Headquarters Region": ["Headquarters Region", "headquarters_region_city", "State"],
    "Headquarters Sub Region": ["Headquarters Sub Region", "headquarters_sub_region"],
    "Headquarters Continent": ["Headquarters Continent", "headquarters_continent"],
    "Phone Number": ["Phone Number", "telephone"],
    "Annual Results Year End": ["annual_results_for_year_ending"],
    "HHID": ["HHID","hhid"],
    "Ownership": ["Ownership"],
    "Notes": ["Notes"],
    "Source": ["Source"],
    "Trade Name": ["Trade Name"],
    "Postalcode": ["Postalcode"],
    "EMTAK Code": ["EMTAK Code"],
    "NACE Code": ["NACE Code"]
}
'''
