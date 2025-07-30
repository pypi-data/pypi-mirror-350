import numpy as np
import pandas as pd
from scipy import stats
from sklearn.feature_selection import (f_classif, f_regression, 
                                     mutual_info_classif, mutual_info_regression,
                                     chi2)

class StatsAdvisor:
    """
    Provide statistical advice for feature engineering decisions
    """
    
    def analyze_distribution(self, data):
        """Analyze distribution of a column"""
        if pd.api.types.is_numeric_dtype(data):
            skewness = stats.skew(data.dropna())
            kurtosis = stats.kurtosis(data.dropna())
            normality = stats.normaltest(data.dropna())[1]  # p-value
            
            return {
                'mean': np.mean(data),
                'median': np.median(data),
                'std': np.std(data),
                'skewness': skewness,
                'kurtosis': kurtosis,
                'normality_p': normality,
                'is_normal': normality > 0.05
            }
        else:
            value_counts = data.value_counts(normalize=True)
            return {
                'unique_values': len(value_counts),
                'most_common': value_counts.idxmax(),
                'most_common_pct': value_counts.max() * 100,
                'entropy': stats.entropy(value_counts)
            }
    
    def suggest_feature_selection(self, X, y, problem_type='classification'):
        """
        Suggest feature selection methods based on data characteristics
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target variable
        problem_type : str
            'classification' or 'regression'
        """
        suggestions = []
        
        # Check feature types
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object', 'category']).columns
        
        # Check target type
        if problem_type == 'classification':
            target_cardinality = len(y.unique())
            if target_cardinality == 2:
                suggestions.append("chi2 (for categorical features)")
                suggestions.append("mutual_info_classif (for all features)")
                suggestions.append("f_classif (ANOVA F-value for numeric features)")
            else:
                suggestions.append("f_classif (ANOVA F-value for numeric features)")
                suggestions.append("mutual_info_classif (for all features)")
        else:  # regression
            suggestions.append("f_regression (Pearson correlation for numeric features)")
            suggestions.append("mutual_info_regression (for all features)")
        
        # Check feature distributions
        for col in numeric_features:
            dist_stats = self.analyze_distribution(X[col])
            if not dist_stats['is_normal']:
                suggestions.append(f"Consider rank-based methods for {col} (non-normal distribution)")
        
        if len(categorical_features) > 0:
            suggestions.append("Consider chi-square tests for categorical-categorical relationships")
            suggestions.append("Consider Cramer's V for categorical-categorical associations")
        
        return list(set(suggestions))  # Remove duplicates
    
    def run_feature_selection(self, X, y, method='auto', problem_type='classification'):
        """
        Run specified feature selection method
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target variable
        method : str
            Feature selection method
        problem_type : str
            'classification' or 'regression'
        """
        if method == 'auto':
            suggestions = self.suggest_feature_selection(X, y, problem_type)
            method = suggestions[0]  # Use first suggestion
            
        numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
        categorical_features = X.select_dtypes(include=['object', 'category']).columns
        
        if method == 'f_classif':
            scores, _ = f_classif(X[numeric_features], y)
            return pd.Series(scores, index=numeric_features, name='f_score')
        elif method == 'f_regression':
            scores, _ = f_regression(X[numeric_features], y)
            return pd.Series(scores, index=numeric_features, name='f_score')
        elif method == 'mutual_info_classif':
            scores = mutual_info_classif(X, y)
            return pd.Series(scores, index=X.columns, name='mutual_info')
        elif method == 'mutual_info_regression':
            scores = mutual_info_regression(X, y)
            return pd.Series(scores, index=X.columns, name='mutual_info')
        elif method == 'chi2':
            # For chi2, need positive values and encode categoricals
            X_encoded = pd.get_dummies(X[categorical_features])
            scores, _ = chi2(X_encoded, y)
            return pd.Series(scores, index=X_encoded.columns, name='chi2_score')
        else:
            raise ValueError(f"Unsupported feature selection method: {method}")