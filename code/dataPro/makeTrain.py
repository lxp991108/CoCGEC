import json
import random
import jsonlines
from tqdm import tqdm

prompt_correct = "纠正下面句子中可能存在的语病并输出正确的句子："
prompt_type = "判断下面句子是否含有某种类型的语病错误："
prompt_scope = "找出下面句子中存在语病的地方："
prompt_cot = "分步骤地检查下面句子中是否存在语病，若存在则纠正并输出正确的句子："
prompt_base = "识别并纠正下列句⼦中可能含有的语法错误并输出正确的句⼦。要求在纠正错误的同时尽可能减少对原句⼦的改动，避免对句⼦结构进⾏不必要的更改或添加。只输出没有语法错误的句⼦，不要添加任何其他解释或说明。如果原句⼦是正确的句⼦，则直接输出原句⼦。输⼊："


def makeTrainTask1():
    data_list = []
    with open(r"ori_data\FCGEC_train_1500_auto.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)
    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\train\task1\correct_1500.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["error"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_0.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope1"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_1.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope2"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_2.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope3"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_3.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope4"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_4.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope1"]}'
            data_instance.append(data)
            if line["scope2"] != line["scope1"]:
                data = {}
                data["instruction"] = prompt_scope
                data["input"] = line["input"]
                data["output"] = f'该句存在语病的地方：{line["scope2"]}'
                data_instance.append(data)
            if line["scope3"] != line["scope1"] and line["scope3"] != line["scope2"]:
                data = {}
                data["instruction"] = prompt_scope
                data["input"] = line["input"]
                data["output"] = f'该句存在语病的地方：{line["scope3"]}'
                data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：#"
            data_instance.append(data)
    with open(r"cgec\train\task1\auto_scope_1+2+3.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def makeTrainTask2():
    data_list = []
    with open(r"ori_data\FCGEC_train_auto.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{line['output'][0]}"
        data_instance.append(data)
    with open(r"cgec\train\task2\correct.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：没有存在语病的地方"
            data_instance.append(data)
    with open(r"cgec\train\task2\scope.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_type
            data["input"] = line["input"]
            data["output"] = f'这句话中含有的语病错误类型：{line["type"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_type
            data["input"] = line["input"]
            data["output"] = f"这句话中含有的语病错误类型：无"
            data_instance.append(data)
    with open(r"cgec\train\task2\type.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def makeTrainTask3():
    trainShuffle()
    data_list = []
    with open(r"ori_data\FCGEC_train_shuffle.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{line['output'][0]}"
        data_instance.append(data)
    with open(r"cgec\train\task3\correct_shuffle.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f'该句存在语病的地方：{line["scope"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_scope
            data["input"] = line["input"]
            data["output"] = f"该句存在语病的地方：没有存在语病的地方"
            data_instance.append(data)
    with open(r"cgec\train\task3\scope_shuffle.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_type
            data["input"] = line["input"]
            data["output"] = f'这句话中含有的语病错误类型：{line["type"]}'
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_type
            data["input"] = line["input"]
            data["output"] = f"这句话中含有的语病错误类型：无"
            data_instance.append(data)
    with open(r"cgec\train\task3\type_shuffle.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    makeOrder(data_list, "t-s-c")
    makeOrder(data_list, "t-c-s")
    makeOrder(data_list, "s-t-c")
    makeOrder(data_list, "s-c-t")
    makeOrder(data_list, "c-t-s")
    makeOrder(data_list, "c-s-t")

    data_instance = []
    for line in data_list:
        if line["flag"] == 1:
            data = {}
            data["instruction"] = prompt_cot
            data["input"] = line["input"]
            data["output"] = (
                f'该句子存在语病，其中“{line["scope"]}”存在{line["type"]}的问题。经过纠正后，正确的句子是：{line["output"][0]}'
            )
            data_instance.append(data)
        else:
            data = {}
            data["instruction"] = prompt_cot
            data["input"] = line["input"]
            data["output"] = (
                f'该句子没有任何语病，因此无需任何纠正，正确的句子是：{line["output"][0]}'
            )
            data_instance.append(data)
    with open(r"cgec\train\task3\cot.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def makeOrder(data_list, order):
    order_list = order.split("-")
    data_instance = []
    for line in data_list:
        for o in order_list:
            if o == "s":
                if line["flag"] == 1:
                    data = {}
                    data["instruction"] = prompt_scope
                    data["input"] = line["input"]
                    data["output"] = f'该句存在语病的地方：{line["scope"]}'
                    data_instance.append(data)
                else:
                    data = {}
                    data["instruction"] = prompt_scope
                    data["input"] = line["input"]
                    data["output"] = f"该句存在语病的地方：没有存在语病的地方"
                    data_instance.append(data)
            if o == "t":
                if line["flag"] == 1:
                    data = {}
                    data["instruction"] = prompt_type
                    data["input"] = line["input"]
                    data["output"] = f'这句话中含有的语病错误类型：{line["type"]}'
                    data_instance.append(data)
                else:
                    data = {}
                    data["instruction"] = prompt_type
                    data["input"] = line["input"]
                    data["output"] = f"这句话中含有的语病错误类型：无"
                    data_instance.append(data)
            if o == "c":
                data = {}
                data["instruction"] = prompt_correct
                data["input"] = line["input"]
                data["output"] = f'正确的句子：{line["output"][0]}'
                data_instance.append(data)
    with open(rf"cgec\train\task3\sample_{order}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def trainShuffle():
    data_list = []
    with open(r"ori_data\FCGEC_train_auto.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    random.shuffle(data_list)
    with open(r"ori_data\FCGEC_train_shuffle.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_list, indent=2, ensure_ascii=False))


def makeTest():
    # # FCGEC_test
    data_list = []
    with open(r"ori_data\FCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = ""
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # FCGEC_dev
    data_list = []
    with open(r"ori_data\FCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # MuCGEC_dev
    data_list = []
    with open(r"ori_data\MuCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\MuCGEC_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_dev
    data_list = []
    with open(r"ori_data\NaCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_test
    data_list = []
    with open(r"ori_data\NaCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_correct
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def makeCoT():
    # # FCGEC_test
    data_list = []
    with open(r"ori_data\FCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_cot
        data["input"] = line["input"]
        data["output"] = ""
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_cot_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # FCGEC_dev
    data_list = []
    with open(r"ori_data\FCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_cot
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_cot_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # MuCGEC_dev
    data_list = []
    with open(r"ori_data\MuCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_cot
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\MuCGEC_cot_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_dev
    data_list = []
    with open(r"ori_data\NaCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_cot
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_cot_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_test
    data_list = []
    with open(r"ori_data\NaCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_cot
        data["input"] = line["input"]
        data["output"] = f"正确的句子：{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_cot_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def extraTest():
    # FCGEC_dev
    data_list = []
    with open(r"ori_data\FCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_type
        data["input"] = line["input"]
        if line["flag"] == 1:
            data["output"] = f'这句话中含有的语病错误类型：{line["type"]}'
        else:
            data["output"] = f"这句话中含有的语病错误类型：无"
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_type.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_scope
        data["input"] = line["input"]
        data["output"] = ""
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_scope.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


def makeBaseTest():
    # # FCGEC_test
    data_list = []
    with open(r"ori_data\FCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_base
        data["input"] = line["input"]
        data["output"] = ""
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_base_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # FCGEC_dev
    data_list = []
    with open(r"ori_data\FCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_base
        data["input"] = line["input"]
        data["output"] = f"{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\FCGEC_base_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # MuCGEC_dev
    data_list = []
    with open(r"ori_data\MuCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_base
        data["input"] = line["input"]
        data["output"] = f"{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\MuCGEC_base_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_dev
    data_list = []
    with open(r"ori_data\NaCGEC_dev.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_base
        data["input"] = line["input"]
        data["output"] = f"{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_base_dev.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))

    # NaCGEC_test
    data_list = []
    with open(r"ori_data\NaCGEC_test.json", "r", encoding="utf-8") as file:
        data_list = json.load(file)

    data_instance = []
    for line in data_list:
        data = {}
        data["instruction"] = prompt_base
        data["input"] = line["input"]
        data["output"] = f"{random.choice(line['output'])}"
        data_instance.append(data)
    with open(r"cgec\test\NaCGEC_base_test.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_instance, indent=2, ensure_ascii=False))


# makeCoT()
# makeTrainTask3()
# makeTest()
# extraTest()
makeBaseTest()
