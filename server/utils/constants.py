import os


CONN_STRING = os.environ.get("DB_CONNECTION_STRING", "mongodb://localhost:27017")
DB_NAME = "local-assistant"
