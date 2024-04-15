# nacos_manager.py
import json

import requests


class GetConfigParam:
    def __init__(self, port, app_id, service_id, common_name):
        self.port = port
        self.app_id = app_id
        self.service_id = service_id
        self.common_name = common_name


# 全局参数
param = GetConfigParam(0, 0, 0, "")

nacos_data_cache = {}


def init_config_param(port, app_id, service_id, common_name):
    param.port = port
    param.app_id = app_id
    param.service_id = service_id
    param.common_name = common_name


def get_config_by_nacos(data_id, group, common_name=""):
    if f'{data_id}_{group}' in nacos_data_cache:
        return nacos_data_cache[f'{data_id}_{group}_{common_name}']
    print('get_config_by_nacos:', param.port, "==", param.service_id, "==", param.service_id)
    url = get_request_url(param.port, param.service_id, data_id, group, common_name)
    print(url)
    header = get_request_header(param.app_id)
    # 获取配置
    response = perform_http_request(url, method='GET', headers=header)
    if response and response.status_code == 200:
        print('响应内容：', response.text)
        data_map = json.loads(response.text)
        nacos_data_cache[f'{data_id}_{group}_{common_name}'] = data_map["data"]
        return data_map["data"]
    else:
        print(f'请求失败，错误信息：{response.text}')
        return ""


def perform_http_request(url, method='GET', headers=None, data=None):
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, data=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        return response
    except Exception as e:
        print(f"HTTP请求发生异常: {e}")
        return None


def get_request_url(port, service_id, data_id, group, common_name):
    return f"http://127.0.0.1:{port}/config/nacos/read?dataId={data_id}&serviceId={service_id}&group={group}&commonName={common_name}"


def get_request_header(app_id):
    return {
        'appid': str(app_id),
        'Content-Type': 'application/json'
    }


# /////////////////////////////// scheam 模板替换操作 /////////////////////////

# 优化一个结构体中 同一组件多次引用
shellCodeCache = {}


# 基于自定义 schema 结构体 完成模板数据完全替换
def out_put_end_schema(param):
    for key, base_schema in param.items():
        if not isinstance(base_schema, dict):
            continue

        temp_data = replace_schema(key, base_schema["schema"])
        if temp_data is None:
            print(f"[Error] in gen_module_by_schema: Unable to replace schema for {key}")
            return param

        param[key]["schema"] = temp_data

    return param


# 递归处理 所有需要替换的模板信息
def replace_schema(key, schema):
    for sub_key, v in schema.items():
        # 递归处理结构体类型
        if "type" in v and v["type"] == "object":
            schema[sub_key]["properties"] = replace_schema(sub_key, v["properties"])
            if schema[sub_key]["properties"] is None:
                return schema

        # 递归处理数组类型
        if "type" in v and v["type"] == "table":
            arr_base = v["items"]
            if isinstance(arr_base, dict) and arr_base.get("type") == "object":
                schema[sub_key]["items"]["properties"] = replace_schema(sub_key, arr_base["properties"])
                if schema[sub_key]["items"]["properties"] is None:
                    return schema

        if "importInfo" in v:
            title = ""
            if "title" in v:
                title = v["title"]
            end_struct = replace_import_model(v["importInfo"], title, sub_key)
            if end_struct is None:
                return schema

            # 替换数据
            schema[sub_key] = end_struct[sub_key]

    return schema


# 获取模板中 python 脚本并执行 获取需要替换的值
def replace_import_model(info, title, sub_key):
    if "importName" not in info:
        print(f"[Error] replace_import_model can not found info {info}")
        return {sub_key: {}}
    import_name = info["importName"]

    import_param = {}
    if "importParam" in info:
        import_param = info["importParam"]
    import_param["common_params"] = {"appId": param.app_id}
    # print(f"replace_import_model import_name:{import_name} import_param {import_param} ")

    temp_schema = get_template(import_name)
    # print(f"replace_import_model get_template:{import_name} temp_schema: {temp_schema}")
    # 获取 脚本数据
    if "shellCode" in temp_schema:
        shell_code = temp_schema["shellCode"]
        print(f"replace_import_model get_template:{import_name} shell_code: {shell_code}")

        # 动态加载 代码块 并执行动态方法

        model_data = exec_shell_code(shell_code, import_name, import_param, sub_key)

        # 重命名 title
        if "title" in model_data[sub_key] and title != "":
            model_data[sub_key]["title"] = title

        print(f"replace_import_model get_template:{import_name} end model_data: {model_data}")
        return model_data
    print(f"[Error] replace_import_model get_template not found shell_code")
    return {sub_key: {}}


# 动态调用python
def exec_shell_code(shell_code, import_name, import_param, sub_key):
    # 定义 gen_template 函数
    external_module = {}

    # 动态加载 代码块 并执行动态方法
    exec(shell_code, external_module)
    gen_template = external_module.get("gen_template")
    model_data = gen_template(import_param)
    # 递归生成模板内嵌套
    # print(f"replace_import_model get_template:{import_name} begin model_data: {model_data}")
    return replace_schema(sub_key, {sub_key: json.loads(model_data)})


# 获取 指定template 模板获取
def get_template(model_name):
    if model_name in shellCodeCache:
        print(f"get_template name {model_name} by cache {shellCodeCache[model_name]}")
        return shellCodeCache[model_name]
    # print('get_template:', param.port, "==", param.service_id)
    url = get_template_url(param.port, param.service_id)
    header = get_request_header(param.app_id)

    body = {"templateName": model_name, "commonName": param.common_name}
    print(f'get_template url{url} head{header} body{body}')
    # 获取配置
    response = perform_http_request(url, method='POST', headers=header, data=json.dumps(body))
    if response and response.status_code == 200:
        print('响应内容：', response.text)
        data_map = json.loads(response.text)
        shellCodeCache[model_name] = data_map["data"]
        return data_map["data"]
    else:
        print(f'请求失败，错误信息：{response.text}')
        return ""


def get_template_url(port, service_id):
    return f"http://127.0.0.1:{port}/template/info?serviceId={service_id}"
