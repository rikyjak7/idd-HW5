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
    data = DataframeExtractor.extract_dataframe_by_extension("Files/valueToday_dataset.jsonl")
    mediated_df = pd.DataFrame(columns=mediated_schema_columns)    

    mediated_df["Company ID"] = data["id"]
    mediated_df["Company Name"] = data["name"]
    mediated_df["Rank/Merit"] = data["world_rank"] 
    mediated_df["Annual Revenue"] = data["annual_revenue_in_usd"]
    mediated_df["Net Income"] = data["annual_net_income_in_usd"]
    mediated_df["Annual Results Year End"] = data["annual_results_for_year_ending"]
    mediated_df["Total Assets"] = data["total_assets_in_usd"]
    mediated_df["Total Liabilities"] = data["total_liabilities_in_usd"]
    mediated_df["Net Equity"] = data["total_equity_in_usd"]
    mediated_df["Business Sector(s)"] = data["company_business"] 
    mediated_df["Number of Employees"] = data["number_of_employees"]
    mediated_df["CEO"] = data["ceo"]
    mediated_df["Founders"] = data["founders"]
    mediated_df["Official Website"] = data["company_website"]
    mediated_df["Headquarters Region"] = data["headquarters_region_city"]
    mediated_df["Headquarters Country"] = data["headquarters_country"]
    mediated_df["Headquarters Sub Region"] = data["headquarters_sub_region"]
    mediated_df["Headquarters Continent"] = data["headquarters_continent"]



    # Assegnare NaN per le altre colonne non mappabili
    for col in mediated_schema_columns:
        if col not in mediated_df.columns:
            mediated_df[col] = np.nan

    return mediated_df
