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
    data = DataframeExtractor.extract_dataframe_by_extension("Files/DDD-cbinsight.com.csv")
    mediated_df = pd.DataFrame(columns=mediated_schema_columns)    

    mediated_df["Company Name"] = data["name"]
    mediated_df["Market Valuation"] = data["valuation"]
    mediated_df["Join Date"] = data["dateJoined"]
    mediated_df["Headquarters Country"] = data["country"]
    mediated_df["Headquarters City"] = data["city"]
    mediated_df["Industry"] = data["industry"]
    mediated_df["Investors"] = data["investors"]
    mediated_df["Foundation Date"] = data["founded"]
    mediated_df["Company Status"] = data["stage"]
    mediated_df["Total Raised"] = data["totalRaised"]


    # Assegnare NaN per le altre colonne non mappabili
    for col in mediated_schema_columns:
        if col not in mediated_df.columns:
            mediated_df[col] = np.nan

    return mediated_df