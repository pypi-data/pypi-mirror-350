import logging
import os
from urllib.parse import quote_plus
from pathlib import Path # Added pathlib
from dotenv import load_dotenv # Added dotenv

logger = logging.getLogger(__name__)

# Path to the 'data_engineering/config/' directory.
# Assumes configs.py is in 'data_engineering/config/aetherml_settings/'
PROJECT_CONFIG_ROOT_DIR = Path(__file__).resolve().parent.parent

class BaseConfig:
    """Base configuration class."""
    DB_TYPE: str = "SQLITE" # Default DB type
    # Construct absolute path for the default SQLite DB
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{ (PROJECT_CONFIG_ROOT_DIR / 'default_app_db.db').resolve() }"

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | int | None = None # Stored as string from env, converted if needed
    DB_NAME: str | None = None # For SQLite, this should be just the filename or :memory:

    # Elasticsearch Configuration
    ES_HOST: str | None = None
    ES_PORT: int | None = None
    ES_SCHEME: str | None = "http" # Default scheme
    ES_USER: str | None = None
    ES_PASSWORD: str | None = None
    ES_TIMEOUT: int = 30 # Default timeout in seconds
    ES_API_KEY: str | None = None

    def __init__(self):
        self._configure_db_url()

    def _configure_db_url(self):
        db_type_upper = self.DB_TYPE.upper()
        
        if db_type_upper == "POSTGRES" and all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, str(self.DB_PORT), self.DB_NAME]):
            encoded_password = quote_plus(self.DB_PASSWORD)
            self.SQLALCHEMY_DATABASE_URL = f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif db_type_upper == "REDSHIFT" and all([self.DB_USER, self.DB_PASSWORD, self.DB_HOST, str(self.DB_PORT), self.DB_NAME]):
            encoded_password = quote_plus(self.DB_PASSWORD)
            self.SQLALCHEMY_DATABASE_URL = f"postgresql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" # Redshift uses PG protocol
        elif db_type_upper == "SQLITE":
            # DB_NAME should be just the filename (e.g., "default_app_db.db") or ":memory:"
            sqlite_db_name_only = Path(self.DB_NAME or "default_app_db.db").name
            
            if sqlite_db_name_only == ":memory:":
                self.SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
            else:
                # Construct absolute path relative to the PROJECT_CONFIG_ROOT_DIR
                db_file_path = PROJECT_CONFIG_ROOT_DIR / sqlite_db_name_only
                self.SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_file_path.resolve()}"
        else:
            logger.warning(f"DB_TYPE '{self.DB_TYPE}' is not recognized or missing parameters. Using fallback SQLite URL: {self.SQLALCHEMY_DATABASE_URL}")
            # Ensure fallback is also an absolute path if it's SQLite and not already absolute
            # This check is a bit simplistic, assuming non-memory SQLite URLs have "sqlite:///"
            # Corrected variable name from previous context for clarity
            fallback_sqlite_db_name = Path(self.DB_NAME or "default_app_db.db").name
            if self.SQLALCHEMY_DATABASE_URL.startswith("sqlite:///") and fallback_sqlite_db_name != ":memory:":
                current_path_str = self.SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
                if not Path(current_path_str).is_absolute(): # Check if it's not already absolute
                    fallback_db_path = PROJECT_CONFIG_ROOT_DIR / Path(current_path_str).name
                    self.SQLALCHEMY_DATABASE_URL = f"sqlite:///{fallback_db_path.resolve()}"

class DevelopmentConfig(BaseConfig):
    def __init__(self):
        self.DB_TYPE = os.getenv("DEV_DB_TYPE", "SQLITE").upper()
        self.DB_USER = os.getenv("DEV_DB_USER")
        self.DB_PASSWORD = os.getenv("DEV_DB_PASSWORD")
        self.DB_HOST = os.getenv("DEV_DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DEV_DB_PORT")
        # For SQLite, DB_NAME should be just the filename, path is handled in _configure_db_url
        self.DB_NAME = os.getenv("DEV_DB_NAME", "default_app_db.db") 
        if not self.DB_PORT: # Default ports if not set
            if self.DB_TYPE == "POSTGRES": self.DB_PORT = "5432"
            elif self.DB_TYPE == "REDSHIFT": self.DB_PORT = "5439"
        
        # Elasticsearch Dev Config
        self.ES_HOST = os.getenv("ES_HOST")
        self.ES_PORT = int(os.getenv("ES_PORT")) if os.getenv("ES_PORT") else None
        self.ES_SCHEME = os.getenv("ES_SCHEME", "http")
        self.ES_USER = os.getenv("ES_USER")
        self.ES_PASSWORD = os.getenv("ES_PASSWORD")
        self.ES_TIMEOUT = int(os.getenv("ES_TIMEOUT", "30"))
        self.ES_API_KEY = os.getenv("ES_API_KEY")
        super().__init__()

class TestingConfig(BaseConfig):
    def __init__(self):
        self.DB_TYPE = os.getenv("TEST_DB_TYPE", "SQLITE").upper()
        self.DB_USER = os.getenv("TEST_DB_USER")
        self.DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
        self.DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
        self.DB_PORT = os.getenv("TEST_DB_PORT")
        # For SQLite, DB_NAME should be just the filename or :memory:
        self.DB_NAME = os.getenv("TEST_DB_NAME", ":memory:") 
        if not self.DB_PORT and self.DB_TYPE != "SQLITE": # Default ports if not set and not SQLite
            if self.DB_TYPE == "POSTGRES": self.DB_PORT = "5432"
            elif self.DB_TYPE == "REDSHIFT": self.DB_PORT = "5439"

        # Elasticsearch Test Config
        self.ES_HOST = os.getenv("ES_HOST")
        self.ES_PORT = int(os.getenv("ES_PORT")) if os.getenv("ES_PORT") else None
        self.ES_SCHEME = os.getenv("ES_SCHEME", "http")
        self.ES_USER = os.getenv("ES_USER")
        self.ES_PASSWORD = os.getenv("TEST_ES_PASSWORD")
        self.ES_TIMEOUT = int(os.getenv("TEST_ES_TIMEOUT", "10")) # Shorter timeout for tests
        self.ES_API_KEY = os.getenv("ES_API_KEY")
        super().__init__()

class StagingConfig(BaseConfig):
    def __init__(self):
        self.DB_TYPE = os.getenv("STAGE_DB_TYPE", "POSTGRES").upper()
        self.DB_USER = os.getenv("STAGE_DB_USER")
        self.DB_PASSWORD = os.getenv("STAGE_DB_PASSWORD")
        self.DB_HOST = os.getenv("STAGE_DB_HOST")
        self.DB_PORT = os.getenv("STAGE_DB_PORT")
        self.DB_NAME = os.getenv("STAGE_DB_NAME", "stage_db") # For Postgres, this is just the DB name
        if not self.DB_PORT: # Default ports if not set
            if self.DB_TYPE == "POSTGRES": self.DB_PORT = "5432"
            elif self.DB_TYPE == "REDSHIFT": self.DB_PORT = "5439"

        # Elasticsearch Staging Config
        self.ES_HOST = os.getenv("ES_HOST")
        self.ES_PORT = int(os.getenv("ES_PORT", "9200")) if os.getenv("ES_PORT") else None # Retained default for staging ES_PORT
        self.ES_SCHEME = os.getenv("STAGE_ES_SCHEME", "http")
        self.ES_USER = os.getenv("STAGE_ES_USER")
        self.ES_PASSWORD = os.getenv("STAGE_ES_PASSWORD")
        self.ES_TIMEOUT = int(os.getenv("STAGE_ES_TIMEOUT", "60"))
        self.ES_API_KEY = os.getenv("ES_API_KEY")
        super().__init__()

class ProductionConfig(BaseConfig):
    def __init__(self):
        self.DB_TYPE = os.getenv("PROD_DB_TYPE", "POSTGRES").upper()
        self.DB_USER = os.getenv("PROD_DB_USER")
        self.DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
        self.DB_HOST = os.getenv("PROD_DB_HOST")
        self.DB_PORT = os.getenv("PROD_DB_PORT")
        self.DB_NAME = os.getenv("PROD_DB_NAME", "prod_db") # For Postgres, this is just the DB name
        if not self.DB_PORT: # Default ports if not set
            if self.DB_TYPE == "POSTGRES": self.DB_PORT = "5432"
            elif self.DB_TYPE == "REDSHIFT": self.DB_PORT = "5439"

        # Elasticsearch Production Config
        self.ES_HOST = os.getenv("ES_HOST")
        self.ES_PORT = int(os.getenv("ES_PORT")) if os.getenv("ES_PORT") else None
        self.ES_SCHEME = os.getenv("PROD_ES_SCHEME", "https") # Default to https for prod
        self.ES_USER = os.getenv("PROD_ES_USER")
        self.ES_PASSWORD = os.getenv("PROD_ES_PASSWORD")
        self.ES_TIMEOUT = int(os.getenv("PROD_ES_TIMEOUT", "60"))
        self.ES_API_KEY = os.getenv("ES_API_KEY")
        super().__init__()

def get_app_config() -> BaseConfig:
    # Specify the absolute path to your .env file
    dotenv_path = Path("/Users/marco/data-engineering/data_engineering/.env")

    # Load the .env file.
    # override=True means variables from .env will overwrite existing system environment variables.
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=True)
        logger.info(f"Loaded environment variables from: {dotenv_path}")
    else:
        logger.warning(f".env file not found at: {dotenv_path}. Using system environment variables or defaults.")

    env = os.getenv("APP_ENV", "DEVELOPMENT").upper()
    logger.info(f"APP_ENV environment variable is set to: {env}")
    
    config_instance: BaseConfig
    
    if env == "DEVELOPMENT":
        config_instance = DevelopmentConfig()
        logger.info(f"Loading DEVELOPMENT configuration (DevelopmentConfig).")
    elif env == "TESTING":
        config_instance = TestingConfig()
        logger.info(f"Loading TESTING configuration (TestingConfig).")
    elif env == "STAGING":
        config_instance = StagingConfig()
        logger.info(f"Loading STAGING configuration (StagingConfig).")
    elif env == "PRODUCTION":
        config_instance = ProductionConfig()
        logger.info(f"Loading PRODUCTION configuration (ProductionConfig).")
    else:
        logger.warning(f"Unknown APP_ENV '{env}'. Defaulting to DevelopmentConfig.")
        config_instance = DevelopmentConfig()
        logger.info(f"Loading DEVELOPMENT configuration (DevelopmentConfig) due to unknown APP_ENV.")
        
    return config_instance