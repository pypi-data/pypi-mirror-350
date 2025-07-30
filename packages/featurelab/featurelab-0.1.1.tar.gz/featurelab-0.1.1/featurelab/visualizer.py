import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import numpy as np

class Visualizer:
    """
    Visualization tools for feature engineering
    """
    
    def plot_null_matrix(self, df):
        """Visualize null values in the dataframe"""
        plt.figure(figsize=(10, 6))
        msno.matrix(df)
        plt.title('Null Value Matrix')
        plt.show()
    
    def plot_null_distribution(self, null_percent):
        """Plot percentage of null values per column"""
        plt.figure(figsize=(10, 6))
        null_percent[null_percent > 0].sort_values().plot(kind='barh')
        plt.title('Percentage of Missing Values by Column')
        plt.xlabel('Percentage Missing')
        plt.ylabel('Column Name')
        plt.grid(True)
        plt.show()
    
    def plot_outliers(self, data, outliers, col_name):
        """Visualize outliers in a column"""
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        sns.boxplot(y=data)
        plt.title(f'Boxplot of {col_name}')
        
        plt.subplot(1, 2, 2)
        sns.histplot(data, kde=True)
        plt.axvline(data.mean(), color='r', linestyle='--', label='Mean')
        plt.axvline(data.median(), color='g', linestyle='-', label='Median')
        plt.title(f'Distribution of {col_name}')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def plot_feature_importance(self, importance_scores):
        """Plot feature importance scores"""
        plt.figure(figsize=(10, 8))
        importance_scores.sort_values().plot(kind='barh')
        plt.title('Feature Importance Scores')
        plt.xlabel('Score')
        plt.grid(True)
        plt.show()
    
    def plot_correlation_matrix(self, df):
        """Plot correlation matrix for numeric features"""
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if len(numeric_df.columns) > 1:
            plt.figure(figsize=(12, 10))
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
            plt.title('Feature Correlation Matrix')
            plt.show()


    def plot_duplicates(self, df):
        """Visualize duplicate rows"""
        plt.figure(figsize=(10, 6))
        msno.dendrogram(df)
        plt.title('Duplicate Row Dendrogram')
        plt.show()

    def plot_categorical(self, data):
        """Plot categorical distribution"""
        plt.figure(figsize=(10, 6))
        if len(data.unique()) <= 10:
            data.value_counts().plot(kind='bar')
        else:
            data.value_counts().head(20).plot(kind='bar')
        plt.title(f'Distribution of {data.name}')
        plt.xticks(rotation=45)
        plt.show()

    def plot_pca_variance(self, pca):
        """Plot PCA explained variance"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(pca.explained_variance_ratio_)+1), 
                 np.cumsum(pca.explained_variance_ratio_),
                 marker='o')
        plt.xlabel('Number of Components')
        plt.ylabel('Cumulative Explained Variance')
        plt.title('PCA Explained Variance')
        plt.grid(True)
        plt.show()

    def plot_rfe_results(self, rfe):
        """Plot RFE results"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(rfe.grid_scores_) + 1), rfe.grid_scores_)
        plt.xlabel('Number of Features Selected')
        plt.ylabel('Cross Validation Score')
        plt.title('Recursive Feature Elimination')
        plt.grid(True)
        plt.show()