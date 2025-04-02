import customtkinter as ctk
from PIL import Image

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("1200x600")

        main_frame = ctk.CTkFrame(master=self)
        main_frame.pack(fill="both", expand=True)

        main_frame.grid_columnconfigure(0, weight=0)   
        main_frame.grid_columnconfigure(1, weight=1)   
        main_frame.grid_rowconfigure(0, weight=0)      
        main_frame.grid_rowconfigure(1, weight=1)      

        top_bar = ctk.CTkFrame(master=main_frame, height=60)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="new", pady = 10)
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=0)

        platform_title = ctk.CTkLabel(top_bar, text="BidMasters", font=("Arial", 20, "bold"))
        platform_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

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

        sidebar_container = ctk.CTkFrame(master=main_frame)
        sidebar_container.grid(row=1, column=0, sticky="ns")

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

        for i in range(20):
            ctk.CTkButton(
                master=scrollable_frame,
                text=f"Menu Button {i+1}",
                width=160,
                anchor="w"
            ).pack(pady=10, padx=0)

        content_area = ctk.CTkFrame(master=main_frame, fg_color="#1a1a1a")
        content_area.grid(row=1, column=1, sticky="nsew")
        ctk.CTkLabel(content_area, text="Dashboard Content Here", font=("Arial", 16)).pack(pady=30)

# FOR TESTING PURPOSES ONLY
if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    app = Dashboard()
    app.mainloop()
