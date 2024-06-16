import json
import jsonlines

path_list = []

for path in path_list:
    gold_list = []
    if "cot" in path:
        target = path.split("\\")[-1].replace(".jsonl", ".json").replace("_cot", "")
    else:
        target = path.split("\\")[-1].replace(".jsonl", ".json")
    with open(f"ori_data\\{target}", "r", encoding="utf-8") as f:
        gold_list = json.load(f)
    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            if "cot" in path:
                if "正确的句子是：" in line["predict"] and line["predict"].startswith(
                    "该句子"
                ):
                    out_list = (
                        line["predict"]
                        .replace("正确的句子是：", "\n")
                        .replace("该句子", "\n")
                        .split("\n")
                    )
                    if "" in out_list:
                        out_list.remove("")
                    out = [out_list[1], ""]
                elif "正确的句子是:" in line["predict"] and line["predict"].startswith(
                    "该句子"
                ):
                    out_list = (
                        line["predict"]
                        .replace("正确的句子是:", "\n")
                        .replace("该句子", "\n")
                        .split("\n")
                    )
                    if "" in out_list:
                        out_list.remove("")
                    out = [out_list[1], ""]
                predict_list.append(out)
            else:
                pre = (
                    line["predict"]
                    .replace("正确的句子：", "\n")
                    .replace("正确的句子:", "\n")
                    .split("\n")
                )
                if "" in pre:
                    pre.remove("")
                predict_list.append(pre)

    with open(
        path.replace(".jsonl", ".txt").replace("_cot", ""), "w", encoding="utf-8"
    ) as f:
        for i in range(len(gold_list)):
            s = f"{i+1}\t{gold_list[i]['input']}"
            pre = predict_list[i]
            s += f"\t{pre[0]}\n"
            f.write(s)
