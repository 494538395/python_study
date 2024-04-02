import json

import rule_script

if __name__ == '__main__':
    with open("data.json", "r") as file:
        json_data = json.load(file)

    transformed_data = rule_script.gen_json(json_data)
    print("结果如下")
    print(transformed_data)
