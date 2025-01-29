import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.lines as mlines

# Carica il dataset
file_path = "/home/vboxuser/Documents/GitHub/idd-HW5/csv_files/......."  # Modifica con il percorso corretto
df = pd.read_csv(file_path)

print(df["name"].dtype)  # Controlla il tipo di dati
print(df["name"].head())  # Vedi i primi valori
print(df[df["name"].isna()])  # Trova eventuali valori NaN

# Divide i nomi e filtra i cluster con almeno 2 elementi
df["name"] = df["name"].astype(str).apply(lambda x: x.split(",") if isinstance(x, str) else [])
df = df[df["name"].apply(len) > 1]

# Conta il numero di elementi per cluster
df["size"] = df["name"].apply(len)

# Ordina i cluster per grandezza e seleziona quelli dalla posizione 51 alla 80
top_clusters = df.groupby("cluster").sum().nlargest(80, "size").reset_index()
df_selected = df[df["cluster"].isin(top_clusters["cluster"].iloc[50:80])]

# Filtra i cluster che contengono "\n" nei nomi
df_selected = df_selected[~df_selected["name"].apply(lambda x: any('\n' in name for name in x))]

# Creiamo una lista di parole per ogni cluster
words = list(set([name for names in df_selected["name"] for name in names]))

# Carica il modello pre-addestrato
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# Otteniamo i vettori embedding per ogni parola
word_vectors = {word: model.encode(word) for word in words}

# Riduciamo la dimensionalità con PCA prima di t-SNE
pca = PCA(n_components=20)  # Da 384D a 20D
vectors = np.array([word_vectors[w] for w in words])
vectors_pca = pca.fit_transform(vectors)

# Applichiamo t-SNE per ridurre a 2D
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
vectors_2d = tsne.fit_transform(vectors_pca)

# Creiamo un DataFrame per la visualizzazione
df_plot = pd.DataFrame(vectors_2d, columns=["x", "y"])
df_plot["word"] = words

# Assegniamo un cluster a ogni parola
def find_cluster(word):
    for cluster_id in df_selected["cluster"].unique():
        for names in df_selected[df_selected["cluster"] == cluster_id]["name"]:
            if word in names:
                return cluster_id
    return None

df_plot["cluster"] = df_plot["word"].apply(find_cluster)
df_plot.dropna(inplace=True)

# Aggiungi un solo nome per cluster (primo nome di ogni cluster)
cluster_names = {cluster_id: next(iter(df_selected[df_selected["cluster"] == cluster_id]["name"]))[0]
                 for cluster_id in df_selected["cluster"].unique()}

# Visualizzazione con Seaborn
plt.figure(figsize=(16, 10))  # Aumentato il valore per la larghezza
sns.scatterplot(data=df_plot, x="x", y="y", hue="cluster", palette="tab10", legend=False, alpha=0.7)

# Crea la legenda personalizzata
handles = []
for cluster_id, name in cluster_names.items():
    # Crea un marker per ogni cluster
    handle = mlines.Line2D([], [], marker='o', color='w', markerfacecolor=sns.color_palette("tab10")[cluster_id % 10],
                           markersize=10, label=name)
    handles.append(handle)

# Aggiungi la legenda alla figura con più spazio
plt.legend(handles=handles, title="Cluster", loc="center left", bbox_to_anchor=(1.05, 0.5))

# Non aggiungere etichette per i nodi nel grafico
plt.title("Clusterizzazione dei Word Embeddings con t-SNE", fontsize=14)
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.show()