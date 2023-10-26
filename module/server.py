from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from module.client_event import event_connect, event_disconnect
from module.logger import log


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """生命周期事件"""
    # 启动时的操作
    log.info('startup')
    yield
    # 将被关闭时的操作
    log.debug('shutdown')


app: FastAPI = FastAPI(lifespan=lifespan)  # api框架

# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 日志中间件
@app.middleware('http')
async def log_middleware(request: Request, call_next):
    ip: str = request.client.host
    path_query: str = request.url.path + '?' + request.url.query if request.url.query else request.url.path
    log.debug(f'{ip} {request.method} {path_query}')
    response: Response = await call_next(request)
    log.debug(f'{response.status_code}')
    return response

socket_manager = SocketManager(app=app, mount_location='')  # SocketIO
socket_manager.on('connect', namespace='/client', handler=event_connect)  # 连接事件
socket_manager.on('disconnect', namespace='/client', handler=event_disconnect)  # 断开连接事件
