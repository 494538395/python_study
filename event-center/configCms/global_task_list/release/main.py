import global_task_list

if __name__ == '__main__':
    param = {
        "common_params": {
            "appId": 666
        },
        "nacos_group_id": "cms-event-center"
    }

    gen_template = global_task_list.gen_template(param)
    print("结果如下")
    print(gen_template)
