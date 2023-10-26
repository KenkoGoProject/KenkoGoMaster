from enum import Enum
from typing import Coroutine, Callable

from module.logger import log
from module.sync import sync


class ClientStatus(Enum):
    """客户端状态"""
    DISCONNECTED = 0  # 已断开
    CONNECTED = 1  # 已连接，未注册
    IDLE = 2   # 已注册，暂停调度
    RUNNING = 3  # 已注册，正在调度


class Client:
    """客户端"""

    def __init__(self, sid: str, environ: dict, emit: Callable[[str, any], None]):
        self.sid = sid
        self.environ = environ
        self.status = ClientStatus.DISCONNECTED
        self.emit: Callable[[str, any], None] = emit

    def set_status(self, new_status: ClientStatus):
        """设置客户端状态"""
        self.status = new_status
        log.info(f'client {self.sid} status: {self.status}')

    def auth(self, data: dict) -> bool:
        """认证"""
        log.info(f'client {self.sid} auth: {data}')
        if self.status != ClientStatus.CONNECTED:
            log.error(f'client {self.sid} auth failed: status error')
            self.emit('auth', False)
            return False
        self.set_status(ClientStatus.IDLE)
        log.info(f'client {self.sid} auth ok')
        self.emit('auth', True)
        return True
