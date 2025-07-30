from typing import List, Optional, Dict
from pydantic import BaseModel


class ResCookie(BaseModel):
    """
    cookie对象数据模型
    """
    # 链接序列号（全局唯一）  如：jd:5129155、tmall:576748721316,3985068128611
    sn: str = None
    # 用户唯一编码（用于标识用户，如京东pin码）
    uid: Optional[str] = None
    # user-agent 浏览器
    ua: Optional[str] = None
    # 获取需要的cookie键值对值
    cookieMap: Dict = None
    # 手机号
    phone: Optional[str] = None
    # 代理地址
    proxyHost: Optional[str] = None
    # 代理端口
    proxyPort: Optional[str] = None

