import logging
import os

APP_NAME = os.getenv("APP_NAME", "nsj_embedding_search")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
OPENAI_EMBEDDING_MODEL_LIMIT = int(os.getenv("OPENAI_EMBEDDING_MODEL_LIMIT", "8191"))

CHUNCK_SIZE = int(os.getenv("CHUNCK_SIZE", "256"))
OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE", "128"))

# Configurando o logger
logger = logging.getLogger(APP_NAME)
