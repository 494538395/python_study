import json


# 导入common包 目前可用于获取读取其他配置表

# 自定义最终配置结构
# class Item:


# @name    gen_json
# @param   {any} json_data - 基础数据的结构体数据
# @returns {str}           - 最终 完整配置 json 数据(str)
# @desc 基于与策划定义基础数据格式结合 python 完成完整 配置数据的创建
# 参数校验
# 参数校验
# 参数校验
def param_check(task_group_config):
    CUSTOM_INTERNAL_GROUP_TYPE = 4
    print("task_group_config -->", task_group_config)

    # 任务组Id校验
    if not task_group_config["id"]:
        raise Exception("任务组Id 没有填写")
    # 任务组类型校验
    if not task_group_config["groupType"]:
        raise Exception("任务组类型没有写")

    # 重置频率校验
    group_type = task_group_config["groupType"]
    if int(group_type) == CUSTOM_INTERNAL_GROUP_TYPE and not task_group_config["interval"]:
        raise Exception("你选择的任务组类型是自定义重置频率，请设置重置频率")

    # 开始时间
    if not task_group_config["startTime"]:
        raise Exception("任务组开始时间没有写")

    # 开始时间
    if not task_group_config["startTime"]:
        raise Exception("任务组开始时间没有写")

    # 开始时间
    if not task_group_config["endTime"]:
        raise Exception("任务组结束时间没有写")


def gen_json(json_data):
    transformed_data = {
        "taskGroupConfig": []
    }

    for task_group_config in json_data["simple_test"]["taskGroupConfig"]:
        # 参数校验
        param_check(task_group_config)

        # 映射参数
        task_group = {
            "id": task_group_config["id"],
            "groupType": task_group_config["groupType"],
            "interval": task_group_config.get("interval") or 0,
            "resetTaskCount": task_group_config.get("resetTaskCount") or 0,
            "needSubscribed": task_group_config["needSubscribe"],
            "replaceTaskCount": task_group_config.get("replaceTaskCount") or 0,
            "preGroups": task_group_config.get("preGroups", []),
            "startTime": task_group_config["startTime"],
            "endTime": task_group_config["endTime"],
            "taskListStage": []
        }

        # 没有分档，就只有一档
        if len(task_group_config["stages"]) == 0:
            merge_task_without_group_stage(transformed_data, task_group_config, task_group)
            continue

        # 根据任务组分档条件，计算出对应档位下的任务列表
        merge_task_by_group_stage(transformed_data, task_group_config, task_group)

    return json.dumps(transformed_data)


def merge_task_by_group_stage(transformed_data, task_group_config, task_group) -> any:
    # 遍历任务组档位
    for stage_index, stage in enumerate(task_group_config["stages"]):
        stage_data = {
            # 档位下的任务列表
            "list": [],
            # 档位条件
            "cond": stage["cond"]
        }

        skip_index = 0

        for task_index, task in enumerate(task_group_config["taskList"]):
            # 跳过已合并的任务
            if task_index < skip_index:
                continue

            if "stage" not in task:
                raise Exception(
                    f"任务没有指定所在任务组档位，任务Id: {task['taskId']},任务组Id: {task_group_config['id']}")

            # 处理统一档位下的任务
            if task["stage"] == stage_index + 1:
                cur_taskId = task["taskId"]

                # 当前任务
                task_data = {
                    "taskId": task["taskId"],
                    "stages": [
                        {
                            "prog": task["prog"],
                            "rewards": task["rewards"]
                        }
                    ]
                }

                # 下一个 index
                next_task_index = task_index + 1

                # 比较下一个 taskId 是否和当前相等
                while (next_task_index < len(task_group_config["taskList"]) and cur_taskId ==
                       task_group_config["taskList"][next_task_index]["taskId"] and
                       stage_index + 1 == task_group_config["taskList"][next_task_index]["stage"]):
                    next_task = task_group_config["taskList"][next_task_index]

                    # 合并任务阶段
                    task_data["stages"].append({
                        "prog": next_task["prog"],
                        "rewards": next_task["rewards"]
                    })
                    # 维护遍历下标
                    next_task_index += 1
                    skip_index = next_task_index

                stage_data["list"].append(task_data)

        task_group["taskListStage"].append(stage_data)

    transformed_data["taskGroupConfig"].append(task_group)

    return transformed_data


def merge_task_without_group_stage(transformed_data, task_group_config, task_group) -> any:
    # 默认分档
    stage_data = {
        # 档位下的任务列表
        "list": [],
        # 档位条件
        "cond": []
    }

    # 跳过遍历的索引
    skip_index = 0

    for task_index, task in enumerate(task_group_config["taskList"]):
        # 跳过已合并的任务
        if task_index < skip_index:
            continue

        # 处理统一档位下的任务
        cur_taskId = task["taskId"]

        # 当前任务
        task_data = {
            "taskId": task["taskId"],
            "stages": [
                {
                    "prog": task["prog"],
                    "rewards": task["rewards"]
                }
            ]
        }

        # 下一个 index
        next_task_index = task_index + 1

        # 比较下一个 taskId 是否和当前相等
        while (next_task_index < len(task_group_config["taskList"]) and cur_taskId ==
               task_group_config["taskList"][next_task_index]["taskId"]):
            next_task = task_group_config["taskList"][next_task_index]

            # 合并任务阶段
            task_data["stages"].append({
                "prog": next_task["prog"],
                "rewards": next_task["rewards"]
            })
            # 维护遍历下标
            next_task_index += 1
            skip_index = next_task_index

        stage_data["list"].append(task_data)

    # 加入默认档位数据
    task_group["taskListStage"].append(stage_data)

    transformed_data["taskGroupConfig"].append(task_group)

    return transformed_data



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
