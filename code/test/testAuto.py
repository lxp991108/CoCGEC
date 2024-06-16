import json

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
    return "Total"


def normal_leven(str1, str2):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    # 创建矩阵
    matrix = [0 for n in range(len_str1 * len_str2)]
    # 矩阵的第一行
    for i in range(len_str1):
        matrix[i] = i
    # 矩阵的第一列
    for j in range(0, len(matrix), len_str1):
        if j % len_str1 == 0:
            matrix[j] = j // len_str1
    # 根据状态转移方程逐步得到编辑距离
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[j * len_str1 + i] = min(
                matrix[(j - 1) * len_str1 + i] + 1,
                matrix[j * len_str1 + (i - 1)] + 1,
                matrix[(j - 1) * len_str1 + (i - 1)] + cost,
            )

    return matrix[-1]  # 返回矩阵的最后一个值，也就是编辑距离


data_list = []
with open(r"ori_data\FCGEC_train_1500_auto.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)


def test_match(data_list, key):
    count_Dict = {
        "语序不当": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "搭配不当": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "成分残缺": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "成分赘余": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "结构混乱": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "不合逻辑": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "表意不明": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
        "合计": {"exact_match": 0, "min_edit_distance": 0, "number": 0},
    }
    countNum = 0
    for line in data_list:
        if line["flag"] == 1:
            error_type = line["type"]
            count_Dict["合计"]["number"] += 1
            count_Dict[error_type]["number"] += 1
            if line[key] == line["error"]:
                countNum += 1
                count_Dict[error_type]["exact_match"] += 1
                count_Dict["合计"]["exact_match"] += 1
            count_Dict[error_type]["min_edit_distance"] += normal_leven(
                line[key], line["error"]
            )
            count_Dict["合计"]["min_edit_distance"] += normal_leven(
                line[key], line["error"]
            )
    for k, v in count_Dict.items():
        v["min_edit_distance"] = "{:.2f}".format(v["min_edit_distance"] / v["number"])
        v["exact_match"] = "{:.2f}".format(100 * v["exact_match"] / v["number"])
        count_Dict[k] = v
        print(
            f"{get_key(type_switch, k)}:\texact_match:{v['exact_match']}\tmin_edit_distance:{v['min_edit_distance']}"
        )
    print("-----------------------------------")


test_match(data_list, "scope1")
test_match(data_list, "scope2")
test_match(data_list, "scope3")
test_match(data_list, "scope4")
