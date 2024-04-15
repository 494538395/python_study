import json

import rule_match_mode

if __name__ == '__main__':
    with open("data.json", "r") as file:
        json_data = json.load(file)

    gen_template = rule_match_mode.gen_json(json_data)
    print("结果如下")
    print(gen_template)
