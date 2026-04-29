import customtkinter as ctk
from database import Database
from tkinter import messagebox, simpledialog
from datetime import datetime

class MemberOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Login ဝင်ထားသော Member data

        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Segmented button
        self.grid_rowconfigure(2, weight=1)  # Content frame
        self.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=120, pady=20)
        
        ctk.CTkLabel(
            header, 
            text="Overtime Management", 
            font=("Arial", 22, "bold")
        ).pack(side="left")

        # --- Segmented Button for Tab Selection ---
        self.segmented_btn = ctk.CTkSegmentedButton(
            self,
            values=["📋 Pending Requests", "📜 History"],
            command=self.on_tab_change,
            font=("Arial", 13, "bold"),
            fg_color="#1E1E1E",
            selected_color="#2B5B84",
            unselected_color="#333333",
            text_color="white",
            corner_radius=12,
            height=40
        )
        self.segmented_btn.grid(row=1, column=0, sticky="ew", padx=120, pady=10)
        self.segmented_btn.set("📋 Pending Requests")  # Set default tab

        # --- Content Frame (changes based on selected tab) ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=120, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frames for both tabs
        self.pending_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#121212",
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A"
        )
        
        self.history_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="#121212",
            corner_radius=12,
            border_width=1,
            border_color="#2A2A2A"
        )

        # Initial data load
        self.refresh_all_data()
        
        # Show default tab
        self.show_pending_tab()

    def on_tab_change(self, value):
        """Handle tab/segmented button change"""
        if value == "📋 Pending Requests":
            self.show_pending_tab()
        elif value == "📜 History":
            self.show_history_tab()

    def show_pending_tab(self):
        """Show pending requests tab"""
        # Hide history frame, show pending frame
        self.history_frame.grid_forget()
        self.pending_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.refresh_pending_requests()

    def show_history_tab(self):
        """Show history tab"""
        # Hide pending frame, show history frame
        self.pending_frame.grid_forget()
        self.history_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.refresh_history()

    def refresh_all_data(self):
        """Refresh both tabs"""
        self.refresh_pending_requests()
        self.refresh_history()

    def refresh_pending_requests(self):
        """Show pending OT requests from leader"""
        for w in self.pending_frame.winfo_children():
            w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime_requests o 
            JOIN projects p ON o.project_id = p.id 
            WHERE o.member_id = %s AND o.status = 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(
                    self.pending_frame, 
                    text="✨ No pending requests from leader.",
                    text_color="gray",
                    font=("Arial", 14)
                ).pack(expand=True, fill="both", pady=50)
                return

            # Show count badge
            count_frame = ctk.CTkFrame(self.pending_frame, fg_color="transparent")
            count_frame.pack(fill="x", pady=(10, 5), padx=10)
            
            ctk.CTkLabel(
                count_frame,
                text=f"📬 You have {len(rows)} pending request(s)",
                font=("Arial", 12, "bold"),
                text_color="#3498DB"
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.pending_frame,
                    fg_color=("#2B2B2B", "#1E1E1E"),
                    corner_radius=10,
                    border_width=1,
                    border_color="#3D5166"
                )
                card.pack(fill="x", pady=8, padx=10)

                # Content
                content_frame = ctk.CTkFrame(card, fg_color="transparent")
                content_frame.pack(fill="x", padx=15, pady=12)

                # Project and Date row
                top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
                top_row.pack(fill="x", pady=(0, 8))
                
                ctk.CTkLabel(
                    top_row,
                    text=f"📁 {r['project_name']}",
                    font=("Arial", 13, "bold"),
                    text_color="#4A90E2"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row,
                    text=f"📅 {r['ot_date']}",
                    font=("Arial", 11),
                    text_color="gray"
                ).pack(side="right")

                # Hours and Details
                details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                details_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    details_frame,
                    text=f"⏳ Duration: {r['hours']} hours",
                    font=("Arial", 12)
                ).pack(anchor="w")

                # Leader's reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=("#252525", "#2A2A2A"), corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text="💬 Leader's Request:",
                        font=("Arial", 11, "bold"),
                        text_color="#F39C12"
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Buttons
                btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                btn_frame.pack(fill="x", pady=(12, 0))
                
                ctk.CTkButton(
                    btn_frame, 
                    text="✓ Accept", 
                    width=100,
                    height=35,
                    fg_color="#27AE60", 
                    hover_color="#1E8449",
                    font=("Arial", 12, "bold"),
                    command=lambda id=r['id']: self.update_status(id, 'Accepted')
                ).pack(side="left", padx=(0, 10))
                
                ctk.CTkButton(
                    btn_frame, 
                    text="✗ Reject", 
                    width=100,
                    height=35,
                    fg_color="#E74C3C", 
                    hover_color="#C0392B",
                    font=("Arial", 12, "bold"),
                    command=lambda id=r['id']: self.handle_reject(id)
                ).pack(side="left")

        except Exception as e:
            print(f"Error loading pending requests: {e}")
            messagebox.showerror("Error", f"Could not load requests: {e}")

    def refresh_history(self):
        """Show OT request history (non-pending)"""
        for w in self.history_frame.winfo_children():
            w.destroy()
        
        query = """
            SELECT o.*, p.project_name 
            FROM overtime_requests o 
            JOIN projects p ON o.project_id = p.id 
            WHERE o.member_id = %s AND o.status != 'Pending'
            ORDER BY o.created_at DESC
        """
        try:
            self.db.cursor.execute(query, (self.user['id'],))
            rows = self.db.cursor.fetchall()

            if not rows:
                ctk.CTkLabel(
                    self.history_frame, 
                    text="📭 No overtime history yet.",
                    text_color="gray",
                    font=("Arial", 14)
                ).pack(expand=True, fill="both", pady=50)
                return

            # Show history count
            count_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            count_frame.pack(fill="x", pady=(10, 5), padx=10)
            
            ctk.CTkLabel(
                count_frame,
                text=f"📊 Total records: {len(rows)}",
                font=("Arial", 12, "bold"),
                text_color="#3498DB"
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.history_frame, 
                    fg_color=("#252525", "#1E1E1E"), 
                    corner_radius=10,
                    border_width=1,
                    border_color="#3D5166"
                )
                card.pack(fill="x", pady=8, padx=10)

                status_colors = {
                    "Accepted": "#27AE60", 
                    "Rejected": "#E74C3C", 
                    "Approved": "#2980B9"
                }
                s_color = status_colors.get(r['status'], "gray")

                # Content
                content_frame = ctk.CTkFrame(card, fg_color="transparent")
                content_frame.pack(fill="x", padx=15, pady=12)
                
                # First row: Project, Date, and Status
                top_row = ctk.CTkFrame(content_frame, fg_color="transparent")
                top_row.pack(fill="x", pady=(0, 8))
                
                left_info = f"📁 {r['project_name']}  |  📅 {r['ot_date']}  |  ⏳ {r['hours']} hrs"
                ctk.CTkLabel(
                    top_row, 
                    text=left_info, 
                    font=("Arial", 12)
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row, 
                    text=r['status'], 
                    text_color=s_color, 
                    font=("Arial", 12, "bold")
                ).pack(side="right")

                # Show Leader's Original Reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=("#2B2B2B", "#2A2A2A"), corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text="📋 Leader's Reason:",
                        font=("Arial", 11, "bold"),
                        text_color="#3498DB"
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Show Member's Rejection Reason (if rejected)
                if r['status'] == 'Rejected' and r.get('rejected_reason') and r['rejected_reason'].strip():
                    reject_frame = ctk.CTkFrame(content_frame, fg_color=("#3D1E1E", "#2B1010"), corner_radius=6)
                    reject_frame.pack(fill="x", pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text="❌ Your Rejection Reason:",
                        font=("Arial", 11, "bold"),
                        text_color="#E74C3C"
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text=r['rejected_reason'],
                        font=("Arial", 11),
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

        except Exception as e:
            print(f"Error loading history: {e}")
            messagebox.showerror("Error", f"Could not load history: {e}")

    def handle_reject(self, ot_id):
        """Handle reject action with reason input"""
        reason = simpledialog.askstring(
            "Reject Overtime", 
            "Please provide reason for rejection:", 
            parent=self
        )
        
        if reason and reason.strip():
            self.update_status(ot_id, 'Rejected', reason.strip())
        elif reason == "":
            messagebox.showwarning("Warning", "Reason is required to reject.")

    def update_status(self, ot_id, new_status, member_note=None):
        """Update request status in database"""
        try:
            if member_note:
                sql = """
                UPDATE overtime_requests 
                SET status = %s, 
                    rejected_reason = %s
                WHERE id = %s
                """
                self.db.cursor.execute(sql, (new_status, member_note, ot_id))
            else:
                self.db.cursor.execute(
                    "UPDATE overtime_requests SET status = %s WHERE id = %s", 
                    (new_status, ot_id)
                )
            
            self.db.conn.commit()
            messagebox.showinfo("Success", f"OT Request {new_status}!")
            
            # Refresh current tab
            current_tab = self.segmented_btn.get()
            if current_tab == "📋 Pending Requests":
                self.refresh_pending_requests()
            else:
                self.refresh_history()
                
        except Exception as e:
            messagebox.showerror("Error", f"Could not update status: {e}")