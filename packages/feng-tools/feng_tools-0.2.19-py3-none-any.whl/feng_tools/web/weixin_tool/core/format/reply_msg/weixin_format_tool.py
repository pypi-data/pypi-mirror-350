from pydantic.main import BaseModel


def format_xml_msg(model: BaseModel):
    """使用xml文件格式化消息"""
    xml_file = getattr(model, '_xml_file')
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_format = f.read()
        return xml_format.format(**model.dict())
