import math_filed_list

if __name__ == '__main__':
    # param = {
    #     "common_params": {
    #         "appId": 999
    #     },
    #     "nacos_group_id": "offline-match-server"
    # }

    param = {}

    gen_template = math_filed_list.gen_template(param)
    print("结果如下")
    print(gen_template)
