from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'app.db'}"

#configuración JWT
SECRET_KEY = "4daa5ddf06935dd4adfa01ee5c97d8ed"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60