import socketio
import threading
import time
from pynput import mouse, keyboard

# In member_tracking.py
class MemberTracking:
    def __init__(self, user_id, server_url="http://192.168.43.100:5000"): # ပြင်ရန်!
        self.user_id = user_id
        self.server_url = server_url
        self.sio = socketio.Client()
        self.last_activity_time = time.time()
        self.is_running = True
        
        self.connect_to_server()
        self.start_listeners()
        
        # Thread to check for inactivity (e.g., if no movement for 5 minutes)
        threading.Thread(target=self.check_inactivity, daemon=True).start()

    def connect_to_server(self):
        try:
            if not self.sio.connected:
                self.sio.connect(self.server_url)
                self.sio.emit('register', {'user_id': self.user_id})
        except Exception as e:
            print(f"Tracking Server Connection Failed: {e}")

    def on_activity(self, *args):
        """Triggered on any mouse move, click, or key press"""
        current_time = time.time()
        # Throttling: Only send update if 5 seconds passed since last update to save bandwidth
        if current_time - self.last_activity_time > 5:
            self.last_activity_time = current_time
            try:
                self.sio.emit('status_change', {
                    'user_id': self.user_id, 
                    'status': 'active'
                })
            except:
                pass

    def start_listeners(self):
        # Listen for Mouse and Keyboard
        mouse_listener = mouse.Listener(on_move=self.on_activity, on_click=self.on_activity, on_scroll=self.on_activity)
        key_listener = keyboard.Listener(on_press=self.on_activity)
        mouse_listener.start()
        key_listener.start()

    def check_inactivity(self):
        while self.is_running:
            time.sleep(30) # Check every 30 seconds
            if time.time() - self.last_activity_time > 300: # 5 minutes
                try:
                    self.sio.emit('status_change', {
                        'user_id': self.user_id, 
                        'status': 'away'
                    })
                except:
                    pass