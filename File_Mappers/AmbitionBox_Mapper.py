import pandas as pd
import numpy as np
import DataframeExtractor as DataframeExtractor 


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
    data = DataframeExtractor.extract_dataframe_by_extension("Files/AmbitionBox.csv")
    # Creazione del DataFrame schema mediato
    mediated_df = pd.DataFrame(columns=mediated_schema_columns)

    # Popolamento dello schema mediato
    mediated_df["Company Name"] = data["Name"]
    mediated_df["Industry"] = data["Industry"]
    mediated_df["Ownership"] = data["Ownership"]
    mediated_df["Foundation Date"] = data["Foundation Year"]

    # Popolare Headquarters
    headquarters_mapped = data["Headquarter"].apply(map_headquarters)
    mediated_df["Headquarters City"] = [x[0] for x in headquarters_mapped]
    mediated_df["Headquarters Region"] = [x[1] for x in headquarters_mapped]
    mediated_df["Headquarters Country"] = [x[2] for x in headquarters_mapped]

    # Assegnare NaN per le altre colonne non mappabili
    for col in mediated_schema_columns:
        if col not in mediated_df.columns:
            mediated_df[col] = np.nan

    return mediated_df