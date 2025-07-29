"""
pip install transformers -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple/
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from feng_tools.ai.modelscope import model_download_tools

# 从魔搭社区加载NLLB-200模型和分词器
# model_name = "shibing624/nllb200-600m-zh"
# 下载魔搭社区上的NLLB-200模型
model_dir = model_download_tools.download('Kleaner/v5_facebook-nllb-200-distilled-600M')
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

# 语言代码映射
LANGUAGE_CODE_MAP = {
    "中文": "zho_Hans",
    "英语": "eng_Latn",
    "韩语": "kor_Hang"
}


def translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    翻译函数，支持中英韩互译

    Args:
        text: 待翻译的文本
        source_lang: 源语言名称
        target_lang: 目标语言名称

    Returns:
        翻译后的文本
    """
    # 检查语言是否支持
    if source_lang not in LANGUAGE_CODE_MAP or target_lang not in LANGUAGE_CODE_MAP:
        supported_langs = ", ".join(LANGUAGE_CODE_MAP.keys())
        raise ValueError(f"不支持的语言。支持的语言有: {supported_langs}")

    # 设置源语言和目标语言代码
    source_code = LANGUAGE_CODE_MAP[source_lang]
    target_code = LANGUAGE_CODE_MAP[target_lang]

    # 配置tokenizer的源语言
    tokenizer.src_lang = source_code

    # 编码输入文本
    encoded = tokenizer(text, return_tensors="pt")

    # 生成翻译结果 - 修改此处获取语言ID的方式
    target_lang_id = tokenizer.convert_tokens_to_ids([f"__{target_code}__"])[0]
    generated_tokens = model.generate(
        **encoded,
        forced_bos_token_id=target_lang_id,
        max_length=512
    )

    # 解码翻译结果
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translated_text


# 使用示例
if __name__ == "__main__":
    # 示例1: 中文到英文
    chinese_text = "这是一个翻译模型示例。"
    english_text = translate(chinese_text, "中文", "英语")
    print(f"中文 -> 英语: {english_text}")

    # 示例2: 英文到韩语
    english_text = "This is a translation model example."
    korean_text = translate(english_text, "英语", "韩语")
    print(f"英语 -> 韩语: {korean_text}")

    # 示例3: 韩语到中文
    korean_text = "이것은 번역 모델 예시입니다."
    chinese_text = translate(korean_text, "韩语", "中文")
    print(f"韩语 -> 中文: {chinese_text}")