import pandas as pd
import numpy as np
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class NullHandler:
    """
    Handle missing values with statistical guidance and visualization
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def analyze_null(self):
        """Analyze null values and provide recommendations"""
        null_counts = self.df.isnull().sum()
        null_percent = null_counts / len(self.df) * 100
        
        report = {
            'null_counts': null_counts,
            'null_percentage': null_percent,
            'recommendations': {}
        }
        
        for col in self.df.columns:
            if null_counts[col] > 0:
                col_type = self.df[col].dtype
                dist_stats = self.advisor.analyze_distribution(self.df[col].dropna())
                
                if null_percent[col] > 30:
                    rec = f"Consider dropping column '{col}' as {null_percent[col]:.2f}% values are missing"
                elif col_type in ['float64', 'int64']:
                    if dist_stats['skewness'] > 1:
                        rec = f"Use median imputation (median={dist_stats['median']:.2f}) due to high skewness"
                    else:
                        rec = f"Use mean imputation (mean={dist_stats['mean']:.2f})"
                else:
                    rec = f"Use mode imputation (mode={self.df[col].mode()[0]})"
                
                report['recommendations'][col] = {
                    'recommendation': rec,
                    'stats': dist_stats
                }
        
        # Generate visualization
        self.visualizer.plot_null_matrix(self.df)
        self.visualizer.plot_null_distribution(null_percent)
        
        return report
    
    def handle_null(self, strategy='auto', custom_values=None):
        """
        Handle null values based on strategy or user choice
        
        Parameters:
        -----------
        strategy : str or dict
            'auto' - follow recommendations
            'drop' - drop rows with nulls
            'fill' - fill with specified values
            dict - column-specific strategies {'col1': 'mean', 'col2': 0}
        custom_values : dict
            Custom fill values for each column
        """
        if strategy == 'auto':
            report = self.analyze_null()
            for col, rec in report['recommendations'].items():
                rec_text = rec['recommendation'].lower()
                if 'drop column' in rec_text:
                    self.df.drop(col, axis=1, inplace=True)
                elif 'median' in rec_text:
                    self.df[col].fillna(rec['stats']['median'], inplace=True)
                elif 'mean' in rec_text:
                    self.df[col].fillna(rec['stats']['mean'], inplace=True)
                else:  # mode
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        elif strategy == 'drop':
            self.df.dropna(inplace=True)
        elif strategy == 'fill' and custom_values:
            self.df.fillna(custom_values, inplace=True)
        elif isinstance(strategy, dict):
            for col, method in strategy.items():
                if method == 'mean':
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif method == 'median':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif method == 'mode':
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
                elif method == 'drop':
                    self.df.drop(col, axis=1, inplace=True)
                elif method == 'dropna':
                    self.df.dropna(subset=[col], inplace=True)
        
        return self.df