# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from middleware.text_process import process

load_dotenv()
app = FastAPI(title="小说转剧本接口")
MAX_CHARS = int(os.getenv("MAX_CHARS", 8000))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # 前端地址，*代表全部
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求体模型
class ConvertReq(BaseModel):
    text: str
    api_key: str | None = None
    api_url: str | None = None
    model_name: str | None = None

@app.post("/api/convert")
def convert_book(req: ConvertReq):
    try:
        origin_list, yaml_list = process(
            req.text,
            MAX_CHARS,
            req.api_key,
            req.api_url,
            req.model_name
        )
        return {
            "origin_chunks": origin_list,
            "yaml_chunks": yaml_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))