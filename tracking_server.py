import eventlet
import socketio
from database import Database

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
db = Database() # Server မှာ တစ်ခါပဲ ချိတ်ထားမည်

connected_users = {}

@sio.event
def register(sid, data):
    user_id = data.get('user_id')
    if user_id:
        connected_users[sid] = user_id
        db.update_live_status(user_id, 'active') # Server က DB ကို လှမ်းပြင်သည်
        sio.emit('status_update', {'user_id': user_id, 'status': 'active'})
        print(f"👤 User {user_id} registered.")

@sio.event
def status_change(sid, data):
    user_id = data.get('user_id')
    status = data.get('status')
    if user_id and status:
        db.update_live_status(user_id, status) # DB Update
        sio.emit('status_update', {'user_id': user_id, 'status': status})
        print(f"📡 {user_id} is now {status}")

@sio.event
def disconnect(sid):
    if sid in connected_users:
        user_id = connected_users[sid]
        db.update_live_status(user_id, 'offline')
        sio.emit('status_update', {'user_id': user_id, 'status': 'offline'})
        del connected_users[sid]

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    
    