"""
Configuration management for ASDE with environment-based settings and validation.
Architectural Rationale: Centralized config prevents scattered magic values and
enforces type safety across the system. Environment variable validation ensures
fail-fast behavior for misconfiguration.
"""
import os
import sys
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

class LogLevel(Enum):
    """Standardized logging levels for consistent verbosity control."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation and default fallbacks."""
    project_id: str = field(default_factory=lambda: os.getenv("FIREBASE_PROJECT_ID", ""))
    credentials_path: str = field(default_factory=lambda: os.getenv("FIREBASE_CREDENTIALS", "firebase-credentials.json"))
    
    def validate(self) -> None:
        """Validate Firebase configuration and raise informative errors."""
        if not self.project_id:
            raise ValueError("FIREBASE_PROJECT_ID environment variable must be set")
        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"Firebase credentials not found at: {self.credentials_path}")

@dataclass
class DataConfig:
    """Data source and preprocessing configuration."""
    market_data_source: str = field(default_factory=lambda: os.getenv("MARKET_DATA_SOURCE", "ccxt"))
    max_data_points: int = field(default_factory=lambda: int(os.getenv("MAX_DATA_POINTS", "100000")))
    cache_enabled: bool = field(default_factory=lambda: os.getenv("CACHE_ENABLED", "true").lower() == "true")
    
    def validate(self) -> None:
        """Validate data configuration parameters."""
        if self.max_data_points <= 0:
            raise ValueError(f"MAX_DATA_POINTS must be positive, got {self.max_data_points}")
        valid_sources = ["ccxt", "yfinance", "alpaca"]
        if self.market_data_source not in valid_sources:
            raise ValueError(f"Invalid market data source. Must be one of {valid_sources}")

@dataclass
class ASDEConfig:
    """Main configuration container with dependency injection support."""
    # Core system
    log_level: LogLevel = field(default_factory=lambda: LogLevel[os.getenv("LOG_LEVEL", "INFO")])
    system_id: str = field(default_factory=lambda: os.getenv("SYSTEM_ID", "asde-prod-001"))
    
    # Component configurations
    firebase: FirebaseConfig = field(default_factory=FirebaseConfig)
    data: DataConfig = field(default_factory=DataConfig)
    
    # Performance tuning
    max_parallel_experiments: int = field(default_factory=lambda: int(os.getenv("MAX_PARALLEL_EXPERIMENTS", "4")))
    simulation_timeout_seconds: int = field(default_factory=lambda: int(os.getenv("SIMULATION_TIMEOUT_SECONDS", "300")))
    
    # Feature toggles
    enable_causal_discovery: bool = field(default_factory=lambda: os.getenv("ENABLE_CAUSAL_DISCOVERY", "true").lower() == "true")
    enable_live_trading: bool = field(default_factory=lambda: os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true")
    
    def __post_init__(self) -> None:
        """Post-initialization validation and setup."""
        try:
            self.firebase.validate()
            self.data.validate()
            
            # Boundary checks for performance parameters
            if self.max_parallel_experiments <= 0:
                raise ValueError("MAX_PARALLEL_EXPERIMENTS must be at least 1")
            if self.simulation_timeout_seconds < 30:
                raise ValueError("SIMULATION_TIMEOUT_SECONDS must be at least 30 seconds")