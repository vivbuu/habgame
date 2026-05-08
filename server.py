import asyncio, json
from aiohttp import web
import socketio

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

players = {}

@sio.event
async def connect(sid, environ):
    players[sid] = {'x': 100, 'y': 200}
    await sio.emit('init', {'id': sid, 'x': 100, 'y': 200}, to=sid)
    await sio.emit('join', {'id': sid, 'x': 100, 'y': 200}, skip_sid=sid)

@sio.event
async def move(sid, data):
    if sid in players:
        players[sid] = {'x': data['x'], 'y': data['y']}
        await sio.emit('move', {'id': sid, 'x': data['x'], 'y': data['y']}, skip_sid=sid)

@sio.event
async def disconnect(sid):
    if sid in players:
        del players[sid]
        await sio.emit('leave', {'id': sid})

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
