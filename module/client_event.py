from module.logger import log
from module.manager import ClientManager

client_manager = ClientManager()


async def event_connect(sid: str, _environ: dict):
    """
    连接事件

    :param sid: session id
    :param _environ: 环境变量
    """
    log.debug(f'socket.io client connected: {sid}')
    client_manager.add(sid, _environ)


async def event_disconnect(sid: str):
    """
    断开连接事件

    :param sid: session id
    """
    log.debug(f'socket.io client disconnected: {sid}')
    client_manager.remove(sid)
