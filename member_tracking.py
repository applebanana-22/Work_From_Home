import socketio
import threading
import time
from pynput import mouse, keyboard

class MemberTracking:
    def __init__(self, user_id, server_url="http://192.168.100.137:5000"):
        self.user_id = user_id
        self.server_url = server_url
        self.sio = socketio.Client(reconnection=True)
        self.last_activity_time = time.time()
        self.is_running = True
        self.last_sent_status = None
        
        # --- အသစ်ထည့်သွင်းထားသော Logic ---
        self.is_active_session = False # Check-in ဝင်မှ True ဖြစ်မည်
        
        self.setup_socket_events()
        self.connect_to_server()
        self.start_listeners()
        
        threading.Thread(target=self.check_inactivity, daemon=True).start()

    def set_tracking_state(self, state: bool):
        """Check-in ဝင်လျှင် True, Check-out ထွက်လျှင် False လှမ်းခေါ်ပေးရန်"""
        self.is_active_session = state
        if not state:
            self.last_sent_status = 'offline' # Session ပိတ်လျှင် status ပြန်သတ်မှတ်
            print("⏸️ Tracking Paused: Outside of working session.")
        else:
            print("▶️ Tracking Active: Working session started.")

    def setup_socket_events(self):
        @self.sio.event
        def connect():
            print(f"✅ Connected to tracking server.")
            self.sio.emit('register', {'user_id': self.user_id})

    def connect_to_server(self):
        try:
            if not self.sio.connected:
                self.sio.connect(self.server_url, transports=['websocket'], wait_timeout=5)
        except:
            pass

    def on_activity(self, *args):
        # Working session မဟုတ်လျှင် ဘာမှဆက်မလုပ်ဘဲ ပြန်ထွက်မည်
        if not self.is_active_session or not self.sio.connected:
            return

        current_time = time.time()
        self.last_activity_time = current_time

        if self.last_sent_status != 'active':
            try:
                self.sio.emit('status_change', {
                    'user_id': self.user_id, 
                    'status': 'active'
                })
                self.last_sent_status = 'active'
                print("🟢 Movement Detected: Sending Active Status")
            except:
                pass

    def start_listeners(self):
        mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity)
        key_listener = keyboard.Listener(on_press=self.on_activity)
        mouse_listener.start()
        key_listener.start()

    def check_inactivity(self):
        while self.is_running:
            time.sleep(10)
            
            # Session မရှိလျှင် inactivity စစ်စရာမလိုပါ
            if not self.is_active_session:
                continue

            inactive_duration = time.time() - self.last_activity_time
            if inactive_duration > 30 and self.last_sent_status != 'away':
                if self.sio.connected:
                    try:
                        self.sio.emit('status_change', {
                            'user_id': self.user_id, 
                            'status': 'away'
                        })
                        self.last_sent_status = 'away'
                        print("🟡 Inactivity Detected: Sending Away Status")
                    except:
                        pass

    def stop(self):
        self.is_running = False
        if self.sio.connected:
            self.sio.disconnect()