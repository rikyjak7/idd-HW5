import pandas as pd
import numpy as np
import fase_1.DataframeExtractor as DataframeExtractor 


# Funzione per mappare gli headquarters
def map_headquarters(value):
    if pd.isna(value):
        return np.nan, np.nan, np.nan
    parts = [x.strip() for x in value.split(",")]
    if len(parts) == 2:  # City, Country
        return parts[0], np.nan, parts[1]
    elif len(parts) == 3:  # City, Region, Country
        return parts[0], parts[1], parts[2]
    else:  # Caso generico, mappare tutto su una sola colonna
        return np.nan, np.nan, np.nan

def mapper(mediated_schema_columns): 
    data = DataframeExtractor.extract_dataframe_by_extension("Files/campaignindia.csv")
    # Creazione del DataFrame schema mediato
    mediated_df = pd.DataFrame(columns=mediated_schema_columns)

    mediated_df["Rank/Merit"] = data["RANK"]
    mediated_df["Company Name"] = data["BRAND NAME"]
    mediated_df["Business Sector(s)"] = data["CATEGORY"]
    mediated_df["Main Market"] = data["MAIN MARKET"]
    mediated_df["2010 Rank"] = data["2010 RANK"]

    # Assegnare NaN per le altre colonne non mappabili
    for col in mediated_schema_columns:
        if col not in mediated_df.columns:
            mediated_df[col] = np.nan

    return mediated_df
