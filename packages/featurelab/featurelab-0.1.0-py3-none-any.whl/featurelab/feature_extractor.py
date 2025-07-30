import pandas as pd
import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.random_projection import GaussianRandomProjection
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class FeatureExtractor:
    """
    Feature extraction and dimensionality reduction methods
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def analyze_features(self, target=None):
        """Analyze features and suggest extraction methods"""
        suggestions = []
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        # Check for high dimensionality
        if len(numeric_cols) > 20:
            suggestions.append("PCA for numeric features")
            suggestions.append("t-SNE for visualization (2-3 components)")
        
        # Check for text data
        if len(text_cols) > 0:
            suggestions.append("TF-IDF for text features")
            suggestions.append("CountVectorizer for text features")
        
        # Check for feature clusters
        if len(numeric_cols) > 5:
            suggestions.append("K-means clustering features")
        
        # Check for sparse data
        if (self.df == 0).mean().mean() > 0.8:  # More than 80% zeros
            suggestions.append("TruncatedSVD for sparse data")
        
        return suggestions
    
    def extract_features(self, method='auto', target=None, **kwargs):
        """
        Perform feature extraction
        
        Parameters:
        -----------
        method : str
            'auto' - follow recommendations
            'pca' - principal component analysis
            'tsne' - t-distributed stochastic neighbor embedding
            'svd' - singular value decomposition
            'kmeans' - cluster features
            'tfidf' - text vectorization
        target : str
            Target column name (if supervised)
        """
        if method == 'auto':
            suggestions = self.analyze_features(target)
            if "PCA" in suggestions[0]:
                return self.extract_features(method='pca', **kwargs)
            elif "TF-IDF" in suggestions[-1]:
                return self.extract_features(method='tfidf', **kwargs)
            else:
                return self.extract_features(method='pca', **kwargs)
        
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        text_cols = self.df.select_dtypes(include=['object']).columns
        
        if method == 'pca' and len(numeric_cols) > 0:
            n_components = kwargs.get('n_components', min(10, len(numeric_cols)))
            pca = PCA(n_components=n_components)
            transformed = pca.fit_transform(self.df[numeric_cols])
            
            # Plot explained variance
            self.visualizer.plot_pca_variance(pca)
            
            # Create column names
            cols = [f'PC_{i+1}' for i in range(n_components)]
            return pd.DataFrame(transformed, columns=cols)
        
        elif method == 'tsne' and len(numeric_cols) > 0:
            n_components = kwargs.get('n_components', 2)
            perplexity = kwargs.get('perplexity', 30)
            tsne = TSNE(n_components=n_components, perplexity=perplexity)
            transformed = tsne.fit_transform(self.df[numeric_cols])
            
            cols = [f'TSNE_{i+1}' for i in range(n_components)]
            return pd.DataFrame(transformed, columns=cols)
        
        elif method == 'svd' and len(numeric_cols) > 0:
            n_components = kwargs.get('n_components', min(10, len(numeric_cols)))
            svd = TruncatedSVD(n_components=n_components)
            transformed = svd.fit_transform(self.df[numeric_cols])
            
            cols = [f'SVD_{i+1}' for i in range(n_components)]
            return pd.DataFrame(transformed, columns=cols)
        
        elif method == 'kmeans' and len(numeric_cols) > 0:
            n_clusters = kwargs.get('n_clusters', 3)
            kmeans = KMeans(n_clusters=n_clusters)
            clusters = kmeans.fit_predict(self.df[numeric_cols])
            
            # Add cluster features
            self.df['cluster'] = clusters
            for i in range(n_clusters):
                self.df[f'cluster_{i}_dist'] = np.linalg.norm(
                    self.df[numeric_cols].sub(kmeans.cluster_centers_[i]), axis=1)
            
            return self.df
        
        elif method == 'tfidf' and len(text_cols) > 0:
            max_features = kwargs.get('max_features', 100)
            tfidf = TfidfVectorizer(max_features=max_features)
            
            results = []
            for col in text_cols:
                transformed = tfidf.fit_transform(self.df[col])
                cols = [f'{col}_tfidf_{i}' for i in range(transformed.shape[1])]
                results.append(pd.DataFrame(transformed.toarray(), columns=cols))
            
            return pd.concat([self.df] + results, axis=1)
        
        else:
            raise ValueError(f"Unsupported extraction method: {method} for available data")