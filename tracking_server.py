import eventlet
import socketio
from database import Database

# 1. Socket.IO Setup
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Database instance ကို initialize လုပ်ပါ
db = Database()

# ဘယ်သူတွေ connect လုပ်ထားသလဲ သိနိုင်ရန် {socket_id: user_id}
connected_users = {}

@sio.event
def connect(sid, environ):
    print(f"✅ Connection Established: {sid}")

@sio.event
def disconnect(sid):
    if sid in connected_users:
        user_id = connected_users[sid]
        # Database ထဲတွင် status ကို offline ပြောင်းပါ
        db.update_live_status(user_id, 'offline')
        print(f"❌ User {user_id} disconnected and marked OFFLINE.")
        
        # Leader Dashboard ဆီသို့ refresh လုပ်ရန် signal ပို့ပါ
        sio.emit('status_update', {'user_id': user_id, 'status': 'offline'})
        del connected_users[sid]

@sio.event
def register(sid, data):
    """Member app login ဝင်ချိန်တွင် လှမ်းခေါ်သော function"""
    user_id = data.get('user_id')
    connected_users[sid] = user_id
    db.update_live_status(user_id, 'active')
    print(f"👤 User {user_id} is now ACTIVE.")
    
    # Leader Dashboard များသို့ status အသစ်ကို ဖြန့်ဝေပါ
    sio.emit('status_update', {'user_id': user_id, 'status': 'active'})

@sio.event
def status_change(sid, data):
    """Mouse/Keyboard လှုပ်ရှားမှုအပေါ် မူတည်ပြီး status ပြောင်းလဲခြင်း"""
    user_id = data.get('user_id')
    status = data.get('status') # 'active' သို့မဟုတ် 'away'
    
    db.update_live_status(user_id, status)
    print(f"📡 Update: User {user_id} -> {status}")
    
    # Dashboard များသို့ လှမ်းပို့ပါ
    sio.emit('status_update', {'user_id': user_id, 'status': status})

if __name__ == '__main__':
    # 0.0.0.0 သည် Network အတွင်းရှိ မည်သည့် IP မှမဆို လှမ်းချိတ်နိုင်ရန် ဖြစ်သည်
    print("🚀 Real-time Tracking Server is starting on port 5000...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)