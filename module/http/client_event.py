from ..logger import log


async def event_connect(sid: str, _environ: dict):
    """
    连接事件

    :param sid: session id
    :param _environ: 环境变量
    """
    log.debug(f'client connected: {sid}')
