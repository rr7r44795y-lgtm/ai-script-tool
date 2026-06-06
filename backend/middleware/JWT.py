import os
from datetime import datetime, timedelta
import jwt
from dateutil.tz import UTC
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_EXPIRE = timedelta(hours=24)
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_dict = {}
valid_token = {}

# 密码加密
def hash_pwd(pwd: str):
    return pwd_ctx.hash(pwd)

def verify_pwd(raw_pwd: str, hash_pwd: str):
    return pwd_ctx.verify(raw_pwd, hash_pwd)

# 生成token
def create_token(username: str):
    expire = datetime.now(UTC) + ACCESS_EXPIRE
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    valid_token[username] = token
    return token

# 解析token + 校验是否是当前有效令牌
def get_login_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username in valid_token and valid_token[username] == token:
            return username
        return None
    except Exception:
        return None