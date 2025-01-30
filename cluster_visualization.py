import pandas as pd
import ast  # Per convertire stringhe in liste di Python quando necessario

# File di input e output
input_file = 'C:/Users/hp/idd-HW5/csv_files/cleaned_clustered_embedding.csv'  # Nome del file di input
nodes_output = 'nodesE.csv'  # File dei nodi per Gephi
edges_output = 'edgesE.csv'  # File degli archi per Gephi

# Leggi il file CSV di input
df = pd.read_csv(input_file)

# ===== 1. Generazione dei nodi =====
# Ogni nome di compagnia diventa un nodo con il proprio cluster
nodes = []
for _, row in df.iterrows():
    cluster_id = row['cluster']
    company_names = str(row['name']).strip()  # Converti in stringa ed elimina spazi
    if company_names and company_names.lower() != 'nan':  # Controlla che non sia NaN
        company_names = company_names.split(', ')  # Divide i nomi separati da virgola
        for name in company_names:
            nodes.append((name.strip(), cluster_id))

# Crea un DataFrame per i nodi
nodes_df = pd.DataFrame(nodes, columns=['Id', 'Cluster']).drop_duplicates()
nodes_df.to_csv(nodes_output, index=False)
print(f"Nodi salvati in '{nodes_output}'.")

# ===== 2. Generazione degli archi =====
# Creiamo gli archi collegando i nomi dello stesso cluster
edges = []
for _, row in df.iterrows():
    company_names = str(row['name']).strip()
    if company_names and company_names.lower() != 'nan':
        company_names = company_names.split(', ')  # Divide i nomi separati da virgola
        company_names = [name.strip() for name in company_names]
        # Genera tutte le coppie di nomi appartenenti allo stesso cluster
        for i in range(len(company_names)):
            for j in range(i + 1, len(company_names)):
                edges.append((company_names[i], company_names[j]))

# Crea un DataFrame per gli archi
edges_df = pd.DataFrame(edges, columns=['Source', 'Target']).drop_duplicates()
edges_df.to_csv(edges_output, index=False)
print(f"Archi salvati in '{edges_output}'.")


'''
mport pandas as pd
import ast  # Per convertire le liste stringa in oggetti Python

# File di input e output
input_file = 'C:/Users/hp/idd-HW5/csv_files/cleaned_clustered_embedding.csv'  # Nome del file di input
nodes_output = 'nodesE.csv'  # File dei nodi per Gephi
edges_output = 'edgesE.csv'  # File degli archi per Gephi

# Leggi il file CSV di input
df = pd.read_csv(input_file)

# ===== 1. Generazione dei nodi =====
# Ogni nome di compagnia diventa un nodo con il proprio cluster
nodes = []
for _, row in df.iterrows():
    cluster_id = row['cluster']
    company_names = ast.literal_eval(row['name'])  # Converte la lista stringa in lista Python
    for name in company_names:
        nodes.append((name.strip(), cluster_id))

# Crea un DataFrame per i nodi
nodes_df = pd.DataFrame(nodes, columns=['Id', 'Cluster']).drop_duplicates()
nodes_df.to_csv(nodes_output, index=False)
print(f"Nodi salvati in '{nodes_output}'.")

# ===== 2. Generazione degli archi =====
# Creiamo gli archi collegando i nomi dello stesso cluster
edges = []
for _, row in df.iterrows():
    company_names = ast.literal_eval(row['name'])  # Converte la lista stringa in lista Python
    company_names = [name.strip() for name in company_names]
    # Genera tutte le coppie di nomi appartenenti allo stesso cluster
    for i in range(len(company_names)):
        for j in range(i + 1, len(company_names)):
            edges.append((company_names[i], company_names[j]))

# Crea un DataFrame per gli archi
edges_df = pd.DataFrame(edges, columns=['Source', 'Target']).drop_duplicates()
edges_df.to_csv(edges_output, index=False)
print(f"Archi salvati in '{edges_output}'.")
'''