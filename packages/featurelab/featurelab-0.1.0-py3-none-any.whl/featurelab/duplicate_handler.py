import pandas as pd
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class DuplicateHandler:
    """
    Handle duplicate rows and columns with statistical analysis
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def analyze_duplicates(self):
        """Analyze duplicate rows and columns"""
        report = {
            'duplicate_rows': {
                'count': self.df.duplicated().sum(),
                'percentage': self.df.duplicated().mean() * 100,
                'indices': self.df[self.df.duplicated()].index.tolist()
            },
            'duplicate_columns': self._find_duplicate_columns()
        }
        
        # Visualize duplicates
        if report['duplicate_rows']['count'] > 0:
            self.visualizer.plot_duplicates(self.df)
        
        return report
    
    def _find_duplicate_columns(self):
        """Find duplicate columns in the dataframe"""
        duplicates = {}
        columns = self.df.columns
        
        for i in range(len(columns)):
            col1 = columns[i]
            if col1 not in duplicates:
                for j in range(i+1, len(columns)):
                    col2 = columns[j]
                    if self.df[col1].equals(self.df[col2]):
                        if col1 not in duplicates:
                            duplicates[col1] = []
                        duplicates[col1].append(col2)
        
        return duplicates
    
    def handle_duplicates(self, strategy='auto', keep='first', columns=None):
        """
        Handle duplicates based on specified strategy
        
        Parameters:
        -----------
        strategy : str
            'auto' - follow recommendations
            'drop' - drop duplicates
            'keep' - keep duplicates
        keep : str
            'first' - keep first occurrence
            'last' - keep last occurrence
            False - drop all duplicates
        columns : list
            Columns to consider for duplicate identification
        """
        report = self.analyze_duplicates()
        
        if strategy == 'auto':
            if report['duplicate_rows']['count'] > 0:
                self.df = self.df.drop_duplicates(keep=keep, subset=columns)
            
            for col, dup_cols in report['duplicate_columns'].items():
                for dup_col in dup_cols:
                    if dup_col in self.df.columns:
                        self.df = self.df.drop(dup_col, axis=1)
        
        elif strategy == 'drop':
            self.df = self.df.drop_duplicates(keep=keep, subset=columns)
        
        return self.df