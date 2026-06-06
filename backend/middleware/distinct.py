def split_content(full_text: str, max_limit: int) -> list[str]:
    chunks = []
    lines = full_text.splitlines()
    temp = ""

    for line in lines:
        if len(temp + line + "\n") > max_limit and temp:
            chunks.append(temp.strip())
            temp = ""
        temp += line + "\n"
    if temp:
        chunks.append(temp.strip())
    return chunks