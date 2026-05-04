import customtkinter as ctk
from database import Database
from tkinter import messagebox, simpledialog
from datetime import datetime

class MemberOvertime(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.db = Database()
        self.user = user  # Login ဝင်ထားသော Member data
        
        # Automatic Theme Constants (Tuples) - matching member_report.py
        self.COLOR_CARD_BG = ("#FFFFFF", "#1E1E1E")
        self.COLOR_BORDER = ("#DBDBDB", "#2C2C2C")
        self.COLOR_TEXT_MAIN = ("#1A1A2A", "#E8EDF2")
        self.COLOR_TEXT_SEC = ("#555555", "#AAB7C4")
        self.COLOR_TEXT_TER = ("#777777", "#718096")
        self.COLOR_SCROLL_BG = ("#F5F5F5", "#1A1A1A")
        self.COLOR_CONTAINER_BG = ("#F0F0F0", "#252525")

        # Configure grid
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Segmented button
        self.grid_rowconfigure(2, weight=1)  # Content frame
        self.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=80, pady=20)
        
        ctk.CTkLabel(
            header, 
            text="Overtime Management", 
            font=("Arial", 20, "bold"),
            text_color=self.COLOR_TEXT_MAIN
        ).pack(side="left")

        # --- Segmented Button for Tab Selection ---
        self.segmented_btn = ctk.CTkSegmentedButton(
            self,
            values=["📋 Pending Requests", "📜 History"],
            command=self.on_tab_change,
            font=("Arial", 13, "bold"),
            fg_color=self.COLOR_CONTAINER_BG,
            selected_color=("#3498DB", "#1F538D"),
            unselected_color=self.COLOR_CARD_BG,
            text_color=self.COLOR_TEXT_MAIN,
            corner_radius=12,
            height=40
        )
        self.segmented_btn.grid(row=1, column=0, sticky="ew", padx=80, pady=10)
        self.segmented_btn.set("📋 Pending Requests")  # Set default tab

        # --- Content Frame (changes based on selected tab) ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=80, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Create scrollable frames for both tabs
        self.pending_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
        )
        
        self.history_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=self.COLOR_SCROLL_BG,
            corner_radius=12,
            border_width=1,
            border_color=self.COLOR_BORDER
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
                    text_color=self.COLOR_TEXT_SEC,
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
                text_color=self.COLOR_TEXT_MAIN
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.pending_frame,
                    fg_color=self.COLOR_CARD_BG,
                    corner_radius=10,
                    border_width=1,
                    border_color=self.COLOR_BORDER
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
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row,
                    text=f"📅 {r['ot_date']}",
                    font=("Arial", 11),
                    text_color=self.COLOR_TEXT_SEC
                ).pack(side="right")

                # Hours and Details
                details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                details_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    details_frame,
                    text=f"⏳ Duration: {r['hours']} hours",
                    font=("Arial", 12),
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(anchor="w")

                # Leader's reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=self.COLOR_CONTAINER_BG, corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text="💬 Leader's Request:",
                        font=("Arial", 11, "bold"),
                        text_color=("#F39C12", "#F39C12")
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Buttons
                btn_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                btn_frame.pack(fill="x", pady=(12, 0))

                def _btn(text, color, hover, cmd, width=60, height=30, corner_radius=14):
                    return ctk.CTkButton(
                        btn_frame,
                        text=text,
                        width=width,
                        height=height,
                        corner_radius=corner_radius,
                        fg_color=color,
                        hover_color=hover,
                        font=("Arial", 12, "bold"),
                        text_color="white",
                        command=cmd
                    )

                _btn("✓ Accept", "#27AE60", "#1E8449", 
                    lambda id=r['id']: self.update_status(id, 'Accepted')
                ).pack(side="left", padx=(0, 10))

                _btn("✗ Reject", "#E74C3C", "#C0392B", 
                    lambda id=r['id']: self.handle_reject(id)
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
                    text_color=self.COLOR_TEXT_SEC,
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
                text_color=self.COLOR_TEXT_MAIN
            ).pack(anchor="w")

            for r in rows:
                card = ctk.CTkFrame(
                    self.history_frame, 
                    fg_color=self.COLOR_CARD_BG, 
                    corner_radius=10,
                    border_width=1,
                    border_color=self.COLOR_BORDER
                )
                card.pack(fill="x", pady=8, padx=10)

                status_colors = {
                    "Accepted": self.COLOR_TEXT_MAIN, 
                    "Rejected": ("#E74C3C", "#E74C3C"), 
                    "Approved": ("#2980B9", "#2980B9")
                }
                s_color = status_colors.get(r['status'], self.COLOR_TEXT_SEC)

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
                    font=("Arial", 12),
                    text_color=self.COLOR_TEXT_MAIN
                ).pack(side="left")
                
                ctk.CTkLabel(
                    top_row, 
                    text=r['status'], 
                    text_color=s_color, 
                    font=("Arial", 12, "bold")
                ).pack(side="right")

                # Show Leader's Original Reason
                if r['reason'] and r['reason'].strip():
                    reason_frame = ctk.CTkFrame(content_frame, fg_color=self.COLOR_CONTAINER_BG, corner_radius=6)
                    reason_frame.pack(fill="x", pady=(8, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text="📋 Leader's Reason:",
                        font=("Arial", 11, "bold"),
                        text_color=self.COLOR_TEXT_MAIN
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reason_frame,
                        text=r['reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

                # Show Member's Rejection Reason (if rejected)
                if r['status'] == 'Rejected' and r.get('rejected_reason') and r['rejected_reason'].strip():
                    reject_frame = ctk.CTkFrame(content_frame, fg_color=("#F8E6E6", "#3D1E1E"), corner_radius=6)
                    reject_frame.pack(fill="x", pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text="❌ Your Rejection Reason:",
                        font=("Arial", 11, "bold"),
                        text_color=("#E74C3C", "#E74C3C")
                    ).pack(anchor="w", padx=10, pady=(5, 0))
                    
                    ctk.CTkLabel(
                        reject_frame,
                        text=r['rejected_reason'],
                        font=("Arial", 11),
                        text_color=self.COLOR_TEXT_SEC,
                        wraplength=550,
                        justify="left"
                    ).pack(anchor="w", padx=10, pady=(0, 5))

        except Exception as e:
            print(f"Error loading history: {e}")
            messagebox.showerror("Error", f"Could not load history: {e}")

    def handle_reject(self, ot_id):
        """Handle reject action with reason input (styled popup)"""
        popup = ctk.CTkToplevel(self)
        popup.title("Reject Overtime")
        popup.geometry("400x250")
        popup.grab_set()

        ctk.CTkLabel(
            popup, 
            text="Please provide reason for rejection:", 
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 10))

        reason_box = ctk.CTkTextbox(popup, height=100)
        reason_box.pack(fill="x", padx=20)

        def confirm():
            reason = reason_box.get("0.0", "end").strip()
            if reason:
                self.update_status(ot_id, 'Rejected', reason)
                popup.destroy()
            else:
                messagebox.showwarning("Warning", "Reason is required to reject.")

        def cancel():
            popup.destroy()

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=15)

        ctk.CTkButton(
            btn_frame, 
            text="✓ Confirm", 
            width=60, 
            height=30,
            corner_radius=14,
            fg_color="#E74C3C", 
            hover_color="#C0392B", 
            text_color="white", 
            command=confirm
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, 
            text="✗ Cancel", 
            width=60, 
            height=30,
            corner_radius=14,
            fg_color="#95A5A6", 
            hover_color="#7F8C8D", 
            text_color="white", 
            command=cancel
        ).pack(side="left", padx=10)


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
