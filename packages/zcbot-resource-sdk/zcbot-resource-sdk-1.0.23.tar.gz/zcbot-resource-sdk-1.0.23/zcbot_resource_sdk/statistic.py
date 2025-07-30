import json
import time
import datetime
from zcbot_resource_sdk.common.redis_client import SingletonRedis

rds = SingletonRedis(redis_uri=None, redis_db=None)


def add_api_statistics(biz_id: str, request_total: int, success_total: int, phone: str, sn: str, attach_param: dict = {}, is_success=True, message: str = None):
    # start = time.time()
    success_count = 1
    if not is_success:
        success_count = 0
    day = datetime.datetime.now().strftime('%Y%m%d')
    pipe = rds.client.pipeline()
    pipe.hincrby(name=f'res:got-stat:0000:request-total', key=biz_id, amount=request_total)
    pipe.hincrby(name=f'res:got-stat:0000:request-count', key=biz_id, amount=1)
    pipe.hincrby(name=f'res:got-stat:0000:success-total', key=biz_id, amount=success_total)
    pipe.hincrby(name=f'res:got-stat:0000:success-count', key=biz_id, amount=success_count)
    timestamp = int(time.time() * 1000)
    pipe.hincrby(name=f'res:got-stat:{day}:request-total', key=biz_id, amount=request_total)
    pipe.expire(name=f'res:got-stat:{day}:request-total', time=30 * 86400)
    pipe.hincrby(name=f'res:got-stat:{day}:request-count', key=biz_id, amount=1)
    pipe.expire(name=f'res:got-stat:{day}:request-count', time=30 * 86400)
    pipe.hincrby(name=f'res:got-stat:{day}:success-total', key=biz_id, amount=success_total)
    pipe.expire(name=f'res:got-stat:{day}:success-total', time=30 * 86400)
    pipe.hincrby(name=f'res:got-stat:{day}:success-count', key=biz_id, amount=success_count)
    pipe.expire(name=f'res:got-stat:{day}:success-count', time=30 * 86400)
    param = {
        "phone": phone,
        "sn": sn,
        "requestTotal": request_total,
        "successTotal": success_total,
        "isSuccess": is_success
    }
    if attach_param:
        param.update(attach_param)
    if message:
        param["message"] = message
    pipe.set(name=f'res:got-stat:{day}:detail:{biz_id}:{timestamp}', value=json.dumps(param))
    pipe.expire(name=f'res:got-stat:{day}:detail:{biz_id}:{timestamp}', time=30 * 86400)
    pipe.execute()
    # end = time.time()
    # print(f'add_api_statistics cost: {end - start}s')
