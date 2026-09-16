"""Shared labels and prompts used by the paper experiments."""

ERROR_TYPE_NAMES = {
    "IWO": "语序不当",
    "IWC": "搭配不当",
    "CM": "成分残缺",
    "CR": "成分赘余",
    "SC": "结构混乱",
    "ILL": "不合逻辑",
    "AM": "表意不明",
}

ERROR_TYPE_CODES = {name: code for code, name in ERROR_TYPE_NAMES.items()}

CORRECTION_PROMPT = "纠正下面句子中可能存在的语病并输出正确的句子："
TYPE_PROMPT = "判断下面句子是否含有某种类型的语病错误："
RANGE_PROMPT = "找出下面句子中存在语病的地方："
