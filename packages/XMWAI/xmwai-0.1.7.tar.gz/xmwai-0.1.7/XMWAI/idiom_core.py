import random
import json


def idiom(word, mode=0):
    """
    查询成语信息
    :param word: 要查询的成语
    :param mode: 查询模式
                 0 - 判断是否是成语，返回 True/False
                 1 - 返回拼音
                 2 - 返回解释
                 3 - 返回出处
    :return: 查询结果或 None
    """
    if mode == 0:
        with open("idiom.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if word == i["word"]:
                    return True
        return False
    elif mode == 1:
        with open("idiom.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if word == i["word"]:
                    return i["pinyin"]
        return None

    elif mode == 2:
        with open("idiom.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if word == i["word"]:
                    return i["explanation"]
        return None
    elif mode == 3:
        with open("idiom.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if word == i["word"]:
                    return i["derivation"]
        return None


def searchIdiom(text, num=1):
    """
    模糊查询成语
    :param text: 要查询的字
    :param mode: 第几个字
    :return: 查询结果 或 None
    """
    wordList = []
    with open("idiom.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in data:
            try:
                if text == i["word"][num-1]:
                    wordList.append(i["word"])
            except:
                pass
    if wordList:
        return random.choice(wordList)
    else:
        return False
