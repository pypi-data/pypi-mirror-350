import pandas as pd
import numpy as np
from sklearn.feature_selection import (
    SelectKBest, SelectPercentile, RFE, RFECV,
    SelectFromModel, VarianceThreshold, f_classif, f_regression
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso, LogisticRegression
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class FeatureSelector:
    """
    Feature selection with various statistical and model-based methods
    """
    
    def __init__(self, X, y=None):
        self.X = X.copy()
        self.y = y.copy() if y is not None else None
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def analyze_features(self, problem_type='classification'):
        """Analyze features and suggest selection methods"""
        suggestions = []
        
        # Check for low variance features
        var_threshold = VarianceThreshold()
        try:
            var_threshold.fit(self.X)
            n_low_var = (var_threshold.variances_ == 0).sum()
            if n_low_var > 0:
                suggestions.append(f"{n_low_var} constant features - remove with VarianceThreshold")
        except:
            pass
        
        # Check for correlated features
        corr_matrix = self.X.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        high_corr = [column for column in upper.columns if any(upper[column] > 0.9)]
        if high_corr:
            suggestions.append(f"{len(high_corr)} highly correlated features - consider removing with correlation threshold")
        
        # Add statistical suggestions
        if self.y is not None:
            stats_suggestions = self.advisor.suggest_feature_selection(self.X, self.y, problem_type)
            suggestions.extend(stats_suggestions)
        
        # Add model-based suggestions
        if self.y is not None:
            if problem_type == 'classification':
                suggestions.append("RandomForest feature importance")
                suggestions.append("L1 regularization (LogisticRegression)")
            else:
                suggestions.append("RandomForest feature importance")
                suggestions.append("Lasso regression")
        
        return suggestions
    
    def select_features(self, method='auto', problem_type='classification', **kwargs):
        """
        Perform feature selection
        
        Parameters:
        -----------
        method : str
            'auto' - follow recommendations
            'variance' - remove low variance
            'correlation' - remove correlated
            'univariate' - statistical tests
            'rfe' - recursive feature elimination
            'model' - model-based selection
        problem_type : str
            'classification' or 'regression'
        """
        if method == 'auto':
            suggestions = self.analyze_features(problem_type)
            if "VarianceThreshold" in suggestions[0]:
                return self.select_features(method='variance')
            elif "RandomForest" in suggestions[-1]:
                return self.select_features(method='model', estimator='random_forest')
            else:
                return self.select_features(method='univariate', score_func=suggestions[0])
        
        if method == 'variance':
            selector = VarianceThreshold(threshold=kwargs.get('threshold', 0))
            selected = selector.fit_transform(self.X)
            selected_cols = self.X.columns[selector.get_support()]
            return pd.DataFrame(selected, columns=selected_cols)
        
        elif method == 'correlation':
            corr_matrix = self.X.corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            to_drop = [column for column in upper.columns if any(upper[column] > kwargs.get('threshold', 0.9))]
            return self.X.drop(to_drop, axis=1)
        
        elif method == 'univariate':
            score_func = kwargs.get('score_func', 
                                  f_classif if problem_type == 'classification' else f_regression)
            k = kwargs.get('k', 'all')
            
            selector = SelectKBest(score_func=score_func, k=k)
            selected = selector.fit_transform(self.X, self.y)
            selected_cols = self.X.columns[selector.get_support()]
            
            # Plot feature scores
            scores = pd.Series(selector.scores_, index=self.X.columns, name='feature_scores')
            self.visualizer.plot_feature_importance(scores.sort_values(ascending=False))
            
            return pd.DataFrame(selected, columns=selected_cols)
        
        elif method == 'rfe':
            estimator = self._get_estimator(problem_type, kwargs.get('estimator'))
            n_features = kwargs.get('n_features', None)
            step = kwargs.get('step', 1)
            
            selector = RFECV(estimator=estimator, step=step, cv=5)
            selected = selector.fit_transform(self.X, self.y)
            selected_cols = self.X.columns[selector.support_]
            
            # Plot RFE results
            self.visualizer.plot_rfe_results(selector)
            
            return pd.DataFrame(selected, columns=selected_cols)
        
        elif method == 'model':
            estimator = self._get_estimator(problem_type, kwargs.get('estimator'))
            threshold = kwargs.get('threshold', 'mean')
            
            if isinstance(estimator, (RandomForestClassifier, RandomForestRegressor)):
                estimator.fit(self.X, self.y)
                importances = pd.Series(estimator.feature_importances_, index=self.X.columns)
                selected_cols = importances[importances > importances.mean() * 0.5].index
                
                # Plot feature importances
                self.visualizer.plot_feature_importance(importances.sort_values(ascending=False))
                
                return self.X[selected_cols]
            else:  # Lasso/Logistic
                selector = SelectFromModel(estimator, threshold=threshold)
                selected = selector.fit_transform(self.X, self.y)
                selected_cols = self.X.columns[selector.get_support()]
                return pd.DataFrame(selected, columns=selected_cols)
    
    def _get_estimator(self, problem_type, estimator_type=None):
        """Get appropriate estimator for feature selection"""
        if estimator_type == 'random_forest':
            if problem_type == 'classification':
                return RandomForestClassifier(n_estimators=100)
            else:
                return RandomForestRegressor(n_estimators=100)
        elif estimator_type == 'lasso':
            if problem_type == 'classification':
                return LogisticRegression(penalty='l1', solver='liblinear')
            else:
                return Lasso(alpha=0.1)
        else:
            if problem_type == 'classification':
                return LogisticRegression()
            else:
                return Lasso()