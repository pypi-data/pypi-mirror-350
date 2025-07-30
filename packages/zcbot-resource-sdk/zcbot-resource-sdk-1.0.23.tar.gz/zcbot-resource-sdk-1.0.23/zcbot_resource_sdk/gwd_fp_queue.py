# encoding: utf-8

import json
import random
import logging
from typing import List, Optional, Tuple
from zcbot_web_core.lib import time as time_lib
from zcbot_resource_sdk.common.model import ResCookie
from zcbot_resource_sdk.common.redis_client import SingletonRedis

LOGGER = logging.getLogger('购物党')
rds = SingletonRedis(redis_uri=None, redis_db=None)


def get_settings(biz_id: str) -> dict:
    # 60秒窗口期最多调用10次
    temp = {"expire": 60, "use_times": 10}
    json_str = rds.client.get(f"res:settings:{biz_id}")
    if not json_str:
        return temp
    json_obj = json.loads(json_str)

    temp.update(json_obj)
    return temp


def __is_banded(sn: str):
    """某个cookie是否被禁用"""
    value = rds.client.get(f"res:gwd:banded:{sn}")
    return value == "1"


def __banded_cookie(sn: str, freeze_time: int = 7200):
    """禁用某个cookie"""
    key = f"res:gwd:banded:{sn}"
    rds.client.set(key, "1")
    rds.client.expire(key, freeze_time)


def get_ck_list(origin_key_list: List[str]) -> Tuple[List[Tuple[str, str]], dict]:
    """
    sn_list_key = f"res:cookie:*:gwd:{plat_type}:*"
    乱序返回cookie列表， tuple， (channel, sn)
    :param origin_key_list: redis键
    :return: Tuple[List[Tuple[channel, sn]], dict]
    cookie_map: {sn: redis_key}
    """
    temp = []
    cookie_map = {}
    for key in origin_key_list:
        key_list = key.split(":")
        channel = key_list[2]
        sn = key_list[5]
        temp.append((channel, sn))
        cookie_map[sn] = key

    random.shuffle(temp)
    return temp, cookie_map


def __is_over_times(biz_id: str, sn: str, use_times: int) -> bool:
    """是否超过使用上限"""

    key = f"res:gwd:use:{biz_id}:{sn}:*"
    keys_list = rds.client.keys(key)
    length = len(keys_list)
    return length >= use_times


def get_cookie_info_by_sn(cookie_key: str) -> Tuple[Optional[dict], bool]:
    try:
        cookie_str = rds.client.get(cookie_key)
        return json.loads(cookie_str), True
    except Exception as e:
        return None, False


def build_res_cookie_object(cookie_dict: dict, keys: List[str] = []) -> ResCookie:  # noqa
    res_obj = ResCookie()
    res_obj.sn = cookie_dict.get("sn")
    res_obj.ua = cookie_dict.get("ua")
    res_obj.uid = cookie_dict.get("uid")
    res_obj.phone = cookie_dict.get("phone")

    temp_map = dict()
    cookie_map = cookie_dict.get("cookieMap", {})
    if not keys:
        temp_map = cookie_map
    else:
        for key in keys:
            temp_map[key] = cookie_map.get(key)
    res_obj.cookieMap = temp_map

    return res_obj


def __add_use_time(biz_id: str, cookie_pin: str, expire: int = 60):
    """
    添加一个带有过期时间的key，用以统计短时间内是否达到使用上限
    添加cookie的使用记录，记录时间戳
    :param biz_id:
    :param cookie_pin:
    :param expire: 使用记录的cookie记录
    :return:
    """
    time_stamp = str(time_lib.current_timestamp10())
    key = f"res:gwd:use:{biz_id}:{cookie_pin}:{time_stamp}"
    rds.client.set(key, time_stamp)
    rds.client.expire(key, expire)
    record_key = f"res:gwd:record:{cookie_pin}"
    rds.client.rpush(record_key, time_stamp)


def get_cookie(biz_id: str, keys: List[str] = []) -> Optional[ResCookie]:  # noqa
    """
    根据业务编码获取cookie
    :param biz_id: 业务编号，如：gwd_price
    :param keys: 需要提取的cookie字段，如果为空则获取所有
    :return:
    config: plat_type: str, pc, h5
            expire: int, 使用过期时间
            use_times: 最多使用的次数
            channel: 来源
            freeze_time: 禁用时间，京东默认冻结俩小时
    """
    config = get_settings(biz_id)
    expire = config.get("expire")
    use_times = config.get("use_times")
    channel = config.get("channel")
    plat_type = config.get("plat_type", "pc")

    cookie_queue_key = f'res:cookie:{channel}:gwd:{plat_type}:queue'

    cookie_sn_count = rds.client.llen(cookie_queue_key)
    if cookie_sn_count == 0:
        return None
    idx = 0
    while True:
        idx += 1
        # 遍历一遍了，都没有满足的，直接return None
        if idx > cookie_sn_count:
            return None
        sn = rds.client.rpoplpush(cookie_queue_key, cookie_queue_key)
        if __is_banded(sn):
            continue
        if __is_over_times(biz_id, sn, use_times):
            continue
        cookie_key = f'res:cookie:{channel}:gwd:{plat_type}:{sn}'
        cookie_info, trans_success = get_cookie_info_by_sn(cookie_key)
        if not trans_success:
            continue
        res_obj = build_res_cookie_object(cookie_info, keys)

        __add_use_time(biz_id, sn, expire)
        return res_obj
    return None


def __remove_cookie(sn: str):
    sn_list_key = f"res:cookie:*:gwd:*:{sn}"
    key_list = rds.client.keys(sn_list_key)
    for key_name in key_list:
        rds.client.delete(key_name)
    # 在队列中移除
    keys_name = f"res:cookie:*:gwd:*:queue"
    keys = rds.client.keys(keys_name)
    for key_list_name in keys:
        rds.client.lrem(name=key_list_name, count=0, value=sn)


def remove_cookie(biz_id: str, sn: str, forever: bool = False):
    """
    移除cookie
    """
    config = get_settings(biz_id)
    freeze_time = config.get('freeze_time', 7200)
    if not forever:
        __banded_cookie(sn, freeze_time)
    else:
        # forever == True
        __remove_cookie(sn)


def release_cookie(sn: str):
    """
    把移除的cookie释放，解冻
    """
    rds.client.delete(f"res:gwd:banded:{sn}")


def current_alive(biz_id: str) -> List[str]:
    """
    返回当前可用cookie的sn编码集合
    :return:
    """
    temp = []
    config = get_settings(biz_id)
    expire = config.get("expire")
    use_times = config.get("use_times")
    channel = config.get("channel")
    plat_type = config.get("plat_type", "pc")
    #                       channel     sn
    sn_list_key = f"res:cookie:*:gwd:{plat_type}:*"
    sn_list = rds.client.keys(sn_list_key)
    cookie_list, cookie_map = get_ck_list(sn_list)
    for (cookie_channel, sn) in cookie_list:
        if sn == "queue":
            continue
        if __is_banded(sn):
            continue
        if __is_over_times(biz_id, sn, use_times):
            continue
        # 没有禁用 没有达到使用上限

        # 判断来源是否一致
        if channel != cookie_channel:
            continue

        temp.append(sn)

    return temp


if __name__=="__main__":
    data = get_settings("gwd_fp")
    print(data)