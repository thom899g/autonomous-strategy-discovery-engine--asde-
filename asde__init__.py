"""
Autonomous Strategy Discovery Engine (ASDE)
A world-model based trading strategy discovery system that operates autonomously.
"""

__version__ = "1.0.0"
__author__ = "Evolution Ecosystem"
__license__ = "Proprietary"

from asde.meta.orchestrator import MetaCognitiveOrchestrator
from asde.perception.causal_discovery import CausalDiscoveryEngine
from asde.hypothesis.generator import StrategyHypothesisGenerator
from asde.experimentation.backtest import AdaptiveBacktestEngine

__all__ = [
    "MetaCognitiveOrchestrator",
    "CausalDiscoveryEngine", 
    "StrategyHypothesisGenerator",
    "AdaptiveBacktestEngine"
]