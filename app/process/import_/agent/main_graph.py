from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from app.process.import_.agent.state import ImportGraphState
from app.process.import_.agent.nodes.node_entry import node_entry
from app.process.import_.agent.nodes.node_pdf_to_md import node_pdf_to_md
from app.process.import_.agent.nodes.node_md_img import node_md_img
from app.process.import_.agent.nodes.node_document_split import node_document_split
from app.process.import_.agent.nodes.node_item_name_recognition import node_item_name_recognition
from app.process.import_.agent.nodes.node_bge_embedding import node_bge_embedding
from app.process.import_.agent.nodes.node_import_milvus import node_import_milvus
from app.shared.runtime.logger import  logger

#创建图的对象
import_builder = StateGraph(state_schema=ImportGraphState)

#添加节点
import_builder.add_node("node_entry", node_entry)
import_builder.add_node("node_pdf_to_md", node_pdf_to_md)
import_builder.add_node("node_md_img", node_md_img)
import_builder.add_node("node_document_split", node_document_split)
import_builder.add_node("node_item_name_recognition", node_item_name_recognition)
import_builder.add_node("node_bge_embedding", node_bge_embedding)
import_builder.add_node("node_import_milvus", node_import_milvus)

#添加边
import_builder.set_entry_point("node_entry")

#添加一个路由函数
def after_node_entry(state: ImportGraphState)->str:
    if state.get('is_md_read_enabled'):
        #打印日志
        logger.info(f"传入的是md文件,md_path:{state.get('md_path')},后续跳转到node_md_img")
        return "node_md_img"
    elif state.get('is_pdf_read_enabled'):
        logger.info(f"传入的是pdf文件,pdf_path:{state.get('pdf_path')},后续跳转到node_pdf_to_md")
        return "node_pdf_to_md"
    else:
        logger.warning(f"当前项目只支持pdf和md格式,local_file_path:{state.get('local_file_path')},后续跳转到END节点!")
        return END

import_builder.add_conditional_edges("node_entry", after_node_entry,{"node_md_img":"node_md_img",
                                                                    "node_pdf_to_md":"node_pdf_to_md",
                                                                    END:END
                                                                    })

import_builder.add_edge("node_pdf_to_md","node_md_img")
import_builder.add_edge("node_md_img","node_document_split")
import_builder.add_edge("node_document_split","node_item_name_recognition")
import_builder.add_edge("node_item_name_recognition","node_bge_embedding")
import_builder.add_edge("node_bge_embedding","node_import_milvus")
import_builder.add_edge("node_import_milvus", END)

import_graph_app = import_builder.compile()



