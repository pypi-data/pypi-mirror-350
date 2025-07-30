"""
FeatureEngPro - A comprehensive feature engineering package with statistical guidance
"""

from .null_handler import NullHandler
from .outlier_detector import OutlierDetector
from .duplicate_handler import DuplicateHandler
from .categorical_processor import CategoricalProcessor
from .feature_selector import FeatureSelector
from .feature_extractor import FeatureExtractor
from .stats_advisor import StatsAdvisor
from .visualizer import Visualizer
from .utils import FeatureUtils

__version__ = "0.1.0"
__all__ = [
    'NullHandler',
    'OutlierDetector',
    'DuplicateHandler',
    'CategoricalProcessor',
    'FeatureSelector',
    'FeatureExtractor',
    'StatsAdvisor',
    'Visualizer',
    'FeatureUtils'
]