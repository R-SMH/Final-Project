import customtkinter as ctk
from PIL import Image
import os
import json
from wallet_ui import *
from profile_window import ProfileWindow
from auction_button import create_auction_button
from bidpopup_ui import open_bid_popup


current_balance = 0

class Dashboard(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        self.current_balance = current_balance
        self.title("Dashboard")
        self.geometry("1200x600")

        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.top_bar = ctk.CTkFrame(master=self.main_frame, height=70)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="new")
        self.top_bar.grid_propagate(False)
        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=0)

        platform_title = ctk.CTkLabel(self.top_bar, text="BidMasters", font=("Arial", 25, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="nsw")

        icon_path = "assets/user_icon.png"
        self.icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(32, 32))

        account_btn = ctk.CTkButton(
            master=self.top_bar,
            image=self.icon_image,
            text="",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=self.open_profile_window_func
        )
        account_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        sidebar_container = ctk.CTkFrame(master=self.main_frame)
        sidebar_container.grid(row=1, column=0, rowspan=3, sticky="ns")

        sidebar_canvas = ctk.CTkCanvas(sidebar_container, bg='#2b2b2b', highlightthickness=0, bd=0)
        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        sidebar_canvas.configure(width=250)
        sidebar_canvas.pack(side="left", fill="y", expand=True)

        buttons = ["Expiring Auctions", "Silent Auction", "Mystery Auction"]

        ctk.CTkButton(master=scrollable_frame, text="Home", width=130, anchor="w", command=self.load_home_view).pack(pady=3, padx=(5, 5))

        auction_btn = create_auction_button(scrollable_frame, self)
        auction_btn.pack(pady=3, padx=(5, 5))

        for bt in buttons:
            ctk.CTkButton(master=scrollable_frame, text=bt, width=130, anchor="w").pack(pady=3, padx=(5, 5))

        wallet_button = ctk.CTkButton(master=scrollable_frame, text="Wallet", width=130, anchor="w", command=self.open_wallet_ui)
        wallet_button.pack(pady=3, padx=(5, 5))

        ctk.CTkButton(master=scrollable_frame, text="➕ Add Auction Item", width=130, anchor="w", command=self.open_add_item_window).pack(pady=15, padx=0)

        self.load_home_view(user_id)

    def load_home_view(self, user_id=None):
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    info = child.grid_info()
                    if int(info.get("column", -1)) == 1 and int(info.get("row", -1)) >= 1:
                        child.grid_forget()

        self.summary_label = ctk.CTkLabel(master=self.main_frame, text="Summary", font=("Arial", 18, "bold"))
        self.summary_label.grid(row=1, column=1, sticky="nw", padx=10, pady=(10, 0))

        self.summary_frame = ctk.CTkFrame(master=self.main_frame, height=100)
        self.summary_frame.grid(row=2, column=1, sticky="new", padx=10, pady=(5, 0))
        self.summary_frame.grid_propagate(False)
        self.summary_frame.configure(height=100)
        self.summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.summary_frame.grid_rowconfigure(0, weight=1)

        self.user_id = user_id
        summary_data = self.get_summary_data(self.user_id)

        self.display_data = [
            ("Balance", f"$ {summary_data[0]}"),
            ("Active Bids", f"{summary_data[1]}"),
            ("Auctions Won", f"{summary_data[2]}"),
            ("Total Spent", f"$ {summary_data[3]}")
        ]

        self.balance_summary_label = None

        for i, (label, value) in enumerate(self.display_data):
            card = ctk.CTkFrame(master=self.summary_frame, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))

            if label == "Balance":
                self.balance_summary_label = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"))
                self.balance_summary_label.pack(expand=True)
            else:
                ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(expand=True)

        self.auction_section = ctk.CTkFrame(master=self.main_frame, fg_color="transparent")
        self.auction_section.grid(row=3, column=1, sticky="nsew", padx=10, pady=(10, 20))
        self.auction_section.grid_rowconfigure(1, weight=1)
        self.auction_section.grid_columnconfigure(0, weight=4)
        self.auction_section.grid_columnconfigure(1, weight=2)

        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.auction_label = ctk.CTkLabel(master=self.auction_section, text="Your Auctions", font=("Arial", 18, "bold"))
        self.auction_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)

        self.add_auction_btn = ctk.CTkButton(master=self.auction_section, text="Add Auction", width=60, height=30, corner_radius=8, command=self.open_add_item_window)
        self.add_auction_btn.grid(row=0, column=0, sticky="e", pady=(0, 0), padx=(0, 10))

        self.scroll_container = ctk.CTkFrame(master=self.auction_section)
        self.scroll_container.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.scroll_container.grid_rowconfigure(0, weight=1)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        self.auction_canvas = ctk.CTkCanvas(self.scroll_container, bg="#2b2b2b", highlightthickness=0)
        self.auction_scrollbar = ctk.CTkScrollbar(master=self.scroll_container, orientation="vertical", command=self.auction_canvas.yview)

        self.scrollable_list = ctk.CTkFrame(master=self.auction_canvas)
        self.scroll_window = self.auction_canvas.create_window((0, 0), window=self.scrollable_list, anchor="nw")
        self.scrollable_list.bind("<Configure>", lambda e: self.auction_canvas.configure(scrollregion=self.auction_canvas.bbox("all")))

        self.auction_canvas.configure(yscrollcommand=self.auction_scrollbar.set)
        self.auction_canvas.grid(row=0, column=0, sticky="nsew")
        self.auction_scrollbar.grid(row=0, column=1, sticky="ns")
        #----------------------------------NOTIFICATION PANEL----------------------------------#
        self.notification_panel = ctk.CTkFrame(master=self.auction_section, fg_color="#3a3a3a", corner_radius=8)
        self.notification_panel.grid(row=1, column=1, sticky="nsew")
        self.notification_panel.grid_columnconfigure(0, weight=1)
        self.notification_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.notification_panel, text="Notifications", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.notification_list = ctk.CTkScrollableFrame(self.notification_panel, fg_color="#2b2b2b", corner_radius=5)
        self.notification_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        sample_notifications = [
            "✅ You won the 'Smartwatch' auction!",
            "❌ You were outbid on 'Vintage Camera'.",
            "💸 You added $500 to your wallet.",
            "🔔 Someone bid on your 'Headphones' listing!"
            ""
        ]

        for note in sample_notifications:
            ctk.CTkLabel(master=self.notification_list, text=note, anchor="w", justify="left", wraplength=400).pack(anchor="w", pady=3)

        self.render_auction_cards()


        
    def open_add_item_window(self):
            from add_auction import Add_Auction_Window
            Add_Auction_Window(self, on_submit=self.render_auction_cards)
            
    def open_wallet_ui(self):
            Wallet = WalletWindow(self, current_balance=self.current_balance, on_balance_update=self.update_balance)
            Wallet.grab_set()
            
    def get_summary_data(self, username):
        return [self.current_balance, 5, 3, 1500]  # Use instance variable!

    def update_balance(self, new_balance):
        previous_balance = self.current_balance
        self.current_balance = new_balance

        if self.balance_summary_label:
            self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")

        # Now compare AFTER updating the label
        if new_balance > previous_balance:
            self.add_notification(f"💰 You added ${new_balance - previous_balance:.2f} to your wallet.")
        elif new_balance < previous_balance:
            self.add_notification(f"📉 You spent ${previous_balance - new_balance:.2f}.")


    def load_auctions(self):
        with open("sample_data.json", "r") as f:
            return json.load(f)
        


    def open_profile_window_func(self):

        user_data = {
            "username": "Shuvo",
            "user_id": "123456",
            "first_name": "Shreyastha",
            "last_name": "Banik",
            "dob": "2006-03-10",
            "balance": self.current_balance
        }
        try:
            with open("profile_data.json", "r") as f:
                saved_data = json.load(f)
            user_data.update(saved_data)
        except FileNotFoundError:
            pass

        def handle_profile_save(updated_data):
            self.current_balance = updated_data["balance"]
            if hasattr(self, "balance_summary_label"):
                self.balance_summary_label.configure(text=f"$ {self.current_balance:.2f}")
            print("Profile updated:", updated_data)

        ProfileWindow(self, user_data, on_save=handle_profile_save).grab_set()

    '''def open_profile_window_func(self):
        user_data = {
            "username": "shreyastha18",
            "user_id": "U123456",
            "first_name": "Shreyastha",
            "last_name": "Banik",
            "dob": "2005-03-10",
            "balance": self.current_balance
        }

        def handle_profile_save(updated_data):
            self.current_balance = updated_data["balance"]
            if hasattr(self, "balance_summary_label"):
                self.balance_summary_label.configure(text=f"$ {self.current_balance:.2f}")
            print("Profile updated:", updated_data)

        ProfileWindow(self, user_data, on_save=handle_profile_save).grab_set()
'''
    def add_notification(self, message):
        if hasattr(self, 'notification_list'):
            # Create a container frame for the message + delete button
            notif_frame = ctk.CTkFrame(self.notification_list, fg_color="transparent")
            notif_frame.pack(fill="x", pady=2, padx=5)

            # Message label
            notif_label = ctk.CTkLabel(
                master=notif_frame,
                text=message,
                anchor="w",
                justify="left",
                wraplength=350,
                font=("Arial", 13)
            )
            notif_label.pack(side="left", fill="x", expand=True, padx=(0, 5))

            # Delete button
            delete_btn = ctk.CTkButton(
                master=notif_frame,
                text="❌",
                width=28,
                height=28,
                font=("Arial", 12),
                fg_color="#4a4a4a",
                hover_color="#d13b3b",
                command=notif_frame.destroy
            )
            delete_btn.pack(side="right", padx=2)


    def render_auction_cards(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        sample_auctions = self.load_auctions()

        columns = 3
        for index, auction in enumerate(sample_auctions):
            row = index // columns
            col = index % columns

            card = ctk.CTkFrame(master=self.scrollable_list, width=250, height=280, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False)

            if "image" in auction and os.path.exists(auction["image"]):
                auction_image = ctk.CTkImage(Image.open(auction["image"]), size=(230, 120))
                image_label = ctk.CTkLabel(card, image=auction_image, text="")
                image_label.image = auction_image
            else:
                image_label = ctk.CTkLabel(card, text="[Image Here]", width=230, height=120, fg_color="#444")

            image_label.pack(pady=(10, 5), padx=10)

            ctk.CTkLabel(card, text=auction["Name"], font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Current: {auction['price']}", font=("Arial", 14)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda a=auction: open_bid_popup(self, a, on_submit=lambda bid: self.add_notification(f"✅ You bid ${bid:.2f} on '{a['Name']}'"))).pack(pady=(5, 10))   #bid now button


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
