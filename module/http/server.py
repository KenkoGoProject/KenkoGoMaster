from fastapi import FastAPI
from contextlib import asynccontextmanager

from module.logger import log


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 启动时的操作
    log.info('startup')
    yield
    # 将被关闭时的操作
    log.debug('shutdown')


app: FastAPI = FastAPI(lifespan=lifespan)
