"""
Configuration settings for Elasticsearch parallel processing.
"""

import os
from typing import Dict, Any

class ElasticsearchParallelConfig:
    """Configuration class for Elasticsearch parallel processing settings."""
    
    # Default values
    DEFAULT_MAX_WORKERS = 5
    DEFAULT_CHUNK_SIZE = 100
    DEFAULT_BATCH_SIZE = 50
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRY_ATTEMPTS = 3
    DEFAULT_RETRY_DELAY = 1  # seconds
    
    def __init__(self):
        # Load from environment variables with fallbacks to defaults
        self.max_workers = int(os.getenv("ES_MAX_WORKERS", self.DEFAULT_MAX_WORKERS))
        self.chunk_size = int(os.getenv("ES_CHUNK_SIZE", self.DEFAULT_CHUNK_SIZE))
        self.batch_size = int(os.getenv("ES_BATCH_SIZE", self.DEFAULT_BATCH_SIZE))
        self.timeout = int(os.getenv("ES_OPERATION_TIMEOUT", self.DEFAULT_TIMEOUT))
        self.retry_attempts = int(os.getenv("ES_RETRY_ATTEMPTS", self.DEFAULT_RETRY_ATTEMPTS))
        self.retry_delay = float(os.getenv("ES_RETRY_DELAY", self.DEFAULT_RETRY_DELAY))
        
        # Performance tuning flags
        self.enable_bulk_operations = os.getenv("ES_ENABLE_BULK", "true").lower() == "true"
        self.progress_logging_interval = int(os.getenv("ES_PROGRESS_LOG_INTERVAL", "100"))
        
        # Validate settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate configuration settings."""
        if self.max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        if self.max_workers > 20:
            # Warning for very high worker counts
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"High worker count ({self.max_workers}) may overwhelm Elasticsearch. Consider reducing.")
        
        if self.chunk_size < 1:
            raise ValueError("chunk_size must be at least 1")
        if self.batch_size < 1:
            raise ValueError("batch_size must be at least 1")
        if self.timeout < 1:
            raise ValueError("timeout must be at least 1 second")
        if self.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Return configuration as a dictionary."""
        return {
            "max_workers": self.max_workers,
            "chunk_size": self.chunk_size,
            "batch_size": self.batch_size,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "enable_bulk_operations": self.enable_bulk_operations,
            "progress_logging_interval": self.progress_logging_interval
        }
    
    def __str__(self) -> str:
        """String representation of the configuration."""
        config_dict = self.get_config_dict()
        config_lines = [f"  {key}: {value}" for key, value in config_dict.items()]
        return "ElasticsearchParallelConfig:\n" + "\n".join(config_lines)

# Environment-specific configurations
class DevelopmentParallelConfig(ElasticsearchParallelConfig):
    """Development environment configuration with conservative settings."""
    
    DEFAULT_MAX_WORKERS = 3
    DEFAULT_CHUNK_SIZE = 50
    DEFAULT_BATCH_SIZE = 25

class ProductionParallelConfig(ElasticsearchParallelConfig):
    """Production environment configuration with optimized settings."""
    
    DEFAULT_MAX_WORKERS = 8
    DEFAULT_CHUNK_SIZE = 200
    DEFAULT_BATCH_SIZE = 100

class TestingParallelConfig(ElasticsearchParallelConfig):
    """Testing environment configuration with minimal parallelization."""
    
    DEFAULT_MAX_WORKERS = 2
    DEFAULT_CHUNK_SIZE = 10
    DEFAULT_BATCH_SIZE = 5

def get_parallel_config(env: str = None) -> ElasticsearchParallelConfig:
    """
    Get the appropriate parallel configuration based on environment.
    
    Args:
        env: Environment name (development, production, testing)
             If None, reads from APP_ENV environment variable
             
    Returns:
        Appropriate configuration instance
    """
    if env is None:
        env = os.getenv("APP_ENV", "development").lower()
    
    config_map = {
        "development": DevelopmentParallelConfig,
        "production": ProductionParallelConfig,
        "testing": TestingParallelConfig,
        "staging": ProductionParallelConfig,  # Use production config for staging
    }
    
    config_class = config_map.get(env, DevelopmentParallelConfig)
    return config_class()

# Example usage and documentation
if __name__ == "__main__":
    print("Elasticsearch Parallel Configuration Examples")
    print("=" * 50)
    
    # Show configurations for different environments
    for env_name in ["development", "production", "testing"]:
        print(f"\n{env_name.upper()} Configuration:")
        config = get_parallel_config(env_name)
        print(config)
    
    print("\nEnvironment Variables:")
    print("You can override settings using these environment variables:")
    env_vars = [
        "ES_MAX_WORKERS - Number of parallel threads (default: varies by env)",
        "ES_CHUNK_SIZE - Documents per chunk (default: varies by env)",
        "ES_BATCH_SIZE - Documents per batch for bulk operations (default: varies by env)",
        "ES_OPERATION_TIMEOUT - Timeout for operations in seconds (default: 30)",
        "ES_RETRY_ATTEMPTS - Number of retry attempts (default: 3)",
        "ES_RETRY_DELAY - Delay between retries in seconds (default: 1)",
        "ES_ENABLE_BULK - Enable bulk operations (default: true)",
        "ES_PROGRESS_LOG_INTERVAL - Progress logging interval (default: 100)"
    ]
    for var in env_vars:
        print(f"  - {var}") 