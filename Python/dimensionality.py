import pandas as pd
import umap
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import seaborn as sns
import MLTraining
import plotly.express as px
import numpy as np

def lda():
    df = pd.read_csv("Archive/test Data set/TrainingSetWdeltas_L.csv")
    df = df[df['activeCube'] != -1]
    X = df.drop("GoalGesture", axis=1)
    y = df["GoalGesture"]
    lda = LinearDiscriminantAnalysis(n_components=2)
    X_lda = lda.fit_transform(X, y)
    plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='rainbow', edgecolor='k', alpha=0.7)
    plt.xlabel("LDA Component 1")
    plt.ylabel("LDA Component 2")
    plt.title("LDA projection of the dataset")
    plt.show()


def PCAVisual(X_pca, y):
    pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    pca_df["GoalGesture"] = y
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="GoalGesture", palette="Set2")
    plt.title("PCA: Projection of Gestures")
    plt.show()


#MLTraining.trainPCA(data, RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=10, min_samples_split=2))
def PCAcalc():
    data = pd.read_csv("Archive/test Data set/TrainingSetWdeltas_L.csv")
    data = data[data['activeCube'] != -1]
    pca = PCA(n_components=0.95)
    X = data.drop(columns=["GoalGesture"])
    y = data["GoalGesture"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_pca = pca.fit_transform(X_scaled)

    lda = LinearDiscriminantAnalysis(n_components=None)
    X_lda = lda.fit_transform(X_pca, y)

    unique_classes = np.unique(y)
    colors = ['red', 'green', 'blue', 'orange']  # Add more if you have more classes

    if X_lda.shape[1] < 3:
        print(f"Only {X_lda.shape[1]} LDA component(s) available. Showing 2D plot instead.")
        for i, cls in enumerate(unique_classes):
            idx = y == cls
            plt.scatter(X_lda[idx, 0], X_lda[idx, 1], label=f"Class {cls}",
                        color=colors[i], edgecolor='k', alpha=0.7)
        plt.xlabel("LDA Component 1")
        plt.ylabel("LDA Component 2")
        plt.title("2D LDA projection (discrete classes)")
    else:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        for i, cls in enumerate(unique_classes):
            idx = y == cls
            ax.scatter(X_lda[idx, 0], X_lda[idx, 1], X_lda[idx, 2],
                       label=f"Class {cls}", color=colors[i], s=60, edgecolors='k', alpha=0.8)
        ax.set_xlabel("LDA Component 1")
        ax.set_ylabel("LDA Component 2")
        ax.set_zlabel("LDA Component 3")
        ax.set_title("3D LDA projection (discrete classes)")
        ax.legend(title="Class")

    plt.tight_layout()
    plt.show()
    df_pca = pd.DataFrame(X_pca)
    df_pca["GoalGesture"] = y
    return df_pca


data = PCAcalc()


def tsne_Visualization():
    data = pd.read_csv("Archive/test Data set/TrainingSetWdeltas_L.csv")
    data = data[data['activeCube'] != -1]
    X = data.drop(columns=["GoalGesture"])
    y = data["GoalGesture"]

    X_scaled = StandardScaler().fit_transform(X)
    tsne = TSNE(n_components=3, random_state=3, perplexity=10)
    X_tsne = tsne.fit_transform(X_scaled)

    tsne_df = pd.DataFrame(X_tsne, columns=["Dim1", "Dim2", "Dim3"])
    tsne_df["label"] = y

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Choose a color palette that has enough contrast
    palette = sns.color_palette("Set2", n_colors=tsne_df["label"].nunique())

    for label in tsne_df["label"].unique():
        subset = tsne_df[tsne_df["label"] == label]
        ax.scatter(subset["Dim1"], subset["Dim2"], subset["Dim3"],
                   label=label, s=40, alpha=0.8)

    ax.set_title("t-SNE 3D: Gesture Clusters")
    ax.set_xlabel("Dim1")
    ax.set_ylabel("Dim2")
    ax.set_zlabel("Dim3")
    ax.legend()
    plt.tight_layout()
    plt.show()

def umapVisualization():
    data = pd.read_csv("Archive/test Data set/TrainingSetWdeltas_L.csv")
    data = data[data['activeCube'] != -1]
    X = data.drop(columns=["GoalGesture"])
    y = data["GoalGesture"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    reducer = umap.UMAP(n_components=3, random_state=42, metric='correlation', min_dist=0.05, n_neighbors=7)
    X_umap = reducer.fit_transform(X_scaled)

    umap_df = pd.DataFrame(X_umap, columns=["Dim1", "Dim2", "Dim3"])  # ✅
    umap_df["label"] = y.astype(str)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(X_umap[:, 0], X_umap[:, 1], X_umap[:, 2], c=y, cmap="Set2", s=50)
    legend = ax.legend(*scatter.legend_elements(), title="Label")
    ax.add_artist(legend)
    plt.title("UMAP: 3D Gesture Clusters")
    plt.show()

    fig = px.scatter_3d(
        umap_df,
        x="Dim1", y="Dim2", z="Dim3",
        color="label",
        title="UMAP: 3D Gesture Clusters (Interactive)",
        opacity=0.8
    )

    fig.show()

    fig.write_html("umap3DplotL.html")



