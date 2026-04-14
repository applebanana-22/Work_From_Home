import eventlet
import socketio
from database import Database

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
db = Database()
connected_users = {}

@sio.event
def connect(sid, environ):
    print(f"✅ Connected: {sid}")

@sio.event
def register(sid, data):
    user_id = data.get('user_id')
    connected_users[sid] = user_id
    db.update_live_status(user_id, 'active')
    sio.emit('status_update', {'user_id': user_id, 'status': 'active'})
    print(f"👤 User {user_id} Registered.")

@sio.event
def status_change(sid, data):
    user_id = data.get('user_id')
    status = data.get('status')
    db.update_live_status(user_id, status)
    # Dashboard အားလုံးဆီ status အသစ်ကို တန်းပို့ပေးတယ်
    sio.emit('status_update', {'user_id': user_id, 'status': status})

@sio.event
def disconnect(sid):
    if sid in connected_users:
        user_id = connected_users[sid]
        db.update_live_status(user_id, 'offline')
        sio.emit('status_update', {'user_id': user_id, 'status': 'offline'})
        del connected_users[sid]

if __name__ == '__main__':
    # 0.0.0.0 သုံးထားလို့ Hotspot IP နဲ့ လှမ်းချိတ်လို့ရပါပြီ
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)