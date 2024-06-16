import json
import jsonlines
import random

data_list = []
type_list = ["IWO", "IWC", "CM", "CR", "SC", "ILL", "AM"]
with open(r"ori_data\FCGEC_test.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)


def test_correct(path):
    output_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            if "cot" not in path:
                pre = (
                    line["predict"]
                    .replace("正确的句子：", "\n")
                    .replace("正确的句子:", "\n")
                    .split("\n")
                )
                if "" in pre:
                    pre.remove("")
                pre = pre[0]
                output_list.append(pre)
            else:
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
                    out = out_list[1]
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
                    out = out_list[1]
                output_list.append(out)
    output_dict = {}
    for i in range(len(data_list)):
        flag = 0
        if data_list[i]["input"] != output_list[i]:
            flag = 1
        if flag == 0:
            output_dict[data_list[i]["id"]] = {
                "error_flag": flag,
                "error_type": "*",
                "correction": output_list[i],
            }
        else:
            output_dict[data_list[i]["id"]] = {
                "error_flag": flag,
                "error_type": random.choice(type_list),
                "correction": output_list[i],
            }
    with open(
        path.replace("FCGEC_test.jsonl", "predict.json").replace(
            "FCGEC_cot_test.jsonl", "predict.json"
        ),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(json.dumps(output_dict, indent=2, ensure_ascii=False))


path_list = []
for path in path_list:
    test_correct(path)
