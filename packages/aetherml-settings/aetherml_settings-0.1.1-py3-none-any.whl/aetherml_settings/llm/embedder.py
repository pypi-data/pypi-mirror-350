import ollama
import logging
from typing import List, Optional, Dict
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed


logger = logging.getLogger(__name__)

class NomicTextEmbedder:
    """
    A class to generate text embeddings using a model served by Ollama,
    specifically targeting models like 'nomic-embed-text'.
    """
    def __init__(self, model_name: str = "nomic-embed-text", ollama_host: Optional[str] = None):
        """
        Initializes the NomicTextEmbedder.
        Args:
            model_name: The name of the embedding model in Ollama (e.g., 'nomic-embed-text').
            ollama_host: Optional URL of the Ollama host. 
                         Defaults to 'http://localhost:11434' if None.
        """
        self.model_name = model_name
        self.ollama_host = ollama_host if ollama_host is not None else "http://localhost:11434"
        logger.info(f"NomicTextEmbedder initialized with model: {self.model_name}, Ollama host: {self.ollama_host}")
    
    def _get_single_embedding(self, text: str, attempt_info: str = "") -> Optional[List[float]]:
        """
        Generate embedding for a single given text using the specified model.
        Internal method, called by the parallel version.

        Args:
            text: The text to generate embeddings for.
            attempt_info: Information about the attempt for logging (e.g., item number).

        Returns:
            List[float]: A list of floats representing the embeddings, or None if an error occurs.
        """
        if not text or not text.strip():
            logger.warning(f"Input text is empty or whitespace only {attempt_info}. Returning None.")
            return None
        
        # Ensure ollama_host has a scheme
        url_to_use = self.ollama_host
        if not url_to_use.startswith(("http://", "https://")):
            url_to_use = "http://" + url_to_use # Default to http if no scheme
        
        api_endpoint = f"{url_to_use.rstrip('/')}/api/embeddings"
        
        payload = {
            "model": self.model_name,
            "prompt": text # Ollama API uses "prompt" for embeddings
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            logger.debug(f"Requesting embedding {attempt_info} from {api_endpoint} for model {self.model_name}")
            response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30) # Added timeout
            response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
            
            data = response.json()
            embedding = data.get("embedding") # Ollama direct /api/embeddings returns { "embedding": [...] }
            
            if embedding and isinstance(embedding, list):
                logger.debug(f"Successfully got embedding {attempt_info}. Length: {len(embedding)}")
                return embedding
            else:
                logger.error(f"Failed to retrieve a valid embedding structure {attempt_info} from Ollama. Response: {data}")
                return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error generating embedding {attempt_info}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error generating embedding {attempt_info}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error generating embedding {attempt_info} for text '{text[:50]}...': {e}")
        return None

    def get_embeddings_parallel(self, texts: List[str], max_workers: Optional[int] = None) -> List[Optional[List[float]]]:
        """
        Generates embeddings for a list of texts in parallel.

        Args:
            texts: A list of input texts to embed.
            max_workers: The maximum number of threads to use. 
                         If None, it defaults to a number suitable for the system's processors.

        Returns:
            A list of embeddings (each possibly None if an error occurred for that text),
            in the same order as the input texts.
        """
        if not texts:
            logger.warning("Input list of texts for parallel embedding is empty.")
            return []

        results: List[Optional[List[float]]] = [None] * len(texts)
        # Using a dictionary to map future to index to ensure correct order
        future_to_index: Dict[object, int] = {}

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i, text_item in enumerate(texts):
                attempt_info = f"(item {i+1}/{len(texts)})"
                future = executor.submit(self._get_single_embedding, text_item, attempt_info)
                future_to_index[future] = i
            
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    logger.error(f"Error processing result for text item {index+1}: {e}")
                    results[index] = None # Ensure it's None on future.result() error
        
        logger.info(f"Parallel embedding processing complete for {len(texts)} texts.")
        return results


# Example Usage (optional, for testing purposes):
# if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    # logger.info("Testing NomicTextEmbedder...")

    # # Ensure Ollama is running and the 'nomic-embed-text' model is available.
    # # You might need to run `ollama pull nomic-embed-text` first.
    
    # # Initialize embedder (ensure OLLAMA_HOST env var is set or Ollama runs on default http://localhost:11434)
    # # Or pass host directly: embedder = NomicTextEmbedder(ollama_host="http://your-ollama-host:11434")
    # embedder = NomicTextEmbedder(model_name="nomic-embed-text") # Uses default host http://localhost:11434

    # # Test 1: Single embedding (using the internal method for direct testing if needed)
    # sample_text_1 = "The quick brown fox jumps over the lazy dog."
    # logger.info(f"Attempting single embedding for: '{sample_text_1}'")
    # embedding_1 = embedder._get_single_embedding(sample_text_1, "(Test Single)")
    # if embedding_1:
    #     logger.info(f"Successfully got single embedding (first 5 dims): {embedding_1[:5]}..., Length: {len(embedding_1)}")
    # else:
    #     logger.error("Failed to get single embedding.")
    # print("-"*50)

    # # Test 2: Parallel embeddings
    # sample_texts_batch = [
    #     "First document for batch processing.",
    #     "Second document, slightly different.",
    #     "", # Empty string test
    #     "    ", # Whitespace only test
    #     "Yet another document to see how batching works.",
    #     "This is a moderately long sentence to test performance.",
    #     "Short one.",
    #     "Another one to make it up to eight for testing with, say, 4 workers."
    # ]
    # logger.info(f"Attempting parallel embeddings for {len(sample_texts_batch)} texts...")
    # batch_embeddings = embedder.get_embeddings_parallel(sample_texts_batch, max_workers=4)
    
    # if batch_embeddings:
    #     logger.info(f"Received {len(batch_embeddings)} results from parallel processing.")
    #     successful_count = 0
    #     for i, emb in enumerate(batch_embeddings):
    #         original_text_snip = f"'{sample_texts_batch[i][:30]}...'"
    #         if emb:
    #             logger.info(f"Parallel item {i+1} ({original_text_snip}) (first 5 dims): {emb[:5]}..., Length: {len(emb)}")
    #             successful_count += 1
    #         else:
    #             logger.warning(f"Parallel item {i+1} ({original_text_snip}) failed or returned None.")
    #     logger.info(f"Successfully processed {successful_count}/{len(sample_texts_batch)} items in parallel.")
    # else:
    #     logger.error("Parallel embedding failed to return results or returned an empty list.")
    # print("-"*50)

    # # Test 3: Parallel with fewer texts than workers
    # short_batch = ["Hello world", "Test again"]
    # logger.info(f"Attempting parallel embeddings for {len(short_batch)} texts (fewer than workers)...")
    # short_batch_embeddings = embedder.get_embeddings_parallel(short_batch, max_workers=4)
    # if short_batch_embeddings:
    #     logger.info(f"Received {len(short_batch_embeddings)} results for short batch.")
    #     for i, emb in enumerate(short_batch_embeddings):
    #         if emb:
    #             logger.info(f"Short batch item {i+1} (first 5 dims): {emb[:5]}..., Length: {len(emb)}")
    # print("-"*50)

    # # Test 4: Empty list input for parallel
    # logger.info("Attempting parallel embeddings for an empty list...")
    # empty_results = embedder.get_embeddings_parallel([])
    # logger.info(f"Results for empty list: {empty_results} (Expected: [])")

