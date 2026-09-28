import os

# Settings require DATABASE_URL; provide a dummy one so tests run without a .env file.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
