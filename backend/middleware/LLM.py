import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
model = os.getenv("LLM_MODEL")

# 读取提示词+Schema
def load_prompt():
    with open("./middleware/sys_promot.txt", "r", encoding="utf-8") as f1:
        base = f1.read()
    with open("./middleware/script_schema.txt", "r", encoding="utf-8") as f2:
        schema = f2.read()

    full_sys = base + "\n固定YAML格式如下：\n" + schema
    return full_sys

# 调用ai函数
def request_llm(user_content: str, in_key=None, in_url=None, in_model=None) -> str:
    SYS_CONTENT = load_prompt()
    use_key = in_key if in_key else api_key
    use_url = in_url if in_url else api_url
    use_model = in_model if in_model else model

    headers = {
        "Authorization": f"Bearer {use_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": use_model,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system", "content": SYS_CONTENT
            },
            {
                "role": "user", "content": user_content
            }
        ]
    }
    try:
        resp = requests.post(use_url, json=body, headers=headers, timeout=60)
        resp.raise_for_status()
        res_json = resp.json()
        raw = res_json["choices"][0]["message"]["content"]
        return raw

    except requests.exceptions.Timeout:
        raise Exception("LLM接口请求超时，请重试")
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 401:
            raise Exception("API密钥错误或权限失效")
        elif resp.status_code == 402:
            raise Exception("账号余额不足/额度已耗尽")
        elif resp.status_code == 429:
            raise Exception("接口调用频率超限，请稍后再试")
        else:
            raise Exception(f"接口异常：{str(e)}")
    except requests.exceptions.ConnectionError:
        raise Exception("无法连接大模型接口，检查网络与接口地址")
    except KeyError:
        raise Exception("AI返回数据格式异常，缺少choices字段")
    except Exception as e:
        raise Exception(f"未知异常：{str(e)}")

