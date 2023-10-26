from module.logger import log
from module.model.client import Client, ClientStatus
from module.model.singleton import SingletonType


class ClientManager(metaclass=SingletonType):
    """客户端管理器"""

    def __init__(self):
        self._clients = {}

    def add(self, sid: str, environ: dict, emit) -> None:
        """添加客户端"""
        self._clients[sid] = Client(sid, environ, emit)
        log.info(f'client {sid} added')
        self._clients[sid].set_status(ClientStatus.CONNECTED)

    def remove(self, sid: str):
        """移除客户端"""
        self._clients.pop(sid, None)
        log.info(f'client {sid} removed')

    def get_client(self, sid: str) -> Client:
        """获取客户端"""
        return self._clients.get(sid, None)
