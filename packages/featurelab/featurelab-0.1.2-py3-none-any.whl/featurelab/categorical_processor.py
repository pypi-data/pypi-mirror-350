import pandas as pd
import numpy as np
from sklearn.preprocessing import (OneHotEncoder, OrdinalEncoder, 
                                 LabelEncoder, TargetEncoder)
from category_encoders import (BinaryEncoder, CountEncoder, 
                              WOEEncoder, CatBoostEncoder)
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class CategoricalProcessor:
    """
    Handle categorical variables with various encoding strategies
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def analyze_categorical(self, target=None):
        """Analyze categorical columns and suggest encoding methods"""
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        report = {}
        
        for col in cat_cols:
            stats = self.advisor.analyze_distribution(self.df[col])
            stats['suggestions'] = self._suggest_encoding(col, stats, target)
            report[col] = stats
            
            # Plot categorical distribution
            self.visualizer.plot_categorical(self.df[col])
        
        return report
    
    def _suggest_encoding(self, col, stats, target=None):
        """Suggest encoding methods based on column characteristics"""
        suggestions = []
        cardinality = stats['unique_values']
        
        if cardinality < 5:
            suggestions.append('one-hot encoding')
        elif 5 <= cardinality < 20:
            suggestions.append('ordinal encoding')
            suggestions.append('target encoding (if target available)')
        else:
            suggestions.append('frequency encoding')
            suggestions.append('binary encoding')
            suggestions.append('hash encoding')
        
        if target is not None:
            suggestions.append('target encoding')
            suggestions.append('WOE encoding (for classification)')
            suggestions.append('catboost encoding')
        
        if stats['most_common_pct'] > 70:  # High imbalance
            suggestions.append('consider grouping rare categories')
        
        return suggestions
    
    def encode_categorical(self, strategy='auto', target=None, **kwargs):
        """
        Encode categorical variables
        
        Parameters:
        -----------
        strategy : str or dict
            'auto' - follow recommendations
            'onehot' - one-hot encoding
            'ordinal' - ordinal encoding
            'target' - target encoding
            dict - column-specific strategies
        target : str
            Target column name for supervised encoding
        """
        if strategy == 'auto':
            report = self.analyze_categorical(target)
            for col, col_stats in report.items():
                if 'one-hot encoding' in col_stats['suggestions'] and col_stats['unique_values'] < 10:
                    self._onehot_encode(col, **kwargs)
                elif 'ordinal encoding' in col_stats['suggestions']:
                    self._ordinal_encode(col, **kwargs)
                elif target is not None and 'target encoding' in col_stats['suggestions']:
                    self._target_encode(col, target, **kwargs)
                else:
                    self._frequency_encode(col, **kwargs)
        elif isinstance(strategy, dict):
            for col, method in strategy.items():
                if method == 'onehot':
                    self._onehot_encode(col, **kwargs)
                elif method == 'ordinal':
                    self._ordinal_encode(col, **kwargs)
                elif method == 'target' and target is not None:
                    self._target_encode(col, target, **kwargs)
                elif method == 'frequency':
                    self._frequency_encode(col, **kwargs)
                elif method == 'binary':
                    self._binary_encode(col, **kwargs)
        else:
            if strategy == 'onehot':
                self._onehot_encode(**kwargs)
            elif strategy == 'ordinal':
                self._ordinal_encode(**kwargs)
            elif strategy == 'target' and target is not None:
                self._target_encode(target=target, **kwargs)
        
        return self.df
    
    def _onehot_encode(self, columns=None, drop_first=False):
        """One-hot encoding implementation"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        self.df = pd.get_dummies(self.df, columns=columns, drop_first=drop_first)
        return self.df
    
    def _ordinal_encode(self, columns=None, categories='auto'):
        """Ordinal encoding implementation"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        encoder = OrdinalEncoder(categories=categories)
        self.df[columns] = encoder.fit_transform(self.df[columns])
        return self.df
    
    def _target_encode(self, columns=None, target=None, smoothing=1.0):
        """Target encoding implementation"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        encoder = TargetEncoder(smoothing=smoothing)
        self.df[columns] = encoder.fit_transform(self.df[columns], self.df[target])
        return self.df
    
    def _frequency_encode(self, columns=None):
        """Frequency encoding implementation"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        for col in columns:
            freq = self.df[col].value_counts(normalize=True)
            self.df[col+'_freq'] = self.df[col].map(freq)
            self.df.drop(col, axis=1, inplace=True)
        
        return self.df
    
    def _binary_encode(self, columns=None):
        """Binary encoding implementation"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object', 'category']).columns
        
        encoder = BinaryEncoder(cols=columns)
        self.df = encoder.fit_transform(self.df)
        return self.df