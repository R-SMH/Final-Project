import customtkinter as ctk
from PIL import Image
# from app import user_id
# Caden will import a function like:
# from _ import *

class Dashboard(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1200x600")
        # user_id

        # === Main Layout Frame ===
        main_frame = ctk.CTkFrame(master=self)
        main_frame.pack(fill="both", expand=True)

        main_frame.grid_columnconfigure(0, weight=0)   # Sidebar
        main_frame.grid_columnconfigure(1, weight=1)   # Main content
        main_frame.grid_rowconfigure(0, weight=0)  # Top bar
        main_frame.grid_rowconfigure(1, weight=0)  # Summary label
        main_frame.grid_rowconfigure(2, weight=0)  # Summary cards
        main_frame.grid_rowconfigure(3, weight=1)  # Main content below


        # === Top Bar ===
        top_bar = ctk.CTkFrame(master=main_frame, height=70)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="new",)
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        platform_title = ctk.CTkLabel(top_bar, text="BidMasters", font=("Arial", 20, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")
        
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
        scrollbar = ctk.CTkScrollbar(master=sidebar_container, orientation="vertical", command=sidebar_canvas.yview)

        scrollable_frame = ctk.CTkFrame(master=sidebar_canvas)
        scroll_window = sidebar_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def resize_scroll_region(event):
            sidebar_canvas.itemconfig(scroll_window, width=event.width)

        scrollable_frame.bind(
            "<Configure>", lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        sidebar_canvas.bind("<Configure>", resize_scroll_region)

        sidebar_canvas.configure(yscrollcommand=scrollbar.set, width=250)

        sidebar_canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")


        # === Sidebar Buttons ===
        for i in range(20):
            ctk.CTkButton(
                master=scrollable_frame,
                text=f"Menu Button {i+1}",
                width=160,
                anchor="w"
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


# Run for demo
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
