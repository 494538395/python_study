import sys

import redis

from nacos import NacosClient

# Redis
REDIS_HOST = '10.0.1.71'
REDIS_PORT = 6379
REDIS_DB = 7

# Nacos
SERVER_ADDRESS = "10.0.1.84:38848"  # 服务器地址,多台需要用,隔开
GROUP_ID = 'event-center-v2'
NAMESPACE = 'public'
LOG_DIR = '../nacos/log'


def init_redis_client():
    redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    return redis_db


def init_nacos_client():
    nacos_client = NacosClient(server_addresses=SERVER_ADDRESS, namespace=NAMESPACE, logDir=LOG_DIR)
    return nacos_client


def genTaskGroupDataId(app_id):
    return str(app_id) + "_task_group_config"


# 领奖
def taskClaim(app_id, object_id, task_group_id, period_id, task_id, claim_prog):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_group_id == 0 or period_id == 0 or task_id == 0 or claim_prog == 0:
        error_message = f"taskClaim, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskGroupId,periodId,taskId.claimProg"
        raise Exception(error_message)

    # 拼接 key
    key = f"evt:mt:{int(app_id)}:{int(task_group_id)}:{int(period_id)}:{{{object_id}}}"
    # 拼接 field
    rsField = f"rs_{int(task_id)}"
    # 写库
    redis_db.hset(key, rsField, int(claim_prog))


# 设任务进度
def setTaskProgress(app_id, object_id, task_group_id, period_id, task_id, progress, expire):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_group_id == 0 or period_id == 0 or task_id == 0 or progress == 0:
        error_message = f"setTaskProgress, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskGroupId,periodId,taskId.progress\n" \
                        f"可选参数：expire"
        raise Exception(error_message)

    # 拼接 key
    key = f"evt:mt:{int(app_id)}:{int(task_group_id)}:{int(period_id)}:{{{object_id}}}"
    # 拼接 field
    prField = f"pr_{int(task_id)}"
    # 写库
    redis_db.hset(key, prField, int(progress))
    # 设置过期时间
    if int(expire) > 0:
        redis_db.expire(key, int(expire))


# 设全局任务进度
def setGlobalTaskProgress(app_id, object_id, task_id, progress):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_id == 0 or progress == 0:
        error_message = f"setGlobalTaskProgress, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskId.progress"
        raise Exception(error_message)

    # 拼接 key
    key = f"evt:global:{int(app_id)}:{int(task_id)}:{{{object_id}}}"
    # 写库
    redis_db.set(key, int(progress))


# 设任务池
def setTaskPool(app_id, object_id, task_group_id, period_id, task_pool, expire):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_group_id == 0 or period_id == 0 or task_pool == "":
        error_message = f"setTaskPool, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskGroupId,periodId.taskPool\n" \
                        f"可选参数：expire"
        raise Exception(error_message)

    # 拼接 key
    poolKey = f"evt:tk:{int(app_id)}:{int(task_group_id)}:{int(period_id)}:{{{object_id}}}"
    # 删除之前的数据
    redis_db.delete(poolKey)

    # 切分数据
    task_list = task_pool.split(',')
    # 写库
    redis_db.sadd(poolKey, *task_list)
    # 设置过期时间
    if int(expire) > 0:
        redis_db.expire(key, int(expire))


# 设任务完成标记
def setTaskGroupFinish(app_id, object_id, task_group_id, period_id):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_group_id == 0 or period_id == 0:
        error_message = f"setTaskGroupFinish, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskGroupId,periodId\n"
        raise Exception(error_message)

    # 拼接 key
    key = f"evt:mt:{int(app_id)}:{int(task_group_id)}:{int(period_id)}:{{{object_id}}}"
    # 拼接属性
    finishField = "group_finish"
    # 写库
    redis_db.hset(key, finishField, "true")


# 设已替换任务次数、已替换任务列表
def setReplaceCountAndList(app_id, object_id, task_group_id, period_id, replace_count, replace_list):
    # 初始化 Redis client
    redis_db = init_redis_client()
    # 参数校验
    if app_id == 0 or object_id == 0 or task_group_id == 0 or period_id == 0 or replace_count == 0 or replace_list == "":
        error_message = f"setReplaceCountAndList, 参数异常\n" \
                        f"请传入指定的参数：\n" \
                        f"必要参数：appId,objectId,taskGroupId,periodId,replaceCount,replaceList\n"
        raise Exception(error_message)

    # 拼接 key
    key = f"evt:mt:{int(app_id)}:{int(task_group_id)}:{int(period_id)}:{{{object_id}}}"

    # 设置已替换任务次数
    replaceCountField = f"replace_count"
    redis_db.hset(key, replaceCountField, int(replace_count))

    # 设置已替换任务列表
    replaceListField = f"replace_list"
    redis_db.hset(key, replaceListField, replace_list)


if __name__ == "__main__":
    client = init_nacos_client()
    content = client.get_config(data_id=genTaskGroupDataId(str('888')), group=GROUP_ID)

    client.publish_config(data_id=genTaskGroupDataId(str('1234')), group=GROUP_ID,  content='nihao')

    # 获取传入的参数
    args = sys.argv[1:]

    # 解析参数为字典形式
    params = {}
    for arg in args:
        key, value = arg.split("=")
        params[key] = value

    # 根据参数执行不同的逻辑
    if "funcType" in params:
        if params["funcType"] == "taskClaim":
            print("领奖")
            taskClaim(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskGroupId", 0)),
                int(params.get("taskId", 0)),
                int(params.get("periodId", 0)),
                int(params.get("claimProg", 0))
            )
        elif params["funcType"] == "setTaskProgress":
            print("设置任务进度")
            setTaskProgress(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskGroupId", 0)),
                int(params.get("taskId", 0)),
                int(params.get("periodId", 0)),
                int(params.get("progress", 0)),
                int(params.get("expire", 0))
            )
        elif params["funcType"] == "setGlobalTaskProgress":
            print("设置全局任务进度")
            setGlobalTaskProgress(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskId", 0)),
                int(params.get("progress", 0))
            )
        elif params["funcType"] == "setTaskPool":
            print("设置任务池")
            setTaskPool(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskGroupId", 0)),
                int(params.get("periodId", 0)),
                params.get("taskPool", ""),
                int(params.get("expire", 0))
            )
        elif params["funcType"] == "setTaskGroupFinish":
            print("设置任务组完成标记")
            setTaskGroupFinish(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskGroupId", 0)),
                int(params.get("periodId", 0)),
            )
        elif params["funcType"] == "setReplaceCountAndList":
            print("设置已替换任务次数、已替换任务列表")
            setReplaceCountAndList(
                int(params.get("appId", 0)),
                params.get("objectId", ""),
                int(params.get("taskGroupId", 0)),
                int(params.get("periodId", 0)),
                int(params.get("replaceCount", 0)),
                params.get("replaceList", ""),
            )
        else:
            error_message = f"请指名具体的操作类型, 当前类型是={params['funcType']}。" \
                            f"支持的类型有:setTaskProgress、setGlobalTaskProgress、" \
                            f"setTaskPool、setTaskGroupFinish、setReplaceCountAndList"
            print(error_message)
            raise Exception(error_message)

else:
    error_message = f"没有操作类型方法,请传入 funcType 参数"
    print(error_message)
    raise Exception(error_message)
