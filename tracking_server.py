import eventlet
import socketio
from database import Database

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
db = Database()

@sio.event
def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.on('register')
def handle_register(sid, data):
    # Member ID နှင့် Socket SID ကို ချိတ်ဆက်သိမ်းဆည်းခြင်း (optional)
    print(f"User {data['user_id']} registered.")

@sio.on('status_change')
def handle_status(sid, data):
    user_id = data['user_id']
    status = data['status']
    
    # Database ထဲသို့ Live Update လုပ်ခြင်း
    db.update_live_status(user_id, status)
    
    # Leader Dashboard များသို့ Real-time သတင်းပို့ခြင်း
    sio.emit('status_update', {'user_id': user_id, 'status': status})

@sio.event
def disconnect(sid):
    print(f"Disconnected: {sid}")

if __name__ == '__main__':
    # သင့်စက်၏ IP တွင် နားထောင်မည်
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)