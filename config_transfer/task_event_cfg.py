import json

import pandas as pd


def getBasInfo():
    # 读取前7列
    df1 = df.iloc[:, :7]
    # print(df)

    result = {"taskEventConfig": []}
    for index, row in df1.iterrows():
        if not row.isnull().all():
            current_base = {
                "id": int(row[0]),
                "event": str(row[1]),
                "msgType": str(row[2]) if not pd.isnull(row[2]) else "",
                "topic": str(row[3]),
                "target": {
                    "type": int(row[4]),
                    "field": str(row[5]) if not pd.isnull(row[5]) else "",
                    "formula": str(row[6]) if not pd.isnull(row[6]) else "",
                }
            }
            result["taskEventConfig"].append(current_base)

    return result


def getCond():
    df1 = df.ffill()
    # print(df1)

    result = {"cond": []}

    for index, row in df1.iterrows():
        if not row.isnull().all():
            cur_cond = {
                "id": int(row[0]),
                "key": str(row[7]),
                "keyType": str(row[8]),
                "formula": str(row[9]) if not pd.isnull(row[9]) else "",
                "expr": str(row[10]),
                "val": str(row[11]),
            }
            result["cond"].append(cur_cond)

    # print(json.dumps(result, indent=2))

    return result


if __name__ == '__main__':
    excel_file_path = './config.xlsx'
    df = pd.read_excel(excel_file_path, skiprows=2, sheet_name=0, header=None)
    baseInfo = getBasInfo()
    print(json.dumps(baseInfo, indent=2))
    print("----------------------------------")

    condRes = getCond()

    # merge all data
    for cond in condRes["cond"]:
        for taskEvt in baseInfo["taskEventConfig"]:
            if taskEvt["id"] == cond["id"]:
                taskEvt.setdefault("cond", []).append(
                    {
                        "key": cond["key"],
                        "keyType": cond["keyType"],
                        "formula": cond["formula"],
                        "expr": cond["expr"],
                        "val": cond["val"],
                    }
                )

    print(json.dumps(baseInfo, indent=2))
