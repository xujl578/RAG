from app.process.import_.agent.state import ImportGraphState
from app.shared.runtime.logger import logger
from pathlib import Path

def  resolve_input_file(state: ImportGraphState) -> ImportGraphState:
    """
    入口识别服务：
    1. 校验 local_file_path
    2. 识别文件类型（PDF / Markdown）
    3. 回写 is_pdf_read_enabled / is_md_read_enabled
    4. 回写 pdf_path / md_path / file_title
    """
    # 1. 获取文件本地路径
    local_file_path = state.get("local_file_path")
    # 非空校验
    if not local_file_path:
        logger.error(f"local_file_path 不存在")
        raise ValueError("local_file_path 不存在")

    # 2. 文件类型识别
    if local_file_path.lower().endswith(".md"):
        state["is_md_read_enabled"] = True
        state["is_pdf_read_enabled"] = False
        state["md_path"] = local_file_path
    elif local_file_path.lower().endswith(".pdf"):
        state["is_pdf_read_enabled"] = True
        state["is_md_read_enabled"] = False
        state["pdf_path"] = local_file_path
    else:
        # 3. 其他文件类型，暂不处理
        return state

    # 4. 将地址转化为Path对象
    local_file_obj: Path = Path(local_file_path)
    file_title:str = local_file_obj.stem
    #更新state
    state["file_title"] = file_title
    return state