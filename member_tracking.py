import socketio
import threading
import time
from pynput import mouse, keyboard

class MemberTracking:
    def __init__(self, user_id, server_url="http://172.19.135.113:5000"):
        self.user_id = user_id
        self.server_url = server_url
        
        # reconnection=True ထည့်ထားခြင်းဖြင့် server ခဏပိတ်သွားရင် အလိုအလျောက်ပြန်ချိတ်ပါမယ်
        self.sio = socketio.Client(reconnection=True, reconnection_attempts=0) 
        self.last_activity_time = time.time()
        self.is_running = True
        
        # Socket events setup
        self.setup_socket_events()
        self.connect_to_server()
        self.start_listeners()
        
        # Inactivity check thread
        threading.Thread(target=self.check_inactivity, daemon=True).start()

    def setup_socket_events(self):
        @self.sio.event
        def connect():
            print(f"✅ Connected to tracking server at {self.server_url}")
            # ချိတ်ဆက်မိတာနဲ့ register လုပ်မယ်
            self.sio.emit('register', {'user_id': self.user_id})

        @self.sio.event
        def disconnect():
            print("❌ Disconnected from tracking server")

    def connect_to_server(self):
        """Server ကို ချိတ်ဆက်ခြင်း - error တက်ရင်လည်း app မရပ်သွားအောင် ကာကွယ်ထားသည်"""
        try:
            if not self.sio.connected:
                self.sio.connect(self.server_url, wait_timeout=10)
        except Exception as e:
            print(f"⚠️ Initial Connection Failed: {e}. Will retry automatically...")

    def on_activity(self, *args):
        print("📍 Movement Detected!") 
        
        # Socket ချိတ်မချိတ် စစ်ဆေးတဲ့ code ထည့်ပါ
        if not self.sio.connected:
            print("❌ Socket not connected. Trying to reconnect...")
            self.connect_to_server()
            return

        current_time = time.time()
        if current_time - self.last_activity_time > 5:
            self.last_activity_time = current_time
            try:
                self.sio.emit('status_change', {
                    'user_id': self.user_id, 
                    'status': 'active'
                })
                print(f"📡 Status 'active' sent for User: {self.user_id}")
            except Exception as e:
                print(f"⚠️ Emit Error: {e}")

    # member_tracking.py ထဲတွင် အစားထိုးကြည့်ရန်
    def start_listeners(self):
        print("🖱️ Mouse & Keyboard Listeners Starting...")
        mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        key_listener = keyboard.Listener(on_press=self.on_activity)
        
        mouse_listener.start()
        key_listener.start()
        print("✅ Listeners are Active! Try moving your mouse.")
        
        # Listener တွေ မရပ်သွားအောင် Join လုပ်ထားဖို့လိုသည် (သို့မဟုတ် while loop သုံးရမည်)
        # self.is_running while loop က check_inactivity ထဲမှာ ရှိပြီးသားဖြစ်ရမည်

    def check_inactivity(self):
        """၅ မိနစ် ငြိမ်နေပါက 'away' status သို့ ပြောင်းမည်"""
        while self.is_running:
            time.sleep(5) # ၃၀ စက္ကန့်တစ်ခါ စစ်ဆေးမည်
            inactive_duration = time.time() - self.last_activity_time
            
            if inactive_duration > 30: # ၅ မိနစ် (300 seconds)
                if self.sio.connected:
                    try:
                        self.sio.emit('status_change', {
                            'user_id': self.user_id, 
                            'status': 'away'
                        })
                        print("🟡 Status Sent: Away (Inactivity detected)")
                    except:
                        pass

    def stop(self):
        """App ပိတ်သောအခါ listener များနှင့် connection ကို ဖြတ်ရန်"""
        self.is_running = False
        if self.sio.connected:
            self.sio.disconnect()

# စမ်းသပ်ရန် (Main App ထဲတွင် ထည့်သွင်းအသုံးပြုပုံ)
if __name__ == "__main__":
    # ဥပမာ Employee ID 'E1' ဖြင့် စမ်းသပ်ခြင်း
    tracker = MemberTracking(user_id="E1")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop()