import pandas as pd
import json
import os
import csv

# 1. Caricamento dei dati da file Excel
def load_excel_files(filename):
    dataframe = pd.read_excel(filename)
    return dataframe

# 2. Caricamento dei dati da file JSON come DataFrame
def load_json_files(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        dataframe = pd.json_normalize(json_data)
        return dataframe
    except Exception as e:
        print(f"Errore nella lettura del file JSON {filename}: {e}")
        return None

# 3. Caricamento dei dati da file JSONL come DataFrame (line per line)
def load_jsonl_files(filename):
    try:
        data_list = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                data_list.append(json.loads(line.strip()))  # Carica ogni riga JSON separatamente
        dataframe = pd.json_normalize(data_list)
        return dataframe
    except Exception as e:
        print(f"Errore nella lettura del file JSONL {filename}: {e}")
        return None

# 4. Caricamento dei dati da file CSV
def load_csv_files(filename):
    try:
        dataframe = pd.read_csv(filename, encoding='latin1')
        return dataframe
    except UnicodeDecodeError as e:
        print(f"Errore nella lettura del file CSV {filename}: {e}")
        return None

# 5. Elaborazione dei file con diverse estensioni
def lists_by_extension(path):
    json_datas = []
    jsonl_datas = []
    csv_datas = []
    excel_datas = []
    
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if filename.endswith('.json'):
                json_dataframe = load_json_files(file_path)
                if json_dataframe is not None:
                    json_datas.append(json_dataframe)
            elif filename.endswith('.jsonl'):
                jsonl_dataframe = load_jsonl_files(file_path)
                if jsonl_dataframe is not None:
                    jsonl_datas.append(jsonl_dataframe)
            elif filename.endswith('.csv'):
                csv_dataframe = load_csv_files(file_path)
                if csv_dataframe is not None:
                    csv_datas.append(csv_dataframe)
            elif filename.endswith('.xls') or filename.endswith('.xlsx'):
                excel_dataframe = load_excel_files(file_path)
                excel_datas.append(excel_dataframe)
        except Exception as e:
            print(f"Errore durante il processamento del file {filename}: {e}")
    
    return json_datas, jsonl_datas, csv_datas, excel_datas

#elaborazione per singolo file
def extract_dataframe_by_extension(file_path):    
    try:
        if file_path.endswith('.json'):
            json_dataframe = load_json_files(file_path)
            if json_dataframe is not None:
                data = json_dataframe
        elif file_path.endswith('.jsonl'):
            jsonl_dataframe = load_jsonl_files(file_path)
            if jsonl_dataframe is not None:
                data = jsonl_dataframe
        elif file_path.endswith('.csv'):
            csv_dataframe = load_csv_files(file_path)
            if csv_dataframe is not None:
                data = csv_dataframe
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            excel_dataframe = load_excel_files(file_path)
            data = excel_dataframe
    except Exception as e:
        print(f"Errore durante il processamento del file {file_path}: {e}")
    
    return data

""" 
path = "Files/"  
json_files, jsonl_files, csv_files, excel_files = lists_by_extension(path)


print("JSON Files:")
for i, df in enumerate(json_files):
    print(f"File {i+1}:\n", df)

print("JSONL Files:")
for i, df in enumerate(jsonl_files):
    print(f"File {i+1}:\n", df) 

print("CSV Files:")
for i, df in enumerate(csv_files):
    print(f"File {i+1}:\n", df)

print("Excel Files:")
for i, df in enumerate(excel_files):
    print(f"File {i+1}:\n", df)  
"""



