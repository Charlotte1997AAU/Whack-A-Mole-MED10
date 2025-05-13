import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd

# Load and clean data
data = pd.read_csv("Archive/test Data set/TrainingSet_L.csv")
data = data.dropna()
data = data.select_dtypes(include=[np.number])  # Use only numeric columns

def check_umap_assumptions(data, n_neighbors=15, plot=True):
    results = {}

    # Assumption 1: Uniform distribution on a Riemannian manifold
    nbrs = NearestNeighbors(n_neighbors=n_neighbors).fit(data)
    distances, _ = nbrs.kneighbors(data)
    avg_densities = np.mean(distances[:, 1:], axis=1)
    std_density = np.std(avg_densities)
    mean_density = np.mean(avg_densities)
    density_ratio = std_density / mean_density
    results["Uniform Distribution"] = density_ratio < 0.5  # heuristic threshold
    print(f"Uniformity (std/mean of local densities): {density_ratio:.2f} => {'✓' if results['Uniform Distribution'] else '✗'}")

    # Assumption 2: Locally constant Riemannian metric
    local_variance_ratios = []
    for i in range(data.shape[0]):
        _, indices = nbrs.kneighbors(data.iloc[[i]])  # Double brackets fix the warning
        local_patch = data.iloc[indices[0]]
        pca = PCA(n_components=min(3, data.shape[1]))
        pca.fit(local_patch)
        explained = np.sum(pca.explained_variance_ratio_)
        local_variance_ratios.append(explained)
    var_ratio_std = np.std(local_variance_ratios)
    results["Locally Constant Metric"] = var_ratio_std < 0.1
    print(f"Local PCA variance consistency (std): {var_ratio_std:.2f} => {'✓' if results['Locally Constant Metric'] else '✗'}")

    # Assumption 3: Locally connected manifold
    connectivity_scores = []
    for i in range(data.shape[0]):
        _, indices = nbrs.kneighbors(data.iloc[[i]])
        local_patch = data.iloc[indices[0]]
        local_nbrs = NearestNeighbors(n_neighbors=5).fit(local_patch)
        graph = local_nbrs.kneighbors_graph(local_patch).toarray()
        connected = np.sum(graph) / (graph.shape[0] * (graph.shape[0] - 1))
        connectivity_scores.append(connected)
    avg_connectivity = np.mean(connectivity_scores)
    results["Locally Connected"] = avg_connectivity > 0.5
    print(f"Local connectivity score: {avg_connectivity:.2f} => {'✓' if results['Locally Connected'] else '✗'}")

    # Optional plot
    if plot:
        plt.hist(avg_densities, bins=30, alpha=0.7)
        plt.title("Histogram of Local Average Distances (Density Proxy)")
        plt.xlabel("Average kNN Distance")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.show()

    return results

# Run the check
check_umap_assumptions(data, n_neighbors=15, plot=True)
