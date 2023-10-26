from enum import Enum

from module.logger import log


class ClientStatus(Enum):
    """客户端状态"""
    DISCONNECTED = 0  # 已断开
    CONNECTED = 1  # 已连接，未注册
    IDLE = 2   # 已注册，暂停调度
    RUNNING = 3  # 已注册，正在调度


class Client:
    """客户端"""

    def __init__(self, sid: str, environ: dict):
        self.sid = sid
        self.environ = environ
        self.status = ClientStatus.DISCONNECTED

    def set_status(self, new_status: ClientStatus):
        """设置客户端状态"""
        self.status = new_status
        log.info(f'client {self.sid} status: {self.status}')
