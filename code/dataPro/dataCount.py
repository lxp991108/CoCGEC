import json
from tqdm import tqdm

type_switch = {
    "IWO": "语序不当",
    "IWC": "搭配不当",
    "CM": "成分残缺",
    "CR": "成分赘余",
    "SC": "结构混乱",
    "ILL": "不合逻辑",
    "AM": "表意不明",
}


def get_key(dict, value):
    for k, v in dict.items():
        if v == value:
            return k
    return "NE"


with open(r"ori_data\FCGEC_train_auto.json", "r", encoding="utf-8") as file:
    data_list = json.load(file)

dict_type = {}

for line in tqdm(data_list):
    if line["type"] not in dict_type:
        dict_type[line["type"]] = {"num": 1, "ref": len(line["output"])}
    else:
        dict_type[line["type"]]["num"] += 1
        dict_type[line["type"]]["ref"] += len(line["output"])

sum = {"num": 0, "ref": 0}
for k, v in dict_type.items():
    if k != "没有语病":
        sum["num"] += v["num"]
        sum["ref"] += v["ref"]
    v["ref"] = v["ref"] / v["num"]
    print(f'{get_key(type_switch, k)}:\tnum:{v["num"]}\tref:{v["ref"]:.2f}')
print(f"SUM:\tnum:{sum['num']}\tref:{sum['ref']/sum['num']:.2f}")
