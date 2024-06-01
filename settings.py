import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import logging
# Load .env file
load_dotenv('.env')


# Настройка логирования
logging.basicConfig(level=logging.DEBUG)  # Установите уровень логирования на DEBUG
logger = logging.getLogger(__name__)  # Получите логгер для текущего модуля

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Настройка OAuth2PasswordBearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

# для токена
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
