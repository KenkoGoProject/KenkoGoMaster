from typing import Callable, Coroutine

from fastapi_socketio import SocketManager as _SocketManager
from module.logger import log
from module.client_manager import ClientManager
from module.sync import sync


class SocketManager(_SocketManager):
    def __init__(self, app):
        super().__init__(app=app, mount_location='')
        self.client_manager = ClientManager()
        self.on('connect', namespace='/client', handler=self.event_connect)
        self.on('disconnect', namespace='/client', handler=self.event_disconnect)
        self.on('auth', namespace='/client', handler=self.event_auth)

    def create_emit_method(self, sid: str) -> Callable[[str, any], None]:
        """为客户端创建emit方法"""
        def emit(event: str, data: any) -> None:
            return sync(self.emit(event, data, to=sid, namespace='/client'))

        return emit

    async def event_connect(self, sid: str, _environ: dict):
        """
        连接事件

        :param sid: session id
        :param _environ: 环境变量
        """
        log.debug(f'socket.io client connected: {sid}')
        self.client_manager.add(sid, _environ, self.create_emit_method(sid))

    async def event_disconnect(self, sid: str):
        """
        断开连接事件

        :param sid: session id
        """
        log.debug(f'socket.io client disconnected: {sid}')
        self.client_manager.remove(sid)

    async def event_auth(self, sid: str, data: dict):
        """
        认证事件

        :param sid: session id
        :param data: 认证数据
        """
        client = self.client_manager.get_client(sid)
        if client is None:
            log.error(f'client {sid} not found')
            return
        if client.auth(data):
            log.debug(f'client {sid} authenticated')
        else:
            log.error(f'client {sid} authentication failed')
