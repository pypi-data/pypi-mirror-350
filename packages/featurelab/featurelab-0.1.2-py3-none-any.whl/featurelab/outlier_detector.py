import pandas as pd
import numpy as np
from scipy import stats
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer

class OutlierDetector:
    """
    Detect and handle outliers with statistical methods and visualization
    """
    
    def __init__(self, df):
        self.df = df.copy()
        self.advisor = StatsAdvisor()
        self.visualizer = Visualizer()
        
    def detect_outliers(self, method='iqr', threshold=1.5):
        """
        Detect outliers using specified method
        
        Parameters:
        -----------
        method : str
            'iqr' - Interquartile Range
            'zscore' - Z-score method
            'modified_zscore' - Modified Z-score
            'percentile' - Percentile based
        threshold : float
            Threshold for outlier detection
        """
        outlier_report = {}
        
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            data = self.df[col].dropna()
            outliers = pd.Series(index=self.df.index, data=False)
            
            if method == 'iqr':
                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                outliers = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(data))
                outliers = z_scores > threshold
                
            elif method == 'modified_zscore':
                median = np.median(data)
                mad = np.median(np.abs(data - median))
                modified_z_scores = 0.6745 * (data - median) / mad
                outliers = np.abs(modified_z_scores) > threshold
                
            elif method == 'percentile':
                lower_bound = data.quantile((1 - threshold)/2)
                upper_bound = data.quantile(1 - (1 - threshold)/2)
                outliers = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            
            outlier_report[col] = {
                'outliers': outliers.sum(),
                'percentage': outliers.mean() * 100,
                'indices': self.df[outliers].index.tolist(),
                'method': method,
                'threshold': threshold
            }
            
            # Plot distribution with outliers highlighted
            self.visualizer.plot_outliers(self.df[col], outliers, col)
        
        return outlier_report
    
    def handle_outliers(self, strategy='winsorize', report=None, **kwargs):
        """
        Handle outliers based on specified strategy
        
        Parameters:
        -----------
        strategy : str or dict
            'remove' - Remove outliers
            'winsorize' - Cap outliers at percentiles
            'transform' - Apply log/sqrt transform
            'impute' - Replace with median/mean
            dict - column-specific strategies
        report : dict
            Outlier report from detect_outliers()
        """
        if report is None:
            report = self.detect_outliers(**kwargs)
            
        for col, col_report in report.items():
            outliers = col_report['outliers']
            if outliers == 0:
                continue
                
            if strategy == 'remove':
                self.df = self.df[~self.df.index.isin(col_report['indices'])]
            elif strategy == 'winsorize':
                lower = self.df[col].quantile(0.05)
                upper = self.df[col].quantile(0.95)
                self.df[col] = np.where(self.df[col] < lower, lower, 
                                      np.where(self.df[col] > upper, upper, self.df[col]))
            elif strategy == 'transform':
                if self.df[col].min() > 0:
                    self.df[col] = np.log1p(self.df[col])
                else:
                    self.df[col] = np.sign(self.df[col]) * np.sqrt(np.abs(self.df[col]))
            elif strategy == 'impute':
                median = self.df[col].median()
                self.df.loc[self.df.index.isin(col_report['indices']), col] = median
        
        return self.df