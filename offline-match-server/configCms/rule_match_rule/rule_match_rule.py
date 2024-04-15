import json


# 导入common包 目前可用于获取读取其他配置表

# 自定义最终配置结构
# class Item:


# 生成匹配规则 JSON
def gen_json(json_data: any) -> str:
    print("hello, gen_json")
    print("jsonData-->", json_data)

    match_rule_config = json_data.get("simple_test", {}).get("rules", [])
    data = {"rules": match_rule_config}

    # 遍历所有 modes
    for rule in data['rules']:
        # 处理 排序
        if len(rule['sort']) == 0:
            print(1)
        if 'fields' in rule['sort']:
            sort = gen_sort(rule['sort']['fields'], rule['sort']['order'])
            rule['sort'] = sort

    return json.dumps(data, ensure_ascii=False)


# 生成 sort
def gen_sort(intimacyFields, order: any, ):
    sort = {
        "type": "number",
        "order": order,
        "params": intimacyFields,
        "func": {
            "variables": [],
            "result": ""
        },
    }

    # 生成排序
    sort['func']['variables'] = gen_sort_variables(intimacyFields)
    sort['func']['result'] = gen_sort_result(intimacyFields)

    print("sort-->", sort)

    return sort


# 生成 variables 语句
def gen_sort_variables(intimacyFields: any):
    variables = []

    # 遍历所有 modes
    for field in intimacyFields:
        item = {
            "name": field + "Factor",
            "expr": "1 / Math.max(1, (Math.abs(others['{}'].value - self.{}) + 1));".format(field, field)
        }
        # 将 item 添加到 variables 列表中
        variables.append(item)

    return variables


# 生成 result 语句
def gen_sort_result(intimacyFields: any):
    # 生成每个字段的因子表达式
    field_factors = [field + "Factor" for field in intimacyFields]

    # 使用字符串的 join 方法将所有字段的因子表达式连接起来
    result_sql = "*".join(field_factors)

    return result_sql + ";"


# @name    gen_schema
# @param   {any} data - 规则页面中配置的完整 schema 的json对象
# @returns {str}      - 最终 完整配置 json 数据
# @desc 自定义逻辑用来支持 schema 字段下拉框支持, 返回结构:
def gen_schema(data: any) -> str:
    print("hello, gen_schema")
    return json.dumps(data)

# @name    base_common.get_config_by_nacos
# @param   {str} data_id    - 获取的对应nacos的 dataID
# @param   {str} group_id   - 数据所在的 group
# @returns {str}            - 最终从nacos中获取到的配置信息字符串
# @desc 用于级联查询关联配置的配置信息的函数
