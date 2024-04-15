import json

import base_common

# 导入common包 目前可用于获取读取其他配置表

COMMON_NAME = '离线匹配'


# 生成 dataId
def get_match_rule_data_id(app_id) -> str:
    return str(app_id) + "_match_rule_config"


def gen_template(params: any) -> str:
    if isinstance(params, dict):

        # 1.获取 nacos 匹配规则配置
        data_id = get_match_rule_data_id(params.get("common_params").get("appId"))
        nacos_group = params.get("nacos_group_id")

        # 2.参数打印
        print("params.get(common_params).get(appId)-->", params.get("common_params").get("appId"))
        print("data_id-->", data_id)
        print("nacos_group_id-->", nacos_group)

        # 3.查 Nacos
        content = base_common.get_config_by_nacos(data_id=data_id, group=nacos_group,
                                                  common_name=COMMON_NAME)
        print("nacos content-->", content)

        # 4.组装下拉框
        data = json.loads(content)
        result = {
            "title": "匹配规则列表",
            "type": "selector",
            "params": {
                "options": []
            }
        }
        options = []
        for rule in data['rules']:
            option = {
                "label": rule['name'],
                "value": rule['name']
            }
            options.append(option)
        result["params"]["options"].append({"label": "Manager", "options": options})
        res = json.dumps(result, indent=2, ensure_ascii=False)
        print(res)

        # 5.返回结果
        return res

    else:
        raise Exception("params 不是字典类型")
