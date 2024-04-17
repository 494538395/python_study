import app_push_nacos

if __name__ == '__main__':
    param = {
        "AppId": 8885,
        "NacosUrl": "http://nacos.89tgame.com:82",
        "NacosGroup": 'rank-server',
        "NacosNamespace": "base-common-service"
    }



    app_push_nacos.gen_app_config(param)
