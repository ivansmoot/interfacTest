"""启动本地接口

    使用FastAPI启动本地接口
    端口返回值通过randomReturn中的get_randomKey方法随机获取
    具体的返回值和相应的概率在prize_probability这个dict中声明

"""


from fastapi import FastAPI
from randomReturn import get_randomKey


server = FastAPI()


@server.get("/lottery")
def lottery():
    return {
        'status': 'success',
        'prize': {
            'stuff': get_randomKey(prize_probability)
        }
    }


prize_probability = {
    'RTX3080': 0.1,
    '三星980 pro': 5,
    '猫头鹰D15S': 10,
    '100元现金奖励': 15,
    '200元代金券': 20,
    '10000元余额宝体验基金': 49.9
}


# server为文件名，app为FastAPI的实例名称
# --reload即热重载
# uvicorn interfaceServer:server --reload --port 6565
