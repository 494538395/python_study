import math_rule_list

if __name__ == '__main__':
    param = {
        "common_params": {
            "appId": 999
        },
        "nacos_group_id": "offline-match-server"
    }

    gen_template = math_rule_list.gen_template(param)
    print("结果如下")
    print(gen_template)
