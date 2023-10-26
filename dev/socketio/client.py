# noinspection PyPackageRequirements
from socketio import Client

sio: Client = Client()
namespace: str = '/client'


# 封装sio.on装饰器，固定namespace
def on(event: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        sio.on(event, namespace=namespace)(wrapper)
        return wrapper

    return decorator


@on('connect')
def connect():
    print('connection established')
    sio.emit('auth', 'thanks', namespace=namespace)


@on('auth')
def recv_auth(data: bool):
    print(f'auth result: {data}')


@on('disconnect')
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:17680')
sio.wait()
