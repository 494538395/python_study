import json

# 导入common包 目前可用于获取读取其他配置表


# 自定义最终配置结构
# class Item:


# @name    gen_json
# @param   {any} json_data - 基础数据的结构体数据
# @returns {str}           - 最终 完整配置 json 数据(str)
# @desc 基于与策划定义基础数据格式结合 python 完成完整 配置数据的创建
def gen_json(json_data: any) -> str:
    print("hello, gen_json")
    print("jsonData-->", json_data)

    match_mode_config = json_data.get("simple_test", {}).get("modes", [])
    data = {"modes": match_mode_config}

    # 遍历所有 modes
    for mode in data['modes']:
        # 遍历所有 stages
        for stage in mode['stages']:
            # 将 rangeMin 和 rangeMax 转换为 range 字段
            stage['range'] = {'min': stage.pop('rangeMin'), 'max': stage.pop('rangeMax')}

    return json.dumps(data)


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
