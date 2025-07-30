from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus # For URL encoding passwords
from sqlalchemy.ext.declarative import declarative_base
from aetherml_settings.configs import get_app_config
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


current_config = get_app_config()
SQLALCHEMY_DATABASE_URL = current_config.SQLALCHEMY_DATABASE_URL

logger.info(f"Database Type: {current_config.DB_TYPE}")
logger.info(f"SQLAlchemy Database URL: {SQLALCHEMY_DATABASE_URL}")

engine_args = {}
if current_config.DB_TYPE == "REDSHIFT":
    # engine_args['connect_args'] = {'sslmode': 'prefer'} # Example Redshift specific arg
    pass

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# IMPORTANT REMINDER:
# Ensure Base (declarative_base()) is defined in a central model file 
# (e.g., data_engineering/model/entity/base.py) and all your SQLAlchemy models import it.