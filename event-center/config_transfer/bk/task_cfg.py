import pandas as pd
import json


def getBasInfo():
    result = {"taskConfig": []}

    for index, row in df.iterrows():
        current_base = {
            "id": int(row[0]),
            "isGlobal": bool(row[1]),
            "taskEventId": int(row[2]),
            "updateMode": str(row[3]),
            "ex": str(row[4]) if not pd.isnull(row[4]) else ""
        }
        result["taskConfig"].append(current_base)

    return result


if __name__ == '__main__':
    excel_file_path = 'config.xlsx'
    df = pd.read_excel(excel_file_path, skiprows=1, sheet_name=1, header=None)
    baseInfo = getBasInfo()
    print(json.dumps(baseInfo, indent=2))
