from dotenv import load_dotenv
import os

load_dotenv()

# db config
MONGO_URL = os.environ.get("MONGO_URL")
DB_NAME = os.environ.get("DB_NAME")

# jwt
JWT_SECRET = os.environ.get("JWT_SECRET")

# 10mins
SMS_CODE_EXPIRE_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION_MINUTES = 30