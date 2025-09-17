"""
Football Pool Domination System

A comprehensive Python-based system for maximizing your success in NFL/College
football confidence pools.
"""

__version__ = "1.0.0"
__author__ = "Football Pool Domination Team"

from .core import PoolDominationSystem
from .models import CompetitorPick, GameResult, Pick

__all__ = ["PoolDominationSystem", "Pick", "GameResult", "CompetitorPick"]
