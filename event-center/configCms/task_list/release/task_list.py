import json

# 导入common包 目前可用于获取读取其他配置表

import base_common

COMMON_NAME = '事件中心'


def get_task_data_id(app_id) -> str:
    return str(app_id) + "_task_config"


def gen_template(params: any) -> str:
    if isinstance(params, dict):

        # 获取 nacos 任务事件配置
        data_id = get_task_data_id(params.get("common_params").get("appId"))

        nacos_group = params.get("nacos_group_id")
        print("nacos_group_id-->",nacos_group)

        content = base_common.get_config_by_nacos(data_id=data_id, group=nacos_group,
                                                  common_name=COMMON_NAME)
        print(content)

        data = json.loads(content)
        result = {
            "title": "任务列表",
            "type": "selector",
            "params": {
                "options": []
            }
        }

        options = []
        for task in data['taskConfig']:
            option = {
                "label": str(task['id']),
                "value": task['id']
            }
            options.append(option)

        result["params"]["options"].append({"label": "Manager", "options": options})

        res = json.dumps(result, indent=2, ensure_ascii=False)
        print(res)

        return res

    else:
        raise Exception("params 不是字典类型")
