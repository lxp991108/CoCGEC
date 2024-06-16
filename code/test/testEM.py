import jsonlines
import json


def testEM(path):
    label_list = []
    target = path.split("\\")[-1].replace(".jsonl", ".json")
    with open(f"ori_data\\{target}", "r", encoding="utf-8") as f:
        label_list = json.load(f)

    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            pre = line["predict"]
            predict_list.append(pre)

    emNum = 0
    for i in range(len(label_list)):
        out_list = (
            predict_list[i]
            .replace("正确的句子：", "\n")
            .replace("正确的句子:", "\n")
            .split("\n")
        )
        if "" in out_list:
            out_list.remove("")
        if out_list[0] in label_list[i]["output"]:
            emNum += 1
    print(f"{path}\t{emNum}\t{(emNum/len(label_list))*100:.2f}")


def testCoTEM(path):
    label_list = []
    target = path.split("\\")[-1].replace(".jsonl", ".json").replace("cot_", "")
    with open(f"ori_data\\{target}", "r", encoding="utf-8") as f:
        label_list = json.load(f)

    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            pre = line["predict"]
            predict_list.append(pre)

    emNum = 0
    for i in range(len(label_list)):
        if "正确的句子是：" in predict_list[i] and predict_list[i].startswith("该句子"):
            out_list = (
                predict_list[i]
                .replace("正确的句子是：", "\n")
                .replace("该句子", "\n")
                .split("\n")
            )
            if "" in out_list:
                out_list.remove("")
            out = out_list[1]
        elif "正确的句子是:" in predict_list[i] and predict_list[i].startswith(
            "该句子"
        ):
            out_list = (
                predict_list[i]
                .replace("正确的句子是:", "\n")
                .replace("该句子", "\n")
                .split("\n")
            )
            if "" in out_list:
                out_list.remove("")
            out = out_list[1]
        else:
            print(predict_list[i])
        if out in label_list[i]["output"]:
            emNum += 1
    print(f"{path}\t{emNum}\t{(emNum/len(label_list))*100:.2f}")


def testNeEM(path):
    label_list = []
    target = path.split("\\")[-1].replace(".jsonl", ".json")
    with open(f"ori_data\\{target}", "r", encoding="utf-8") as f:
        label_list = json.load(f)
    error_num = 0
    predict_list = []
    with open(path, "r", encoding="utf-8") as f:
        for line in jsonlines.Reader(f):
            pre = line["predict"]
            predict_list.append(pre)

    emNum = 0
    for i in range(len(label_list)):
        if label_list[i]["flag"] == 1:
            error_num += 1
            out_list = (
                predict_list[i]
                .replace("正确的句子：", "\n")
                .replace("正确的句子:", "\n")
                .split("\n")
            )
            if "" in out_list:
                out_list.remove("")
            if out_list[0] in label_list[i]["output"]:
                emNum += 1
    print(f"{path}\t{emNum}\t{(emNum/error_num)*100:.2f}")


test_path = []

# for path in test_path:
#     testNeEM(path)
# print("------------------")
for path in test_path:
    if "cot" in path:
        testCoTEM(path)
    else:
        testEM(path)
