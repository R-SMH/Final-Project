import customtkinter as ctk
from PIL import Image
import os
import json
from wallet_ui import * # Assuming wallet_ui.py contains the WalletWindow class

current_balance = 1000  # Placeholder for current balance, replace with actual value

class Dashboard(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        self.current_balance = current_balance 
        self.title("Dashboard")
        self.geometry("1200x600")
        main_frame = ctk.CTkFrame(master=self)
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=0)   # Sidebar
        main_frame.grid_columnconfigure(1, weight=1)   # Main content
        main_frame.grid_rowconfigure(0, weight=0)  # Top bar
        main_frame.grid_rowconfigure(1, weight=0)  # Summary label
        main_frame.grid_rowconfigure(2, weight=0)  # Summary cards
        main_frame.grid_rowconfigure(3, weight=1)  # Auction section
        top_bar = ctk.CTkFrame(master=main_frame, height=70)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="new",)
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)
        platform_title = ctk.CTkLabel(top_bar, text="BidMasters", font=("Arial", 25, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=(10,5), sticky="nsw")
        icon_path = "assets/user_icon.png"
        icon_image = ctk.CTkImage(light_image=Image.open(icon_path), size=(32, 32))

        account_btn = ctk.CTkButton(
            master=top_bar,
            image=icon_image,
            text="",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="transparent",
            hover_color="#3a3a3a",
            command=lambda: print("Account Manager Clicked")
        )
        account_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        sidebar_container = ctk.CTkFrame(master=main_frame)
        sidebar_container.grid(row=1, column=0, rowspan=3, sticky="ns")

        sidebar_canvas = ctk.CTkCanvas(
            sidebar_container, bg='#2b2b2b', highlightthickness=0, bd=0
        )

        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")


        sidebar_canvas.configure(width=250)
        # current_balance = 1000  # or from DB via self.Caden_func()

        sidebar_canvas.pack(side="left", fill="y", expand=True)

        def open_add_item_window():
            from add_auction import Add_Auction_Window
            Add_Auction_Window(self, on_submit=self.render_auction_cards)
            
        buttons = [
            "Home","Auction", "Expiring Auctions", "Silent Auction", "Mystery Auction",
        ]
        for bt in buttons:
            ctk.CTkButton(
                master=scrollable_frame,
                text=bt,
                width=130,
                anchor="w"
            ).pack(pady=3, padx=(5,5))

        def open_wallet_ui():

            Wallet = WalletWindow(self, current_balance=self.current_balance, on_balance_update=self.update_balance)
            Wallet.grab_set()

            # Hook the "Wallet" button manually
        wallet_button = ctk.CTkButton(
             master=scrollable_frame,
            text="Wallet",
            width=130,
            anchor="w",
            command=open_wallet_ui
                                        )
        wallet_button.pack(pady=3, padx=(5,5))

   

            
        ctk.CTkButton(
            master=scrollable_frame,
            text="➕ Add Auction Item",
            width=130,
            anchor="w",
            command=open_add_item_window
        ).pack(pady=15, padx=0)
    
        
        summary_label = ctk.CTkLabel(master=main_frame, text="Summary", font=("Arial", 18, "bold"))
        summary_label.grid(row=1, column=1, sticky="nw", padx=10, pady=(10, 0))

        summary_frame = ctk.CTkFrame(master=main_frame, height=100,)
        summary_frame.grid(row=2, column=1, sticky="new",padx = 10, pady=(5, 0))
        summary_frame.grid_propagate(False)
        summary_frame.configure(height=100)
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        summary_frame.grid_rowconfigure(0, weight=1)
        

        def Caden_func(username):
            usm = username
            return list((current_balance, 5, 3, 1500))
        
        # Call the function to get summary data
        summary_data = Caden_func(user_id)
        summary_data = self.get_summary_data(user_id)

        display_data = [
            ("Balance", f"$ {summary_data[0]}"),
            ("Active Bids", f"{summary_data[1]}"),
            ("Auctions Won", f"{summary_data[2]}"),
            ("Total Spent", f"$ {summary_data[3]}")
        ]

        # Create each card
        self.balance_summary_label = None  # Add this to store the reference


        for i, (label, value) in enumerate(display_data):
            card = ctk.CTkFrame(master=summary_frame, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))
            #ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(expand = True)

            if label == "Balance":
                self.balance_summary_label = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"))
                self.balance_summary_label.pack(expand=True)

        #    if label == "Balance":
        #        self.balance_summary_label = ctk.CTkLabel  # Store the reference

        auction_section = ctk.CTkFrame(master=main_frame, fg_color="transparent")
        auction_section.grid(row=3, column=1, sticky="nsw", padx=5, pady=(10, 20))
        auction_section.grid_rowconfigure(1, weight=1)
        auction_section.grid_columnconfigure(0, weight=1)
        auction_section.grid_columnconfigure(1, weight=0)

        main_frame.grid_rowconfigure(3, weight=1)     # Let row 3 expand
        main_frame.grid_columnconfigure(1, weight=1)  # Let column 1 expand

        # Wrapper to control width
        content_wrapper = ctk.CTkFrame(master=auction_section, fg_color="transparent", width=800)
        content_wrapper.grid(row=1, column=0, sticky="n", pady=(0, 10))
        content_wrapper.grid_propagate(1)

        # Section label
        auction_label = ctk.CTkLabel(master=auction_section, text="Your Auctions", font=("Arial", 18, "bold"))
        auction_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)

        # Add Auction Button
        add_auction_btn = ctk.CTkButton(
            master=auction_section,
            text="Add Auction",
            width=60,
            height=30,
            corner_radius=8,
            command=open_add_item_window  # Replace with your actual function
        )
        add_auction_btn.grid(row=0, column=0, sticky="e", pady=(0, 0), padx=(0, 10))


        scroll_container = ctk.CTkFrame(master=auction_section)
        scroll_container.grid(row=1, column=0, sticky="nsew")
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)

        auction_canvas = ctk.CTkCanvas(scroll_container, bg="#2b2b2b", highlightthickness=0)
        auction_scrollbar = ctk.CTkScrollbar(master=scroll_container, orientation="vertical", command=auction_canvas.yview)


        self.scrollable_list = ctk.CTkFrame(master=auction_canvas)
        scroll_window = auction_canvas.create_window((0, 0), window=self.scrollable_list, anchor="nw")

        self.scrollable_list.bind(
            "<Configure>", lambda e: auction_canvas.configure(scrollregion=auction_canvas.bbox("all"))
        )
        auction_canvas.configure(yscrollcommand=auction_scrollbar.set)
        auction_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        auction_scrollbar.grid(row=0, column=1, sticky="ns")
        
        #def Caden_will_use_this_for_my_auctions(self, user_id):
            #with open("sample_data.json", "r") as f:
                #return json.load(f)
        
        self.render_auction_cards()
    def get_summary_data(self, username):
        return [self.current_balance, 5, 3, 1500]  # Use instance variable!

    #def update_balance(self, new_balance):
    #    self.current_balance = new_balance
    #    if hasattr(self, "balance_summary_label"):
    #        self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")

    #               # If you want to reflect it on the summary cards, ensure they're accessible
    #    for widget in self.winfo_children():
    #        if isinstance(widget, ctk.CTkFrame):
    #            for label in widget.winfo_children():
    #                if isinstance(label, ctk.CTkLabel) and "Balance" in label.cget("text"):
    #                    label.configure(text=f"$ {new_balance:.2f}")

    def update_balance(self, new_balance):
        self.current_balance = new_balance
        if self.balance_summary_label:
            self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")
       
    def load_auctions(self):
        
        with open("sample_data.json", "r") as f:
            return json.load(f)

        
    
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
            ctk.CTkButton(card, text="Bid Now", command=lambda: "bid now clicked").pack(pady=(5, 10))


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()