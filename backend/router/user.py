from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from middleware.JWT import user_dict, hash_pwd, verify_pwd, create_token, get_login_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# 表单模型
class RegForm(BaseModel):
    username: str
    password: str

class LoginForm(BaseModel):
    username: str
    password: str

# 全局鉴权依赖（给转换接口用）
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_login_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="未登录或账号已在别处登录")
    return user

# 注册
@router.post("/register")
def register(data: RegForm):
    if data.username in user_dict:
        raise HTTPException(status_code=400, detail="账号已被注册")
    user_dict[data.username] = hash_pwd(data.password)
    return {"msg": "注册成功"}

# 登录
@router.post("/login")
def login(data: LoginForm):
    if data.username not in user_dict:
        raise HTTPException(status_code=400, detail="账号不存在")
    if not verify_pwd(data.password, user_dict[data.username]):
        raise HTTPException(status_code=400, detail="密码错误")
    token = create_token(data.username)
    return {"token": token}