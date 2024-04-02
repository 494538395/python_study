import json

from nacos import NacosClient

# Nacos
SERVER_ADDRESS = "10.0.1.84:38848"  # 服务器地址,多台需要用,隔开
GROUP_ID = 'event-center-v2'
NAMESPACE = 'public'
LOG_DIR = '../nacos/log'


def init_nacos_client():
    nacos_client = NacosClient(server_addresses=SERVER_ADDRESS, namespace=NAMESPACE, logDir=LOG_DIR)
    return nacos_client


def get_task_event_data_id(app_id) -> str:
    return str(app_id) + "_task_event_config"


def gen_template(params: any) -> str:
    if isinstance(params, dict):
        # 如果 params 是字典类型，则直接使用
        nacos_client = init_nacos_client()

        # 获取 nacos 任务事件配置
        data_id = get_task_event_data_id(params.get("appId"))

        content = nacos_client.get_config(data_id=data_id, group=GROUP_ID)

        data = json.loads(content)
        result = {
            "title": "任务事件列表",
            "type": "selector",
            "params": {
                "options": []
            }
        }

        options = []
        for event in data['taskEventConfig']:
            option = {
                "label": event['event'] + " - " + str(event['id']),
                "value": event['id']
            }
            options.append(option)

        result["params"]["options"].append({"label": "Manager", "options": options})

        res = json.dumps(result, indent=2, ensure_ascii=False)
        print(res)

        return res

    else:
        raise Exception("params 不是字典类型")


if __name__ == "__main__":
    print("你好")

    gen_template({"appId": 888})
