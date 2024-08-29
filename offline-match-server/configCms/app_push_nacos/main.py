import app_push_nacos

if __name__ == '__main__':
    param = {
        "AppId": 666,
        "NacosUrl": "http://nacos-headless.pub-prod-nacos.svc.cluster.local:8848",
        "NacosGroup": 'msg-main-road',
        'NacosNamespace':'base-common-service'
    }

    app_push_nacos.gen_app_config(param)
