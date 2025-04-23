import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import seaborn as sns
import MLTraining
import numpy as np


def lda():
    df = pd.read_csv("test Data set/TrainingSetWdeltas_L.csv")
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
    data = pd.read_csv("test Data set/TrainingSetWdeltas_L.csv")
    data = data[data['activeCube'] != -1]

    X = data.drop(columns=["GoalGesture"])
    y = data["GoalGesture"]

    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=0.95)
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