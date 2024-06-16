import json
import jsonlines
import random

path_list = []


def pro(path):
    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            predict_list.append(line)

    output_list = []

    # target = path.split("\\")[-1].replace(".jsonl", ".json")
    # with open(f"ori_data\\{target}", "r", encoding="utf-8") as f:
    #     gold_list = json.load(f)
    # for i in range(len(gold_list)):
    #     data = {}
    #     data["input"] = gold_list[i]["input"]
    #     data["output"] = predict_list[i]["predict"]
    #     output_list.append(data)

    for line in predict_list:
        data = {}
        data["input"] = line["input"]
        if (
            "没有语病" in line["output"]
            or "无错误" in line["output"]
            or "无语法错误" in line["output"]
            or "原句正确" in line["output"]
            or "没有语法错误" in line["output"]
            or "没有错误" in line["output"]
            or "没有语法错误" in line["output"]
            or "无需修改" in line["output"]
            or "无需改正" in line["output"]
            or "无需改动" in line["output"]
            or "这个句子是正确的" in line["output"]
            or "原句⼦是正确的" in line["output"]
            or "未发现语法错误" in line["output"]
            or "未发现错误" in line["output"]
            or "输入的句子是正确的" in line["output"]
            or "输出原句" in line["output"]
            or "不需要做任何改动" in line["output"]
            or "正确" == line["output"]
            or ("无需" in line["output"] and "无需" not in line["input"])
            or ("正确的" in line["output"] and "正确的" not in line["input"])
        ):
            data["output"] = data["input"]
        else:
            o = (
                line["output"]
                .replace("Assistant:", "\n")
                .replace("Human:", "\n")
                .replace("修正后的句子：", "\n")
                .replace("改正后的句子：", "\n")
                .replace("输出：", "\n")
                .replace("以下是纠正后的句子：", "\n")
                .replace("正确句⼦：", "\n")
                .replace(" ", "")
                .split("\n")
            )
            for i in o:
                if i != "":
                    data["output"] = i
                    break
        output_list.append(data)

    with open(path, "w", encoding="utf-8") as f:
        for line in output_list:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")


def test(path):
    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            predict_list.append(line)

    random.shuffle(predict_list)
    count = 0
    for line in predict_list:
        if abs(len(line["input"]) - len(line["output"])) > 10 or "\n" in line["output"]:
            count += 1
            print(line)
        if count > 20:
            break


def toEva(path):
    data_list = []
    type_list = ["IWO", "IWC", "CM", "CR", "SC", "ILL", "AM"]
    with open(r"ori_data\FCGEC_test.json", "r", encoding="utf-8") as f:
        data_list = json.load(f)
    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            predict_list.append(line)
    if "FCGEC_test" in path:
        output_dict = {}
        for i in range(len(data_list)):
            flag = 0
            if data_list[i]["input"] != predict_list[i]["output"]:
                flag = 1
            if flag == 0:
                output_dict[data_list[i]["id"]] = {
                    "error_flag": flag,
                    "error_type": "*",
                    "correction": predict_list[i]["output"],
                }
            else:
                output_dict[data_list[i]["id"]] = {
                    "error_flag": flag,
                    "error_type": random.choice(type_list),
                    "correction": predict_list[i]["output"],
                }
            with open(
                path.replace("FCGEC_test.jsonl", "predict.json"), "w", encoding="utf-8"
            ) as f:
                f.write(json.dumps(output_dict, indent=2, ensure_ascii=False))
    else:
        with open(path.replace(".jsonl", ".txt"), "w", encoding="utf-8") as f:
            for i in range(len(predict_list)):
                s = f"{i+1}\t{predict_list[i]['input']}"
                s += f"\t{predict_list[i]['output']}\n"
                f.write(s)


for path in path_list:
    print(path)
    toEva(path)
