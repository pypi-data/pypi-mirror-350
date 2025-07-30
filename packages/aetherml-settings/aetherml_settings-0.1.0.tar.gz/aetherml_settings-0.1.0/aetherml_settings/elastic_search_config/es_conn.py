from elasticsearch import Elasticsearch, exceptions
from aetherml_settings.configs import get_app_config, BaseConfig # Assuming get_app_config returns a BaseConfig or subclass
import logging

logger = logging.getLogger(__name__)

class ElasticsearchConnection:
    """
    Manages the connection to Elasticsearch using configurations
    loaded by get_app_config.
    """
    def __init__(self):
        self.config: BaseConfig = get_app_config()
        self.client: Elasticsearch | None = None
        self._connect()

    def _connect(self):
        """Initializes the Elasticsearch client."""
        if not self.config.ES_HOST or not self.config.ES_PORT:
            logger.error("Elasticsearch host or port not configured. Cannot connect.")
            self.client = None
            return

        elastic_client_endpoint = f"{self.config.ES_HOST}:{self.config.ES_PORT}"
        logger.info(f"Connecting to Elasticsearch at {elastic_client_endpoint}")
        logger.info(f"API Key: {self.config.ES_API_KEY}")
        try:
            self.client = Elasticsearch(
                elastic_client_endpoint,
                api_key=self.config.ES_API_KEY,
                verify_certs=True,
                timeout=self.config.ES_TIMEOUT,
                retry_on_timeout=True,
                max_retries=3
            )
            if not self.client.ping():
                raise exceptions.ConnectionError("Could not connect to Elasticsearch")
            logger.info(f"Successfully connected to Elasticsearch at {self.config.ES_HOST}:{self.config.ES_PORT}")
        except exceptions.AuthenticationException as e:
            logger.error(f"Elasticsearch authentication failed: {e}")
            self.client = None
        except exceptions.ConnectionError as e:
            logger.error(f"Elasticsearch connection failed: {e}")
            self.client = None
        except Exception as e:
            logger.error(f"An unexpected error occurred during Elasticsearch connection: {e}")
            self.client = None

    def get_client(self) -> Elasticsearch | None:
        """Returns the Elasticsearch client instance."""
        if not self.client:
            logger.warning("Elasticsearch client is not initialized. Attempting to reconnect.")
            self._connect() # Try to reconnect if client is None
        return self.client

    def ping(self) -> bool:
        """Checks if the Elasticsearch server is reachable."""
        if self.client:
            try:
                return self.client.ping()
            except exceptions.ConnectionError:
                logger.warning("Ping to Elasticsearch failed - ConnectionError")
                return False
            except Exception as e:
                logger.warning(f"Ping to Elasticsearch failed with an unexpected error: {e}")
                return False
        return False

# # Example usage (optional, for testing purposes):
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     logger.info("Attempting to create Elasticsearch connection...")
#     es_connection = ElasticsearchConnection()
#     if es_connection.get_client():
#         logger.info("Elasticsearch client obtained.")
#         if es_connection.ping():
#             logger.info("Successfully pinged Elasticsearch.")
#         else:
#             logger.error("Failed to ping Elasticsearch after obtaining client.")
#     else:
#         logger.error("Failed to obtain Elasticsearch client.")
