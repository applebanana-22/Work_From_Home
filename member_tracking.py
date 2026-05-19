import socketio
import threading
import time
from pynput import mouse, keyboard

class MemberTracking:
    def __init__(self, user_id, server_url="http://192.168.100.83:5000"):
        self.user_id = user_id
        self.server_url = server_url
        self.sio = socketio.Client(reconnection=True)
        self.last_activity_time = time.time()
        self.is_running = True
        self.last_sent_status = None
        
        self.is_active_session = False 
        
        self.setup_socket_events()
        self.connect_to_server()
        self.start_listeners()
        
        threading.Thread(target=self.check_inactivity, daemon=True).start()

    def set_tracking_state(self, state: bool):
        """
        Check-in ဝင်လျှင် True (Active) ပို့မည်။
        Check-out ထွက်လျှင် False (Offline) ပို့မည်။
        """
        self.is_active_session = state
        
        if not state:
            # Check-out လုပ်လိုက်တဲ့အချိန်မှာ Server ကို Offline ဖြစ်ကြောင်း ချက်ချင်း အကြောင်းကြားရပါမယ်
            if self.sio.connected:
                try:
                    self.sio.emit('status_change', {
                        'user_id': self.user_id, 
                        'status': 'offline'
                    })
                    self.last_sent_status = 'offline'
                    print("🔴 Check-out: Sending Offline Status")
                except:
                    pass
            print("⏸️ Tracking Paused: Outside of working session.")
        else:
            # Check-in ဝင်လိုက်လျှင် Active ဖြစ်ကြောင်း အကြောင်းကြားမည်
            self.last_activity_time = time.time() # Reset activity time
            self.on_activity() # Trigger active status immediately
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
        # Session မရှိလျှင် သို့မဟုတ် Connect မဖြစ်လျှင် ဘာမှမလုပ်ပါ
        if not self.is_active_session or not self.sio.connected:
            return

        current_time = time.time()
        self.last_activity_time = current_time

        # Status က 'active' မဟုတ်သေးမှသာ အသစ်ပို့မည်
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
            
            # Session မရှိလျှင် သို့မဟုတ် Offline ဖြစ်နေလျှင် စစ်စရာမလိုပါ
            if not self.is_active_session or self.last_sent_status == 'offline':
                continue

            inactive_duration = time.time() - self.last_activity_time
            
            # 30 seconds ထက်ကျော်လျှင် Away ပို့မည်
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
        # Program ပိတ်ချိန်တွင် Offline ပို့ပေးခြင်း
        self.set_tracking_state(False)
        self.is_running = False
        if self.sio.connected:
            self.sio.disconnect()