import numpy as np
from .ProxiFlat import ProxiFlat
from pprint import pprint


class Sample:
    def __init__(self, features: np.ndarray, text: str):
        self.features = features
        self.text = text


class ProxiCluster:
    def __init__(
        self, k: int, num_threads: int, num_clusters: int, objective_function: str = "l2"
    ) -> None:
        if k < 0:
            raise ValueError("K cannot be lesser than 0.")
        if num_threads < 0:
            raise ValueError("num_threads cannot be lesser than 0.")
        
        if num_clusters is not None:
            if num_clusters < 0:
                raise ValueError("num_clusters cannot be lesser than 0.")
        
        # Number of clusters. Set to sqrt of number of samples if set to None
        self.num_clusters = num_clusters

        # List of all cluster indices
        self.clusters = []

        # An index of all cluster heads
        self.cluster_head_proxiss = None

        # Name of distance function
        self.objective_function = objective_function

    def index_data(self, embeddings: np.ndarray, documents: np.ndarray) -> None:
        
        if not isinstance(embeddings, np.ndarray):
            raise TypeError("Embeddings must be a NumPy array.")
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)
        if not (embeddings.ndim == 2 or (embeddings.ndim == 1 and embeddings.shape[0] == 0)):
            raise ValueError(
                "Embeddings NumPy array must be 2D (e.g., (N, D)) or an empty 1D array."
            )

        if not isinstance(documents, np.ndarray):
            raise TypeError("Documents must be a NumPy array.")
        if documents.dtype != object:
            documents = documents.astype(object)
        if documents.ndim != 1:
            if documents.size > 0:
                raise ValueError("Documents NumPy array must be 1D.")
            final_documents_list = []
        else:
            final_documents_list = documents.tolist()

        ## Clustering of data

        # Select random cluster heads
        self.cluster_heads_indices = np.random.randint(embeddings.shape[0], size=int(self.num_clusters))
        cluster_heads = embeddings[self.cluster_heads_indices]
        
        # Calculate Distances
        if self.objective_function == "l2":
            embeddings_sq = np.sum(np.square(embeddings), axis=1).reshape(-1, 1)
            heads_sq = np.sum(np.square(cluster_heads), axis=1).reshape(-1, 1)
            dot = embeddings @ cluster_heads.T
            
            distances = np.sqrt(embeddings_sq + heads_sq.T - 2 * dot)
            
        elif self.objective_function == "l1":
            distances = np.sum(np.abs(embeddings[:, np.newaxis, :] - cluster_heads[np.newaxis, :, :]), axis=2)
        
        elif self.objective_function == "cos":
            embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            heads_norm = cluster_heads / np.linalg.norm(cluster_heads, axis=1, keepdims=True)
            similarity = np.dot(embeddings_norm, heads_norm.T)
            distances = 1 - similarity
            
        else:
            raise ValueError(f"Invalid distance function: {self.objective_function}.")
        
        cluster_assignments = np.argmin(distances, axis=1)
        
        cluster_map = {head_idx: [] for head_idx in self.cluster_heads_indices}
        
        for idx, assigned_cluster in enumerate(cluster_assignments):
            global_index = self.cluster_heads_indices[assigned_cluster]
            cluster_map[global_index].append(idx)
            
        # pprint(cluster_map)