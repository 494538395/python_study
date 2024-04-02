import json
import re

import pandas as pd


def getBasInfo():
    df1 = df.iloc[:, :9]

    result = {"taskGroupConfig": []}
    for index, row in df1.iterrows():
        if not row.isnull().all():
            current_base = {
                "id": int(row[0]),
                "groupType": int(row[1]),
                "interval": int(row[2]) if not pd.isnull(row[2]) else 0,
                "resetTaskCount": int(row[3]),
                "needSubscribed": bool(row[4]),
                "replaceCount": int(row[5]) if not pd.isnull(row[5]) else 0,
                "preGroups": getPreGroups(str(row[6])),
                "startTime": int(row[7]),
                "endTime": int(row[8]),
            }

            result["taskGroupConfig"].append(current_base)

    # print(json.dumps(result, indent=2))
    return result


def getPreGroups(input_str):
    array_of_numbers = input_str.split(',')
    if len(array_of_numbers) == 0:
        return []
    if array_of_numbers[0] == "nan":
        return []
    return [int(num) for num in array_of_numbers] if array_of_numbers else []


def getTaskListStages():
    df1 = df.ffill()

    result = {"stages": []}
    for index, row in df1.iterrows():
        if not row.isnull().all():
            cur_prog = {
                "id": int(row[0]),
                "expr": str(row[9]),
                "taskId": int(row[10]),
                "prog": int(row[11]),
                "rewards": []
            }
            rewards = getRewards(row[12])
            cur_prog["rewards"] = rewards
            result["stages"].append(cur_prog)

    # print(json.dumps(result, indent=2))
    return result


def getRewards(input_str):
    # 使用正则表达式匹配每一对大括号中的内容
    matches = re.findall(r'{(\d+),(\d+)}', input_str)

    # 将匹配结果转换为目标形式
    result = [{"itemId": int(item[0]), "itemCnt": int(item[1])} for item in matches]
    # print(result)
    return result


def getCond():
    co_fill = [0, 9]
    df1 = df
    df1[co_fill] = df1[co_fill].ffill()
    df1 = df1.iloc[:, 0:1].join(df1.iloc[:, 9:10])
    df1 = df1.drop_duplicates()
    # print(df1)

    condRes = {"cond_exp": []}
    for index, row in df1.iterrows():
        if not row.isnull().all():
            cur_cond = {
                "id": int(row[0]),
                "expr": str(row[9])
            }

            condRes["cond_exp"].append(cur_cond)

    # print(json.dumps(condRes, indent=2))
    return condRes


def marshalCond(input_str):
    # 定义正则表达式模式
    pattern = r'{(\d+),(\w+),(\d+)}'
    pattern = r'{(\d+),(\W+),(\d+)}'


    # 使用正则表达式进行匹配，并利用列表推导生成所需的字典列表
    matches = re.findall(pattern, input_str)
    if len(matches) == 0:
        return []
    result = [{
        "taskId": int(match[0]),
        "expr": str(match[1]),
        "val": int(match[2])
    } for match in matches]

    return result


def getTaskIds():
    co_fill = [0, 10]
    df1 = df.ffill()
    df1[co_fill] = df1[co_fill].ffill()
    df1 = df1.iloc[:, 0:1].join(df1.iloc[:, 9:11])
    df1 = df1.drop_duplicates()
    # print(df1)

    result = {"list": []}
    for index, row in df1.iterrows():
        if not row.isnull().all():
            current_list = {
                "id": int(row[0]),
                "expr": str(row[9]),
                "taskId": int(row[10])
            }
            result["list"].append(current_list)

    return result


if __name__ == '__main__':
    excel_file_path = 'config.xlsx'
    df = pd.read_excel(excel_file_path, skiprows=4, sheet_name=2, header=None)

    baseInfo = getBasInfo()

    conds = getCond()
    for cond in conds["cond_exp"]:
        for taskGroup in baseInfo["taskGroupConfig"]:
            if taskGroup["id"] == cond["id"]:
                taskGroup.setdefault("taskListStage", []).append(
                    {
                        "cond_exp": cond["expr"]
                    }
                )
    print(json.dumps(baseInfo, indent=2))
    print("----------------------------------")

    taskIds = getTaskIds()
    print(json.dumps(taskIds, indent=2))
    print("----------------------------------")
    for taskId in taskIds["list"]:
        for taskGroup in baseInfo["taskGroupConfig"]:
            for stage in taskGroup["taskListStage"]:
                if stage["cond_exp"] == taskId["expr"] and taskGroup["id"] == taskId["id"]:
                    stage.setdefault("list", []).append(
                        {
                            "taskId": taskId["taskId"]
                        }
                    )
    print(json.dumps(baseInfo, indent=2))
    print("----------------------------------")

    taskListStagesRes = getTaskListStages()
    # print(json.dumps(taskListStagesRes, indent=2))
    # print("----------------------------------")
    for sRes in taskListStagesRes["stages"]:
        for taskGroup in baseInfo["taskGroupConfig"]:
            for stage in taskGroup["taskListStage"]:
                for ts in stage["list"]:
                    if ts["taskId"] == sRes["taskId"] and taskGroup["id"] == sRes["id"]:
                        ts.setdefault("stages", []).append({
                            "prog": sRes["prog"],
                            "rewards": sRes["rewards"]
                        })

    # print(json.dumps(baseInfo, indent=2))
    # print("----------------------------------")

    for taskGroup in baseInfo["taskGroupConfig"]:
        for stage in taskGroup["taskListStage"]:
            cur_exp = marshalCond(stage["cond_exp"])
            stage["cond"] = cur_exp
            del stage["cond_exp"]

    print(json.dumps(baseInfo, indent=2))
    # stages = getTaskListStages()
