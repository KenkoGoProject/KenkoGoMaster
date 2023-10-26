# noinspection PyPackageRequirements
from socketio import Client

sio: Client = Client()
namespace: str = '/client'


@sio.on('connect', namespace=namespace)
def connect():
    print('connection established')
    sio.emit('$client_msg', 'thanks', namespace=namespace)


@sio.on('$server_msg')
def my_message(data: any):
    print(f'message received: {data}')


@sio.on('disconnect')
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:17680')
sio.wait()
