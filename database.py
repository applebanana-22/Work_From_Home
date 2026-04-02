import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="wfh_system"
        )
        # dictionary=True results in {'column': value}
        self.cursor = self.conn.cursor(dictionary=True)

    def authenticate(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_status_counts(self):
        try:
            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'Office'")
            office_count = self.cursor.fetchone()['count']

            self.cursor.execute("SELECT COUNT(*) as count FROM users WHERE current_status = 'WFH'")
            wfh_count = self.cursor.fetchone()['count']

            return office_count, wfh_count
        except Exception as e:
            print(f"Error counting status: {e}")
            return 0, 0
        
    def get_all_teams(self):
        try:
            self.cursor.execute("SELECT team_id, team_name FROM teams")
            return self.cursor.fetchall() 
        except Exception as e:
            print(f"Database Error: {e}")
            return []

    def create_team(self, name):
        try:
            self.cursor.execute("INSERT INTO teams (team_name) VALUES (%s)", (name,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating team: {e}")
            return False

    def update_team(self, team_id, new_name):
        try:
            self.cursor.execute("UPDATE teams SET team_name = %s WHERE team_id = %s", (new_name, team_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating team: {e}")
            return False

    def delete_team(self, team_id):
        try:
            self.cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting team: {e}")
            return False