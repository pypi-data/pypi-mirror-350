import re
import requests
import json
import os


def story(role, time, address, event, key=""):
    content = role+time+address+event
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
            "max_tokens": 1000,     # 回复长度限制
            "top_k": 4,             # 灵活度
            "temperature": 0.5,     # 随机性
            "messages": [
        {
            # 设置对话背景或赋予模型角色，该设定会贯穿整轮对话，对全局的模型生成结果产生影响。对应作为'role'为'system'时，'content'的值
            "role": "system",
            "content": "我是一个非常会写童话的儿童写作作家,根据我写出的关键词，帮我生成一篇童话故事。"
        },
        {
            # 对大模型发出的具体指令，用于描述需要大模型完成的目标任务和需求说明。会与角色设定中的内容拼接，共同作为'role'为'system'时，'content'的值
            "role": "user",
            "content": content
        }
    ],
    "model": "4.0Ultra"
    }
    data["stream"] = True
    if key == "":
        print("没有秘钥！请提供秘钥！")
        return "没有秘钥！请提供秘钥！"
    elif key != "CaJQ":
        print("秘钥错误！请重新输入！")
        return "秘钥错误！请重新输入！"
    header = {
            "Authorization": "Bearer paNyL"+key+"OpyOBmflKZp:yhBhAlSFMwaqlVKAtDbv"
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 流式响应解析示例
    response.encoding = "utf-8"
    contents = ""
    result = response.iter_lines(decode_unicode="utf-8")
    result = str(list(result))
     
    # 正则表达式模式
    pattern = r'"content":"(.*?)"'

    # 使用re.findall查找所有匹配的内容
    contents = re.findall(pattern, result, re.DOTALL)
    s = ""
    for i in contents:
        s += i
    s = s.replace('\\', "")
    s = s.replace("n", "")
    return s


def photo(content, style, size, key=""):
    # 图像生成的 API URL
    if key == "":
        print("没有秘钥！请提供秘钥！")
        return "没有秘钥！请提供秘钥！"
    elif key != "CaJQ":
        print("秘钥错误！请重新输入！")
        return "秘钥错误！请重新输入！"
    key = "image"
    url = "https://gateway.xiaomawang.com/pythonUILibApi/api/text2" + key

    # 请求的头部
    headers = {
        "Content-Type": "application/json"
    }
    resolution = {"1024*1024":3, "1280*720":4, "720*1280":5}
    if content == "":
        return
    if style == "":
        style="默认"
    if size == "":
        size="1024*1024"
    
    # 请求的主体内容
    data = {
        'prompt': content,  # 你想要生成的图像描述
        'imgStyle': style,  
        'imgSize': resolution[size]  # 图像的尺寸
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=data)

    # 检查请求是否成功
    if response.status_code == 200:
        response_data = response.json()
        _data = eval(str(response_data))
        photo_url = _data["data"][0]["url"]

    skin = requests.get(photo_url).content
    with open("{}.png".format(content), 'wb') as s:
        s.write(skin)


def reply(role, content, key=""):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
            "max_tokens": 60,     # 回复长度限制
            "top_k": 5,             # 灵活度
            "temperature": 0.6,     # 随机性
            "messages": [
        {
            # 设置对话背景或赋予模型角色，该设定会贯穿整轮对话，对全局的模型生成结果产生影响。对应作为'role'为'system'时，'content'的值
            "role": "system",
            "content": "你是一位非常优秀的" + role + "，请根据我的提问，非常科学、有趣和严谨的回答我。"
        },
        {
            # 对大模型发出的具体指令，用于描述需要大模型完成的目标任务和需求说明。会与角色设定中的内容拼接，共同作为'role'为'system'时，'content'的值
            "role": "user",
            "content": content + "(一定要80个字左右，语句必须完整，语句必须完整，不准出现断句。)"
        }
    ],
    "model": "4.0Ultra"
    }
    data["stream"] = True
    if key == "":
        print("没有秘钥！请提供秘钥！")
        return "没有秘钥！请提供秘钥！"
    elif key != "CaJQ":
        print("秘钥错误！请重新输入！")
        return "秘钥错误！请重新输入！"
    header = {
            "Authorization": "Bearer paNyL"+key+"OpyOBmflKZp:yhBhAlSFMwaqlVKAtDbv"
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 流式响应解析示例
    response.encoding = "utf-8"
    contents = ""
    result = response.iter_lines(decode_unicode="utf-8")
    result = str(list(result))
     
    # 正则表达式模式
    pattern = r'"content":"(.*?)"'

    # 使用re.findall查找所有匹配的内容
    contents = re.findall(pattern, result, re.DOTALL)
    s = "   "
    for i in contents:
        s += i
    if '\\' in s:
        s = s.replace('\\', "")
    if '*' in s:
        s = s.replace('*', "")
    sum_ = """"""
    for i in range(0,len(s),17):
        sum_ = sum_ + s[i:i+17] + "\n"
    return sum_


def get_access_token(key):
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    API_KEY = "Ox1CTF00wD50XmXF1hiPSqdh"
    SECRET_KEY = "4ZQt4Zj"+ key +"zuT2XtBtRojdRZ3HgZOtrP"
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error getting access token:", response.text)
        return None


def poem(title, key=""):
    if key == "":
        print("没有秘钥！请提供秘钥！")
        return "没有秘钥！请提供秘钥！"
    elif key != "CaJQ":
        print("秘钥错误！请重新输入！")
        return "秘钥错误！请重新输入！"
    key = "ZZC"
    access_token = get_access_token(key)
    if access_token:
        url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/poem?access_token={access_token}"
        payload = {
            "text": title,  # 直接使用普通字符串
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 直接发送JSON对象，不转换为字符串
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['poem'][0]['content']  # 使用response.json()直接解析JSON响应
        else:
            print("Failed with status code:", response.status_code)
            print("Response:", response.text)
    else:
        print("Failed to get access token.")
