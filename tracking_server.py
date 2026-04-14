import eventlet
import socketio
from database import Database

# 1. Socket.IO Setup
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Database instance
db = Database()

# {socket_id: user_id} mapping
connected_users = {}

@sio.event
def connect(sid, environ):
    print(f"✅ Connection Established: {sid}")

@sio.event
def register(sid, data):
    """Member App Login ဝင်ချိန်တွင် Register လုပ်ပေးခြင်း"""
    user_id = data.get('user_id')
    if user_id:
        connected_users[sid] = user_id
        # Database ထဲမှာ 'status' column ကို active လုပ်မယ်
        db.update_live_status(user_id, 'active')
        
        # Leader Dashboard ဆီ signal လှမ်းပို့
        sio.emit('status_update', {'user_id': user_id, 'status': 'active'})
        print(f"👤 User {user_id} Registered and ACTIVE.")

@sio.event
def status_change(sid, data):
    """Mouse/Keyboard movement အရ status ပြောင်းလဲခြင်း"""
    user_id = data.get('user_id')
    status = data.get('status') # 'active' သို့မဟုတ် 'away'
    
    if user_id and status:
        # Database query မှာ column name ကို 'status' လို့ပဲ သုံးဖို့ သတိပြုပါ
        db.update_live_status(user_id, status)
        
        # Leader Dashboard ဆီ status အသစ်ကို ချက်ချင်းပို့
        sio.emit('status_update', {'user_id': user_id, 'status': status})
        print(f"📡 Status Update: {user_id} -> {status}")

@sio.event
def disconnect(sid):
    """Connection ပြတ်သွားလျှင် Offline ပြောင်းခြင်း"""
    if sid in connected_users:
        user_id = connected_users[sid]
        db.update_live_status(user_id, 'offline')
        
        # Dashboard ကို update လုပ်ခိုင်း
        sio.emit('status_update', {'user_id': user_id, 'status': 'offline'})
        print(f"❌ User {user_id} Disconnected and marked OFFLINE.")
        del connected_users[sid]

if __name__ == '__main__':
    print("🚀 Real-time Tracking Server running on port 5000...")
    print("💡 Connect from Client using Server's Hotspot IP.")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)