from middleware.LLM import request_llm
from middleware.distinct import split_content

def process(full_text: str, max_limit: int, in_key=None, in_url=None, in_model=None):
    chunk_list = split_content(full_text, max_limit)
    yaml_result_list = []
    for chunk in chunk_list:
        yaml_str = request_llm(chunk, in_key, in_url, in_model)
        yaml_result_list.append(yaml_str)
    return chunk_list, yaml_result_list