import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import os


class Dashboard(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1200x600")
        
        # === Main Layout Frame ===
        main_frame = ctk.CTkFrame(master=self)
        main_frame.pack(fill="both", expand=True)

        main_frame.grid_columnconfigure(0, weight=0)   # Sidebar
        main_frame.grid_columnconfigure(1, weight=1)   # Main content
        main_frame.grid_rowconfigure(0, weight=0)  # Top bar
        main_frame.grid_rowconfigure(1, weight=0)  # Summary label
        main_frame.grid_rowconfigure(2, weight=0)  # Summary cards
        main_frame.grid_rowconfigure(3, weight=1)  # Main content below
        # main_frame.grid_rowconfigure(4, weight=0) 


        # === Top Bar ===
        top_bar = ctk.CTkFrame(master=main_frame, height=70)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="new",)
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        platform_title = ctk.CTkLabel(top_bar, text="BidMasters", font=("Arial", 25, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=(10,5), sticky="nsw")
        
        # Load account icon
        icon_path = "assets/user_icon.png"
        icon_image = ctk.CTkImage(Image.open(icon_path), size=(32, 32))
        

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

        # === Sidebar under Top Bar (row=1) ===
        sidebar_container = ctk.CTkFrame(master=main_frame)
        sidebar_container.grid(row=1, column=0, rowspan=3, sticky="ns")

        sidebar_canvas = ctk.CTkCanvas(
            sidebar_container, bg='#2b2b2b', highlightthickness=0, bd=0
        )
        # scrollbar = ctk.CTkScrollbar(master=sidebar_container, orientation="vertical", command=sidebar_canvas.yview)

        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_scroll_region(event):
            sidebar_canvas.itemconfig(scroll_window, width=event.width)

        # scrollable_frame.bind(
        #     "<Configure>", lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        # )
        sidebar_canvas.bind("<Configure>", resize_scroll_region)

        sidebar_canvas.configure(width=300)

        sidebar_canvas.pack(side="left", fill="y", expand=True)
        # scrollbar.pack(side="right", fill="y")


        # === Sidebar Buttons ===
        buttons = [
            "Auction", "Expiring Auctions", "Silent Auction", "Mystery Auction", "Wallet",
        ]
        for bt in buttons:
            ctk.CTkButton(
                master=scrollable_frame,
                text=bt,
                width=130,
                anchor="w"
            ).pack(pady=5, padx=0)

        ctk.CTkButton(
            master=scrollable_frame,
            text="➕ Add Auction Item",
            width=130,
            anchor="w",
            command=self.open_add_item_window
        ).pack(pady=10, padx=0)
        
        # === Main Content Area ===
        # content_area = ctk.CTkFrame(master=main_frame, fg_color="#1a1a1a")
        # content_area.grid(row=1, column=1, sticky="nsew")
        # ctk.CTkLabel(content_area, text="Dashboard Content Here", font=("Arial", 16)).pack(pady=30)
        
        # === Top Summary Card Section ===
        # ctk.CTkLabel(master=main_frame, text="Summary", font=("Arial", 20)).pack(pady=(10, 5))
        # ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))
        
        summary_label = ctk.CTkLabel(master=main_frame, text="Summary", font=("Arial", 18, "bold"))
        summary_label.grid(row=1, column=1, sticky="nw", padx=10, pady=(10, 0))

        summary_frame = ctk.CTkFrame(master=main_frame, height=100,)
        summary_frame.grid(row=2, column=1, sticky="new",padx = 10, pady=(5, 0))
        summary_frame.grid_propagate(False)
        summary_frame.configure(height=100)
        summary_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        summary_frame.grid_rowconfigure(0, weight=1)
        

        # Sample data (placeholders)
        # Caden will import a function from a file, which will pass the user_id into his function and return a list of tuples
        def Caden_func(username):
            usm = username
            # Placeholder function to simulate data retrieval
            # In a real application, this would query a database or API
            return list((1000, 5, 3, 1500))
        
        # Call the function to get summary data
        summary_data = Caden_func(user_id)
        display_data = [
            ("Balance", f"$ {summary_data[0]}"),
            ("Active Bids", f"{summary_data[1]}"),
            ("Auctions Won", f"{summary_data[2]}"),
            ("Total Spent", f"$ {summary_data[3]}")
        ]

        # Create each card
        for i, (label, value) in enumerate(display_data):
            card = ctk.CTkFrame(master=summary_frame, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=label, font=("Arial", 14)).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold")).pack(expand = True)

        # === Auction Section (Row 3, Right Side) ===
        # Parent frame for both the label and the scrollable auction frame
        auction_section = ctk.CTkFrame(master=main_frame, fg_color="transparent")
        auction_section.grid(row=3, column=1, sticky="nsw", padx=5, pady=(10, 20))
        auction_section.grid_rowconfigure(1, weight=1)
        auction_section.grid_columnconfigure(0, weight=1)
        auction_section.grid_columnconfigure(1, weight=0)

        main_frame.grid_rowconfigure(3, weight=1)     # Let row 3 expand
        main_frame.grid_columnconfigure(1, weight=1)  # Let column 1 expand

        # Wrapper to control width
        content_wrapper = ctk.CTkFrame(master=auction_section, fg_color="transparent")
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
            command=self.open_add_item_window  # Replace with your actual function
        )
        add_auction_btn.grid(row=0, column=0, sticky="e", pady=(0, 0), padx=(0, 10))


        # === Scrollable Container ===
        scroll_container = ctk.CTkFrame(master=auction_section)
        scroll_container.grid(row=1, column=0, sticky="nsw")
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)

        # Scrollable canvas inside container
        auction_canvas = ctk.CTkCanvas(scroll_container, bg="#2b2b2b", highlightthickness=0)
        auction_scrollbar = ctk.CTkScrollbar(master=scroll_container, orientation="vertical", command=auction_canvas.yview)


        scrollable_list = ctk.CTkFrame(master=auction_canvas)
        scroll_window = auction_canvas.create_window((0, 0), window=scrollable_list, anchor="nw")

        scrollable_list.bind(
            "<Configure>", lambda e: auction_canvas.configure(scrollregion=auction_canvas.bbox("all"))
        )
        auction_canvas.configure(yscrollcommand=auction_scrollbar.set)
        auction_canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        auction_scrollbar.grid(row=0, column=1, sticky="ns")

        

        self.sample_auctions = [
            { "Name":"Watch", "price": "$150", "time_left": "2h 13m", "status": "Active", "image": "assets/watch.jpg"},
            {"Name":"Car","price": "$320", "time_left": "Ended", "status": "Won", "image": "assets/car.jpg"},
            {"Name":"Iphone 16","price": "$210", "time_left": "5h 47m", "status": "Active", "image": "assets/phone.jpg"},
        ]

        '''
        self.render_auction_cards()
        # self.add_auction_card("Watch", "$150", "assets/watch.jpg")
        # self.add_auction_card("Car", "$320", "assets/car.jpg")
        # self.add_auction_card("Iphone 16", "$210", "assets/iphone.jpg")
        def render_auction_cards(self):
            # First, clear existing cards if needed
            for widget in self.scrollable_list.winfo_children():
                widget.destroy()

            columns = 1
            for index, auction in enumerate(self.sample_auctions):
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

                ctk.CTkLabel(card, text=f"{auction['Name']}", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
                ctk.CTkLabel(card, text=f"Current: {auction['price']}", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
                ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 12)).pack(anchor="w", padx=10)
                ctk.CTkLabel(card, text=auction['status'], font=("Arial", 12, "italic")).pack(anchor="w", padx=10)
        
        

        '''
        columns = 1  # Number of cards per row

        for index, auction in enumerate(self.sample_auctions):
            row = index // columns
            col = index % columns

            card = ctk.CTkFrame(master=scrollable_list, width=250, height=280, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=5)
            card.grid_propagate(False)

            # === Auction Image (real image if available) ===
            if "image" in auction and os.path.exists(auction["image"]):
                auction_image = ctk.CTkImage(Image.open(auction["image"]), size=(230, 120))
                image_label = ctk.CTkLabel(card, image=auction_image, text="")
                image_label.image = auction_image  # Keep reference to avoid garbage collection
            else:
                image_label = ctk.CTkLabel(card, text="[Image Here]", width=230, height=120, fg_color="#444")

            image_label.pack(pady=(10, 5), padx=10)

            # === Auction Details ===
            # ctk.CTkLabel(card, text=f"@{auction['host']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"{auction["Name"]}", font=("Arial", 14, "bold")).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Current: {auction['price']}", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(2, 0))
            ctk.CTkLabel(card, text=f"Time Left: {auction['time_left']}", font=("Arial", 12)).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=auction['status'], font=("Arial", 12, "italic")).pack(anchor="w", padx=10, pady=(0, 5))

        
    def open_add_item_window(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Auction Item")
        popup.geometry("320x300")
        popup.resizable(False, False)
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        name_entry = ctk.CTkEntry(popup, placeholder_text="Item Name")
        name_entry.pack(pady=10)

        price_entry = ctk.CTkEntry(popup, placeholder_text="Starting Price")
        price_entry.pack(pady=10)

        auction_duration_entry = ctk.CTkEntry(popup, placeholder_text="Auction Duration (in hours)")
        auction_duration_entry.pack(pady=10)

        image_path_var = ctk.StringVar()

        def upload_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        ctk.CTkButton(popup, text="📁 Upload Image", command=upload_image).pack(pady=10)
        image_label = ctk.CTkLabel(popup, textvariable=image_path_var, font=("Arial", 10), wraplength=250)
        image_label.pack(pady=5)

        def add_item():
            name = name_entry.get()
            price = "$"+price_entry.get()
            auction_duration = auction_duration_entry.get()
            img_path = image_path_var.get()

            if name and price:
                # self.add_auction_card(name, price, img_path if img_path else None)
                self.sample_auctions.append(
                    {"Name": name, "price": price, "time_left": auction_duration_entry.get(), "status": "Active", "image": img_path}
                )
                # self.render_auction_cards() # Refresh the auction cards
                popup.destroy()

        ctk.CTkButton(popup, text="Add Item", command=add_item).pack(pady=20)

# Run for demo
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
