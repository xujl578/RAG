from typing import TypedDict, Any
import copy

class ImportGraphState(TypedDict):
    #任务标识
    task_id: str

    #输入文件和输出文件
    local_file_path: str
    local_dir: str

    #标记文件类型
    is_md_read_enabled: bool
    is_pdf_read_enabled: bool

    #存储对应类型的文件地址
    md_path: str
    pdf_path: str

    #存储数据内容
    md_content: Any
    item_name: str
    file_title: str

    #切片后的数据
    chunks:list[dict[str,Any]]
    embeddings_content:list[dict[str,Any]]

#定义对象模板,赋予少量默认值
default_state: ImportGraphState = {
    "task_id": "",
    "local_file_path": "",
    "local_dir": "",
    "is_md_read_enabled": False,
    "is_pdf_read_enabled": False,
    "md_path": "",
    "pdf_path": "",
    "md_content": "",
    "item_name": "",
    "file_title": "",
    "chunks": [],
    "embeddings_content": []
}

#提供两个快速创建对象的方法
def create_default_state(**kwargs)->ImportGraphState:
    new_state: ImportGraphState = copy.deepcopy(default_state)
    new_state.update(kwargs)
    return new_state

#快速获取模板对象
def get_default_state()->ImportGraphState:
    new_state: ImportGraphState = copy.deepcopy(default_state)
    return new_state

