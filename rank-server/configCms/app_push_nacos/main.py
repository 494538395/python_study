import app_push_nacos

if __name__ == '__main__':
    param = {
        "AppId": 666,
        "NacosUrl": "http://10.0.1.84:38848",
        "NacosGroup": 'room-server',
        "NacosNamespace": "base-common-service"
    }



    app_push_nacos.gen_app_config(param)
