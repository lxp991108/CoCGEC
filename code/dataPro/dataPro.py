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

data_path = r"ori_data/FCGEC_test_pro.json"
data_list = []
with open(data_path, "r", encoding="utf-8") as f:
    data_list = json.load(f)

pro_list = []
# 标点、类型转换
for line in tqdm(data_list):
    data = {}
    data["input"] = (
        line["input"]
        .replace(",", "，")
        .replace("?", "？")
        .replace("!", "！")
        .replace(":", "：")
        .replace(";", "；")
    )
    out_list = []
    for out in line["output"]:
        out = (
            out.replace(",", "，")
            .replace("?", "？")
            .replace("!", "！")
            .replace(":", "：")
            .replace(";", "；")
        )
        if out not in out_list and out != data["input"]:
            out_list.append(out)
    data["output"] = out_list
    if line["type"] == "没有语病":
        data["type"] = ["没有语病"]
        data["output"].append(data["input"])
    else:
        t = line["type"].split(";")
        data["type"] = [type_switch[i] for i in t]
    pro_list.append(data)
print("标点、类型转换完成。")

# 去重
input_list = []
for line in tqdm(data_list):
    if line["input"] not in input_list:
        input_list.append(line["input"])
    else:
        print(line["input"])
print("去重完成。")

# 写入
with open(data_path.replace("_pro.json", ".json"), "w", encoding="utf-8") as f:
    f.write(json.dumps(pro_list, indent=2, ensure_ascii=False))
