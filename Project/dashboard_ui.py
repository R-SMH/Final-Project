import customtkinter as ctk
from PIL import Image
import os
import json
from wallet_ui import *  # Assuming wallet_ui.py contains the WalletWindow class
from profile_window import ProfileWindow


current_balance = 1000  # Placeholder for current balance, replace with actual value

class Dashboard(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        self.current_balance = current_balance 
        self.title("Dashboard")
        self.geometry("1200x600")
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=0)   # Sidebar
        self.main_frame.grid_columnconfigure(1, weight=1)   # Main content
        self.main_frame.grid_rowconfigure(0, weight=0)  # Top bar
        self.main_frame.grid_rowconfigure(1, weight=0)  # Summary label
        self.main_frame.grid_rowconfigure(2, weight=0)  # Summary cards
        self.main_frame.grid_rowconfigure(3, weight=1)  # Auction section
        
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
            command=self.open_profile_window_func  # Corrected function call
        )
        account_btn.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        # 
        sidebar_container = ctk.CTkFrame(master=self.main_frame)
        sidebar_container.grid(row=1, column=0, rowspan=3, sticky="ns")

        # 
        sidebar_canvas = ctk.CTkCanvas(sidebar_container, bg='#2b2b2b', highlightthickness=0, bd=0)
        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # 
        sidebar_canvas.configure(width=250)
        sidebar_canvas.pack(side="left", fill="y", expand=True)


        buttons = [
            "Expiring Auctions", "Silent Auction", "Mystery Auction",
        ]
        
        ctk.CTkButton(
                master=scrollable_frame,
                text="Home",
                width=130,
                anchor="w",
                command = self.load_home_view
            ).pack(pady=3, padx=(5, 5))


        auction_btn = ctk.CTkButton(
                master=scrollable_frame,
                text="Auction",
                width=130,
                anchor="w",
                command=self.load_auction_view  # Corrected function call
            )
            
        auction_btn.pack(pady=3, padx=(5, 5))
        
        
        for bt in buttons:
            ctk.CTkButton(
                master=scrollable_frame,
                text=bt,
                width=130,
                anchor="w"
            ).pack(pady=3, padx=(5, 5))


        wallet_button = ctk.CTkButton(
            master=scrollable_frame,
            text="Wallet",
            width=130,
            anchor="w",
            command=self.open_wallet_ui
        )
        wallet_button.pack(pady=3, padx=(5, 5))

        ctk.CTkButton(
            master=scrollable_frame,
            text="➕ Add Auction Item",
            width=130,
            anchor="w",
            command=self.open_add_item_window
        ).pack(pady=15, padx=0)

        self.load_home_view(user_id)
        
    def load_home_view(self, user_id = None):

        # Clear previous content first (if needed)
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

        """
        def Caden_func(username):
            usm = username
            return list((current_balance, 5, 3, 1500))
            """
        
        # Call the function to get summary data
        # summary_data = Caden_func(user_id)
        self.user_id = user_id
        summary_data = self.get_summary_data(self.user_id)

        self.display_data = [
            ["Balance", f"$ {summary_data[0]}"],
            ["Active Bids", f"{summary_data[1]}"],
            ["Auctions Won", f"{summary_data[2]}"],
            ["Total Spent", f"$ {summary_data[3]}"]
        ]

        self.balance_summary_label = None  # Add this to store the reference

        for i, (label, value) in enumerate(self.display_data):
            card = ctk.CTkFrame(master=self.summary_frame, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))
            
            if label == "Balance":
                self.balance_summary_label = ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"))
                self.balance_summary_label.pack(expand=True)
            else:
                ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(expand=True)

        self.auction_section = ctk.CTkFrame(master=self.main_frame, fg_color="transparent", width=828 )
        self.auction_section.grid(row=3, column=1, sticky="nsw", padx=5, pady=(10, 20))
        self.auction_section.grid_rowconfigure(1, weight=1)
        self.auction_section.grid_columnconfigure(0, weight=1)
        self.auction_section.grid_columnconfigure(1, weight=0)
        self.auction_section.grid_propagate(False) 
        self.main_frame.grid_rowconfigure(3, weight=1)  # Let row 3 expand
        self.main_frame.grid_columnconfigure(1, weight=1)  # Let column 1 expand

        """
        self.content_wrapper = ctk.CTkFrame(master=self.auction_section, fg_color="red", width=800)
        self.content_wrapper.grid(row=1, column=0, sticky="n", pady=(0, 10))
        self.content_wrapper.grid_propagate(1)
        """
        self.auction_label = ctk.CTkLabel(master=self.auction_section, text="My Auctions", font=("Arial", 18, "bold"))
        self.auction_label.grid(row=0, column=0, sticky="w", pady=(0, 5), padx=5)

        # Add Auction Button
        self.add_auction_btn = ctk.CTkButton(
            master=self.auction_section,
            text="Add Auction",
            width=60,
            height=30,
            corner_radius=8,
            command=self.open_add_item_window  # Replace with your actual function
        )
        self.add_auction_btn.grid(row=0, column=0, sticky="e", pady=(0, 0), padx=(0, 10))

        self.scroll_container = ctk.CTkFrame(master=self.auction_section, fg_color="transparent")
        self.scroll_container.grid(row=1, column=0, sticky="nsew")
        self.scroll_container.grid_rowconfigure(0, weight=1)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        self.auction_canvas = ctk.CTkCanvas(self.scroll_container, bg="#2b2b2b", highlightthickness=0)
        self.auction_scrollbar = ctk.CTkScrollbar(master=self.scroll_container, orientation="vertical", command=self.auction_canvas.yview)

        self.scrollable_list = ctk.CTkFrame(master=self.auction_canvas)
        self.scroll_window = self.auction_canvas.create_window((0, 0), window=self.scrollable_list, anchor="nw")
        self.scrollable_list.bind(
            "<Configure>", lambda e: self.auction_canvas.configure(scrollregion=self.auction_canvas.bbox("all"))
        )
        self.auction_canvas.configure(yscrollcommand=self.auction_scrollbar.set)
        self.auction_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.auction_scrollbar.grid(row=0, column=1, sticky="ns")

        # Uncomment this function if you want to use it for loading auctions
        # def Caden_will_use_this_for_my_auctions(self, user_id):
        #     with open("sample_data.json", "r") as f:
        #         return json.load(f)

        self.render_auction_cards()

#=========================================================================================================================
    def load_auction_view(self):
        # Step 1: Clear previous content on right side
        
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    info = child.grid_info()
                    if int(info.get("column", -1)) == 1 and int(info.get("row", -1)) >= 1:
                        child.grid_forget()
        

        # Step 2: Auction view container
        self.auction_view = ctk.CTkFrame(master = self.main_frame, fg_color="#2b2b2b", width=800)
        self.auction_view.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.auction_view.grid_columnconfigure(0, weight=1) 
        self.auction_view.grid_rowconfigure(0, weight=0)
        self.auction_view.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.auction_view, height=28, fg_color = "transparent", width=800)
        search_frame.grid(row=0, column=0, columnspan=1, sticky="ne", pady=(2, 5))
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0)  # Button column
        search_frame.grid_propagate(True)  # Prevent resizing
        search_frame.configure(height=30)

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search auctions...", height=28, width=250, border_width=1, corner_radius=0)
        # search_entry.pack(side="left", padx=10)
        search_entry.grid(row=0, column=0, sticky="new", padx=(5, 0), pady=(5, 0))
        search_entry.grid_propagate(True)  # 

        search_button = ctk.CTkButton(search_frame, text="Search", height=28, width=60, corner_radius=0, command=lambda:  self.perform_search(search_entry.get(),))
        search_button.grid(row=0, column=0, sticky="ne" ,padx=(5, 0), pady=(5, 0))
        search_button.grid_propagate(True)  # Prevent resizing
        # search_button.pack(side="left", padx=5)


        # Step 3: Scrollable canvas
        self.canvas = ctk.CTkCanvas(self.auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.auction_view, orientation="vertical", command=self.canvas.yview,)
        scroll_frame = ctk.CTkFrame(master=self.auction_view) # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew") 
        scrollbar.grid(row=1, column=1, sticky="ns")


        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))
        # self.canvas.itemconfig(self.auction_view, width=800)
        # self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * int(e.delta / 120), "units"))


        # Step 4: Load auction data

        my_auctions = self.load_auctions()
        all_auctions = self.load_all_auctions()

        ctk.CTkLabel(scroll_frame, text="My Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        self.render_cards(my_auctions, self.my_auction_grid, columns=5)


        # Separator
        ctk.CTkFrame(scroll_frame, height=2, fg_color="#666").pack(fill="x", pady=10)


        ctk.CTkLabel(scroll_frame, text="All Auctions", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        my_auction_grid.pack(anchor="nw")
        self.render_cards(all_auctions, my_auction_grid, columns=5)

        # all_auctions = self.load_all_auctions()


#=========================================================================================================================
        
    def open_add_item_window(self):
            from add_auction import Add_Auction_Window
            Add_Auction_Window(self, on_submit=self.render_auction_cards)
            
    def open_wallet_ui(self):
            Wallet = WalletWindow(self, current_balance=self.current_balance, on_balance_update=self.update_balance)
            Wallet.grab_set()
            
    def get_summary_data(self, username):
        return [self.current_balance, 5, 3, 1500]  # Use instance variable!

    def update_balance(self, new_balance):
        self.current_balance = new_balance
        self.balance_summary_label.configure(text=f"$ {new_balance:.2f}")
        self.display_data[0][1] = f"$ {new_balance:.2f}"

    def load_auctions(self):
        with open("sample_data.json", "r") as f:
            return json.load(f)

    def load_all_auctions(self):
        with open("all_auctions.json", "r") as f:
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

# ------------------------------------------------------------------------
    def render_cards(self, auctions, parent_frame, columns=4):
        
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        for i, auction in enumerate(auctions):
            row = i // columns
            col = i % columns

            card = ctk.CTkFrame(master=parent_frame, width=250, height=280, corner_radius=10, fg_color="#3b3b39")
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False) #
            try:
                if "image" in auction and os.path.exists(auction["image"]):
                    img = ctk.CTkImage(Image.open(auction["image"]), size=(200, 100))
                    image_label = ctk.CTkLabel(card, image=img, text="")
                    image_label.image = img
                    image_label.pack(pady=(10, 5))
            except:
                ctk.CTkLabel(card, text="[Image Here]", width=200, height=100, fg_color="#444").pack(pady=(10, 5))

            ctk.CTkLabel(card, text=auction["Name"], font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Price: {auction['price']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 10)).pack(anchor="w", padx=10)
            ctk.CTkButton(card, text="Bid Now", command=lambda: "bid now clicked").pack(pady=(5, 10))
# ------------------------------------------------------------------------
    def perform_search(self, query):
        all_auctions = self.load_all_auctions()
        searched_with = query
        query = query.lower()

        if query == "":
            self.load_auction_view()
            return

        filtered_auctions = [
            auction for auction in all_auctions
            if query in auction["Name"].lower()
        ]

        self.canvas = ctk.CTkCanvas(self.auction_view, highlightthickness=0, bg="#2b2b2b")
        scrollbar = ctk.CTkScrollbar(master=self.auction_view, orientation="vertical", command=self.canvas.yview,)
        scroll_frame = ctk.CTkFrame(master=self.auction_view) # This frame will hold the scrollable content
        scroll_window = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw") # This creates a window in the canvas

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=1, column=0, sticky="nsew") 
        scrollbar.grid(row=1, column=1, sticky="ns")

        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(scroll_window, width=e.width))

        ctk.CTkLabel(scroll_frame, text=f"Searching for {searched_with}", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="w")
        self.my_auction_grid = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.my_auction_grid.pack(anchor="nw")
        if filtered_auctions == []:
            ctk.CTkLabel(scroll_frame, text="No results found", font=("Arial", 16, "bold")).pack(pady=(10, 5), anchor="center")
        else:
            self.render_cards(filtered_auctions, self.my_auction_grid, columns=5) 
        """
        for widget in self.canvas.winfo_children():
            widget.destroy()

        self.render_cards(filtered_auctions, self.my_auction_grid) if query != "" else self.load_self.auction_view()
        """
if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
