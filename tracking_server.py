import eventlet
import socketio
import mysql.connector
from datetime import datetime

# 1. Socket.IO Server Setup
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# 2. Database Connection Function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",      # XAMPP run ထားသော စက်ဖြစ်ပါက localhost ထားပါ
            user="root",
            password="",           # XAMPP default password သည် အလွတ်ဖြစ်သည်
            database="wfh_system"
        )
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# Dictionary to keep track of connected users {sid: user_id}
connected_users = {}

@sio.event
def connect(sid, environ):
    print(f"✅ Client Connected: {sid}")

@sio.event
def disconnect(sid):
    if sid in connected_users:
        user_id = connected_users[sid]
        update_db_status(user_id, 'offline')
        print(f"❌ User {user_id} disconnected.")
        del connected_users[sid]
        # Notify leaders that a user went offline
        sio.emit('status_update', {'user_id': user_id, 'status': 'offline'})

@sio.event
def register(sid, data):
    """Member login ဝင်ချိန်တွင် socket နှင့် user_id ကို ချိတ်ဆက်ပေးခြင်း"""
    user_id = data.get('user_id')
    connected_users[sid] = user_id
    update_db_status(user_id, 'active')
    print(f"👤 User {user_id} registered and marked as ACTIVE.")
    sio.emit('status_update', {'user_id': user_id, 'status': 'active'})

@sio.event
def status_change(sid, data):
    """Member ဘက်မှ mouse/keyboard လှုပ်ရှားမှုရှိပါက status ပြောင်းပေးခြင်း"""
    user_id = data.get('user_id')
    status = data.get('status') # 'active' or 'away'
    
    update_db_status(user_id, status)
    print(f"📡 Status Update: User {user_id} is now {status}")
    
    # Leader Dashboard များဆီသို့ အချက်အလက်ဖြန့်ဝေခြင်း
    sio.emit('status_update', {'user_id': user_id, 'status': status})

def update_db_status(user_id, status):
    """Database ထဲရှိ users table တွင် status ကို တိုက်ရိုက် update လုပ်ခြင်း"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE users SET status = %s WHERE id = %s"
            cursor.execute(sql, (status, user_id))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"⚠️ SQL Update Error: {e}")

if __name__ == '__main__':
    print("🚀 Tracking Server is starting on port 5000...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)