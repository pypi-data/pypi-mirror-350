import pandas as pd
import numpy as np
from typing import Union, List

class FeatureUtils:
    """
    Utility functions for feature engineering as class methods.
    """

    @staticmethod
    def detect_column_types(df: pd.DataFrame) -> dict:
        """
        Detect column types in dataframe
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        
        Returns:
        --------
        dict
            Dictionary with column types classification
        """
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64', 'timedelta']).columns.tolist()
        text_cols = [col for col in categorical_cols 
                    if df[col].apply(lambda x: isinstance(x, str) and len(x.split()) > 3).any()]
        
        # Remove text columns from categorical
        categorical_cols = list(set(categorical_cols) - set(text_cols))
        
        return {
            'numeric': numeric_cols,
            'categorical': categorical_cols,
            'datetime': datetime_cols,
            'text': text_cols,
            'other': list(set(df.columns) - set(numeric_cols) - set(categorical_cols) - set(datetime_cols) - set(text_cols))
        }

    @staticmethod
    def convert_to_numeric(df: pd.DataFrame, columns: Union[str, List[str]] = 'auto') -> pd.DataFrame:
        """
        Convert columns to numeric type
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : str or list
            'auto' - automatically detect convertible columns
            list - specific columns to convert
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with converted columns
        """
        df = df.copy()
        
        if columns == 'auto':
            # Try to convert all object columns that look numeric
            for col in df.select_dtypes(include=['object']).columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
        else:
            if isinstance(columns, str):
                columns = [columns]
            for col in columns:
                df[col] = pd.to_numeric(df[col])
        
        return df

    @staticmethod
    def memory_optimize(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize dataframe memory usage
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        
        Returns:
        --------
        pd.DataFrame
            Memory-optimized dataframe
        """
        df = df.copy()
        
        # Downcast numeric columns
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        # Convert object to category if cardinality is low
        for col in df.select_dtypes(include=['object']).columns:
            if len(df[col].unique()) / len(df[col]) < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
        
        return df

    @staticmethod
    def split_datetime(df: pd.DataFrame, columns: Union[str, List[str]]) -> pd.DataFrame:
        """
        Split datetime columns into multiple features
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : str or list
            Datetime columns to split
        
        Returns:
        --------
        pd.DataFrame
            Dataframe with additional datetime features
        """
        df = df.copy()
        
        if isinstance(columns, str):
            columns = [columns]
        
        for col in columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[f'{col}_year'] = df[col].dt.year
                df[f'{col}_month'] = df[col].dt.month
                df[f'{col}_day'] = df[col].dt.day
                df[f'{col}_hour'] = df[col].dt.hour
                df[f'{col}_minute'] = df[col].dt.minute
                df[f'{col}_dayofweek'] = df[col].dt.dayofweek
                df[f'{col}_is_weekend'] = df[col].dt.dayofweek >= 5
        
        return df