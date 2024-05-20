import json

import jieba
import jsonlines
import re
from tqdm import tqdm

point = "，。？！：；…"


def mixDouPoint(input, sentence):
    startPoint = ["“", "‘", "《"]
    startCount = [0 for i in range(len(startPoint))]
    endPoint = ["”", "’", "》"]
    endCount = [0 for i in range(len(endPoint))]
    needMix = False
    needPoint = ""
    for c in sentence:
        if c in startPoint:
            startCount[startPoint.index(c)] += 1
        if c in endPoint:
            endCount[endPoint.index(c)] += 1
    for i in range(len(startCount)):
        if startCount[i] != endCount[i]:
            needMix = True
            if startCount[i] > endCount[i]:
                needPoint = endPoint[i]
            else:
                needPoint = startPoint[i]
            break
    if needMix:
        temp = input
        hasMix = False
        if temp.startswith(sentence):
            temp = list(temp[len(sentence) :])
            for c in temp:
                if not hasMix:
                    sentence = sentence + c
                    if c == needPoint:
                        hasMix = True
                elif c not in point:
                    sentence = sentence + c
                else:
                    break
        elif temp.endswith(sentence):
            temp = list(temp[: len(sentence)])
            temp.reverse()
            for c in temp:
                if not hasMix:
                    sentence = c + sentence
                    if c == needPoint:
                        hasMix = True
                elif c not in point:
                    sentence = c + sentence
                else:
                    break
        else:
            temp = temp.split(sentence)
            t1 = list(temp[0])
            t1.reverse()
            t2 = list(temp[1])
            if needPoint in startPoint:
                for c in t1:
                    if not hasMix:
                        sentence = c + sentence
                        if c == needPoint:
                            hasMix = True
                    elif c not in point:
                        sentence = c + sentence
                    else:
                        break
                for c in t2:
                    if c not in point:
                        sentence += c
                    else:
                        break
            else:
                for c in t1:
                    if c not in point:
                        sentence = c + sentence
                    else:
                        break
                for c in t2:
                    if not hasMix:
                        sentence = sentence + c
                        if c == needPoint:
                            hasMix = True
                    elif c not in point:
                        sentence = sentence + c
                    else:
                        break
        for sp in startPoint:
            if sentence.startswith(sp) and sentence.endswith(
                endPoint[startPoint.index(sp)]
            ):
                sentence = sentence[1:-1]
        for p in point:
            if sentence.endswith(p):
                sentence = sentence[0:-1]
    return sentence


# 按字进行划分
def addPos1(line):
    word_list = list(line["input"])
    index_list = []
    i_l = [i for i in range(len(word_list))]
    for out in line["output"]:
        temp1 = out
        temp2 = out
        for index in i_l:
            if temp1.startswith(word_list[index]):
                temp1 = temp1[len(word_list[index]) :]
            else:
                index_list.append(index)
                break
        i_l.reverse()
        for index in i_l:
            if temp2.endswith(word_list[index]):
                temp2 = temp2[: len(temp2) - len(word_list[index])]
            else:
                index_list.append(index)
                break
        i_l.reverse()
    index_list.sort()
    start_index = index_list[0]
    end_index = index_list[-1]
    if (
        word_list[start_index] in point
        and word_list[end_index] in point
        and end_index - start_index > 1
    ):
        start_index += 1
        end_index -= 1
    if word_list[start_index] in point:
        start_index += 1
    if word_list[end_index] in point:
        end_index -= 1
    pos = "".join(word_list[start_index : end_index + 1])
    pos = mixDouPoint(line["input"], pos)
    return pos


# 按词进行划分
def addPos2(line):
    word_list = jieba.lcut(line["input"])
    index_list = []
    i_l = [i for i in range(len(word_list))]
    for out in line["output"]:
        temp1 = out
        temp2 = out
        for index in i_l:
            if temp1.startswith(word_list[index]):
                temp1 = temp1[len(word_list[index]) :]
            else:
                index_list.append(index)
                break
        i_l.reverse()
        for index in i_l:
            if temp2.endswith(word_list[index]):
                temp2 = temp2[: len(temp2) - len(word_list[index])]
            else:
                index_list.append(index)
                break
        i_l.reverse()
    index_list.sort()
    start_index = index_list[0]
    end_index = index_list[-1]
    if (
        word_list[start_index] in point
        and word_list[end_index] in point
        and end_index - start_index > 1
    ):
        start_index += 1
        end_index -= 1
    if word_list[start_index] in point:
        start_index += 1
    if word_list[end_index] in point:
        end_index -= 1
    pos = "".join(word_list[start_index : end_index + 1])
    pos = mixDouPoint(line["input"], pos)
    return pos


# 按子句进行划分
def addPos3(line):
    pos_list = []
    for out in line["output"]:
        input_list = re.split(r"[，。？！：；]", line["input"])
        if "" in input_list:
            input_list.remove("")
        out_list = re.split(r"[，。？！：；]", out)
        if "" in out_list:
            out_list.remove("")
        for o in out_list:
            if o == input_list[0]:
                input_list.remove(o)
            else:
                break
        out_list.reverse()
        for o in out_list:
            if o == input_list[-1]:
                input_list.remove(o)
            else:
                break
        pos_list.extend(input_list)
    pos_list = list(set(pos_list))

    input_list = re.split(r"[，。？！：；]", line["input"])
    if "" in input_list:
        input_list.remove("")
    pos = line["input"]
    for i in input_list:
        if i not in pos_list:
            pos = pos[len(i) :]
            if pos[0] in point:
                pos = pos[1:]
        else:
            break
    input_list.reverse()
    for i in input_list:
        if pos[-1] in point:
            pos = pos[:-1]
        if i not in pos_list:
            pos = pos[: -len(i)]
        else:
            break
    input_list.reverse()
    pos = mixDouPoint(line["input"], pos)
    return pos


data_list = []
with open(r"ori_data/FCGEC_train.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

for line in tqdm(data_list):
    if line["flag"] == 1:
        if line["type"] in ["表意不明", "成分赘余"]:
            line["scope"] = addPos2(line)
        elif line["type"] in [
            "语序不当",
            "搭配不当",
            "成分残缺",
            "结构混乱",
            "不合逻辑",
        ]:
            line["scope"] = addPos3(line)
        if line["scope"] == "":
            if addPos2(line) != "":
                line["scope"] = addPos2(line)
            elif addPos3(line) != "":
                line["scope"] = addPos3(line)

with open(r"ori_data/FCGEC_train_auto.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(data_list, indent=2, ensure_ascii=False))
