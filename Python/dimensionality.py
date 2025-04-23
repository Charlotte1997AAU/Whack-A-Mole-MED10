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
    plt.scatter(X_lda[:, 0], X_lda[:, 1], X_lda[:, 2], c=y, cmap='rainbow', edgecolor='k', alpha=0.7)
    plt.xlabel("LDA Component 1")
    plt.ylabel("LDA Component 2")
    plt.title("LDA projection of the dataset")
    plt.show()

    data = pd.DataFrame(X_pca)
    data["GoalGesture"] = y
    return data


def PCAVisual(X_pca, y):
    pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    pca_df["GoalGesture"] = y
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="GoalGesture", palette="Set2")
    plt.title("PCA: Projection of Gestures")
    plt.show()


data = PCAcalc()

#MLTraining.trainPCA(data, RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=10, min_samples_split=2))

