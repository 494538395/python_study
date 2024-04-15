import json

import requests

# Nacos
MATCH_MODE_CONFIG = "match_mode_config"
MATCH_RULE_CONFIG = 'match_rule_config'
STORAGE_RULE_CONFIG = 'storage_rule_config'
SEPARATOR = '_'


# 生成匹配模式配置 dataId
def gen_match_mode_data_id(appId):
    return str(appId) + SEPARATOR + MATCH_MODE_CONFIG


# 生成匹配规则配置 dataId
def gen_match_rule_data_id(appId):
    return str(appId) + SEPARATOR + MATCH_RULE_CONFIG


# 生成存储规则匹配 dataId
def gen_storage_rule_data_id(appId):
    return str(appId) + SEPARATOR + STORAGE_RULE_CONFIG


# 生成默认 nacos content
def gen_default_nacos_content(dataId):
    content = {
        "dataId": dataId,
        "defaultContent": "",
        "remote": None,
        "experiments": None
    }

    return json.dumps(content)


# 生成 dataId
def gen_data_ids(appId):
    data_ids = [
        gen_match_mode_data_id(appId),
        gen_match_rule_data_id(appId),
        gen_storage_rule_data_id(appId)
    ]
    return data_ids


def gen_app_config(params: dict) -> str:
    # 解析参数
    app_id = params.get("AppId")
    nacos_url = params.get("NacosUrl")
    nacos_group = params.get("NacosGroup")

    # 生成 dataId
    data_ids = gen_data_ids(app_id)

    # 遍历字符串数组
    for data_id in data_ids:
        # 只有不存在的 dataId 才会推送空配置
        if not check_data_id_exist(data_id, nacos_url, nacos_group):
            print("即将推送 " + data_id)
            push_config_to_nacos(data_id, nacos_url, nacos_group)

    print("gen_app_config 执行结束")


# 检查 dataId 是否存在
def check_data_id_exist(data_id, nacos_url, nacos_group) -> bool:
    # 构建请求的 URL
    url = f"{nacos_url}/nacos/v1/cs/configs?dataId={data_id}&group={nacos_group}"

    # 发送 HTTP GET 请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 如果状态码为 200，则表示 dataId 存在
        return True
    elif response.status_code == 404:
        # 如果状态码为 404，则表示 dataId 不存在
        return False
    else:
        # 其他状态码，返回未知结果
        return None


# 推送配置到 nacos
def push_config_to_nacos(data_id, nacos_url, nacos_group):
    # 生成默认配置
    content = gen_default_nacos_content(dataId=data_id)

    # 构建 Nacos API 的 URL
    url = f"{nacos_url}/nacos/v1/cs/configs?dataId={data_id}&group={nacos_group}&content={content}"

    # 发起 HTTP 请求推送配置
    try:
        response = requests.post(url)
        response.raise_for_status()  # 检查响应状态码
        print(data_id + " 配置已成功推送到 Nacos")
    except Exception as e:
        print("推送配置到 Nacos 失败:", e)
