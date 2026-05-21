import mysql.connector
from datetime import datetime

class Database:
    def __init__(self, host="192.168.100.45"):
        self.host = host
        self.connect()

    def connect(self):
        """Database ချိတ်ဆက်မှုကို စတင်ပြုလုပ်ခြင်း"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host, 
                user="root",
                password="",  
                database="wfh_system",
                autocommit=True,
                connect_timeout=10 
            )
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            print(f"✅ Successfully connected to XAMPP Database at {self.host}")
        except mysql.connector.Error as err:
            print(f"❌ Database Connection Error: {err}")
            self.conn = None

    def ensure_connection(self):
        """Connection ရှိမရှိ စစ်ဆေးပြီး ပြတ်နေပါက ပြန်ချိတ်ပေးမည် (အရေးကြီးဆုံးအပိုင်း)"""
        try:
            if self.conn and self.conn.is_connected():
                # reconnect=True ကို mysql-connector တွင် ဤသို့သုံးပါသည်
                self.conn.ping(reconnect=True, attempts=3, delay=1)
            else:
                print("🔄 Connection lost. Reconnecting...")
                self.connect()
        except Exception:
            self.connect()

    # --- Authentication ---
    def authenticate(self, username, password):
        self.ensure_connection() # Query မတိုင်ခင် အမြဲစစ်ပါ
        if not self.conn: return None
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Authentication Error: {e}")
            return None

    # --- Attendance ---
    def check_in_user(self, user_id, location):
        self.ensure_connection()
        if not self.conn: return False
        today = datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.now().strftime('%H:%M:%S')
        try:
            sql_att = "INSERT INTO attendance (user_id, attendance_date, check_in, location_type) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql_att, (user_id, today, now_time, location))
            
            # Sync with users table and wfh_schedules to ensure dashboard counts are accurate
            self.update_user_status(user_id, location)
            return True
        except Exception as e:
            print(f"Check-in Error: {e}")
            return False

    def update_user_status(self, user_id, status):
        """Update user's current status and sync with wfh_schedules for today"""
        self.ensure_connection()
        try:
            # 1. Update users table for real-time tracking
            query_user = "UPDATE users SET current_status = %s WHERE id = %s"
            self.cursor.execute(query_user, (status, user_id))
            
            # 2. Sync with wfh_schedules for today (this ensures dashboard counts match the schedule log)
            self.cursor.execute("SELECT id FROM wfh_schedules WHERE user_id = %s AND schedule_date = CURDATE()", (user_id,))
            sched = self.cursor.fetchone()
            
            if sched:
                # Update existing schedule entry for today
                self.cursor.execute("UPDATE wfh_schedules SET status = %s WHERE id = %s", (status, sched['id']))
            else:
                # Create a schedule entry for today if it doesn't exist (e.g. for Leaders or unplanned activity)
                self.cursor.execute("""
                    INSERT INTO wfh_schedules (user_id, leader_id, schedule_date, status) 
                    VALUES (%s, %s, CURDATE(), %s)
                """, (user_id, user_id, status))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Status sync error: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        
    def get_all_teams(self):
        """Team အားလုံးကို database ထဲမှ ဆွဲထုတ်ရန်"""
        try:
            self.cursor.execute("SELECT * FROM teams")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching teams: {e}")
            return []
        
    def get_team_name(self, team_id):
        """Fetch team name from team_id"""
        try:
            self.cursor.execute("SELECT team_name FROM teams WHERE team_id = %s", (team_id,))
            row = self.cursor.fetchone()
            return row['team_name'] if row else None
        except Exception as e:
            print(f"Get team name error: {e}")
            return None
    
    def get_status_counts(self):
        """Fetch real-time counts for all employees in the company using today's schedule"""
        try:
            self.ensure_connection()
            # This query ensures all user accounts are counted.
            # It prioritizes today's entry in wfh_schedules, falls back to current_status,
            # and defaults to 'Office' if neither is set.
            query = """
                SELECT 
                    SUM(CASE WHEN status = 'Office' THEN 1 ELSE 0 END) as office_count,
                    SUM(CASE WHEN status = 'WFH' THEN 1 ELSE 0 END) as wfh_count
                FROM (
                    SELECT 
                        COALESCE(s.status, u.current_status, 'Office') as status
                    FROM users u
                    LEFT JOIN wfh_schedules s ON u.id = s.user_id AND s.schedule_date = CURDATE()
                ) t
            """
            self.cursor.execute(query)
            res = self.cursor.fetchone()
            office_count = int(res['office_count'] or 0)
            wfh_count = int(res['wfh_count'] or 0)

            return office_count, wfh_count
        except Exception as e:
            print(f"Error counting status: {e}")
            return 0, 0
        
    def check_out_user(self, user_id):
        """Attendance table တွင် check_out အချိန်ကို update လုပ်ပြီး 
           users table တွင် live status ကို offline ပြောင်းရန်"""
        try:
            self.ensure_connection()
            
            # ၁။ Attendance Table ကို Update လုပ်ခြင်း (ယနေ့အတွက်)
            query_attendance = """
                UPDATE attendance 
                SET check_out = CURTIME() 
                WHERE user_id = %s AND attendance_date = CURDATE() 
                AND check_out IS NULL
            """
            self.cursor.execute(query_attendance, (user_id,))
            
            # ၂။ Users Table ရှိ live status ကို offline ပြောင်းခြင်း
            query_user = "UPDATE users SET status = 'offline' WHERE id = %s"
            self.cursor.execute(query_user, (user_id,))
            
            self.conn.commit()
            print(f"✅ User ID {user_id} checked out successfully.")
            return True
        except Exception as e:
            print(f"❌ Check-out Error: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    # --- Live Tracking Update ---
    def update_live_status(self, user_id, status):
        """tracking_server မှ လှမ်းခေါ်သော function"""
        self.ensure_connection() # အမြဲစစ်ပေးခြင်းဖြင့် connection timeout ကို ကာကွယ်သည်
        if not self.conn: return
        try:
            query = "UPDATE users SET status = %s WHERE id = %s OR employee_id = %s"
            self.cursor.execute(query, (status, user_id, user_id))
            print(f"💾 DB Updated: {user_id} -> {status}")
        except Exception as e:
            print(f"DB Status Update Error: {e}")
            
    # def insert_reply(self, announcement_id, user, message):
    #     """
    #     Insert a reply into the announcement_replies table.
    #     """
    #     try:
    #         query = """
    #             INSERT INTO announcement_replies
    #             (announcement_id, message, created_by, created_at)
    #             VALUES (%s, %s, %s, NOW())
    #         """
    #         self.cursor.execute(
    #             query,
    #             (announcement_id, message, user['full_name'])
    #         )
    #         self.conn.commit()
    #     except Exception as e:
    #         self.conn.rollback()
    #         raise e
    
    def insert_reply(self, announcement_id, user, reply_text):
        self.cursor.execute("""
            INSERT INTO announcement_replies
            (announcement_id, message, created_by, user_id, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        """, (
            announcement_id,
            reply_text,
            user["full_name"],
            user["id"]
        ))
        self.conn.commit()
    
    def create_team(self, team_name, desccription):

        query = """
        INSERT INTO teams (team_name, description)
        VALUES (%s, %s)
        """

        values = (team_name, desccription)

        self.cursor.execute(query, values)
        self.conn.commit()

        return True

    def update_team(self, team_id, team_name, description):

        query = """
        UPDATE teams
        SET team_name=%s,
            description=%s
        WHERE team_id=%s
        """

        self.cursor.execute(
            query,
            (team_name, description, team_id)
        )

        self.conn.commit()

        return self.cursor.rowcount > 0

    def delete_team(self, team_id):
        try:
            self.cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting team: {e}")
            return False
            
    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("🔌 Database connection closed.")
        except Exception as e:
            print(f"Error closing database: {e}")