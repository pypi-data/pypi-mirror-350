"""
ML-SuperTrend-MT5: Advanced SuperTrend trading bot for MetaTrader 5 with Machine Learning clustering

An advanced SuperTrend trading bot for MetaTrader 5 that leverages Machine Learning (K-means clustering) 
for dynamic parameter optimization, featuring adaptive risk management and comprehensive performance monitoring.

Author: xPOURY4
License: MIT
"""

__version__ = "1.0.0"
__author__ = "xPOURY4"
__email__ = "info@hexquant.xyz"
__license__ = "MIT"

from .core.supertrend_bot import SuperTrendBot
from .core.risk_manager import RiskManager
from .core.performance_monitor import PerformanceMonitor
from .core.news_filter import NewsFilter

__all__ = [
    "SuperTrendBot",
    "RiskManager", 
    "PerformanceMonitor",
    "NewsFilter",
] 