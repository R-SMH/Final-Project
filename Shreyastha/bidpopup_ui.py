import customtkinter as ctk
from PIL import Image
import os


def open_bid_popup(parent, auction, on_submit=None):
    popup = ctk.CTkToplevel(parent)
    popup.title(f"Bid on {auction['Name']}")
    popup.geometry("650x320")
    popup.grab_set()
    popup.focus_force()
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=1)

    main_frame = ctk.CTkFrame(popup)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=2)
    main_frame.grid_rowconfigure(0, weight=1)

    # ===== LEFT SECTION: Details & Input =====
    left = ctk.CTkFrame(main_frame, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=10)
    left.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
    left.grid_rowconfigure(6, weight=1)
    left.grid_columnconfigure(0, weight=1)

    def info_row(text, value, row):
        ctk.CTkLabel(left, text=f"{text}", font=("Arial", 13, "bold")).grid(row=row, column=0, sticky="w", padx=5)
        ctk.CTkLabel(left, text=value, font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=5)

    info_row("Item:", auction["Name"], 0)
    info_row("Current Price:", f"${auction['price']}", 1)
    info_row("Owner:", auction.get("owner", "Unknown"), 2)
    info_row("Highest Bidder:", auction.get("highest_bidder", "None"), 3)

    ctk.CTkLabel(left, text="Your Bid:", font=("Arial", 13)).grid(row=4, column=0, sticky="w", pady=(20, 2), padx=5)
    bid_entry = ctk.CTkEntry(left, placeholder_text="Enter bid amount")
    bid_entry.grid(row=5, column=0, sticky="ew", padx=5)

    feedback = ctk.CTkLabel(left, text="", text_color="red", font=("Arial", 12))
    feedback.grid(row=6, column=0, sticky="w", pady=(5, 0), padx=5)

    def submit_bid():
        try:
            bid = float(bid_entry.get())
            current_price = float(auction["price"])

            if bid <= current_price:
                feedback.configure(text=f"⚠️ Must be greater than ${current_price:.2f}")
            else:
                if on_submit:
                    on_submit(bid)
                popup.destroy()
        except ValueError:
            feedback.configure(text="⚠️ Enter a valid number")

    ctk.CTkButton(left, text="Submit Bid", command=submit_bid).grid(row=7, column=0, sticky="ew", pady=(20, 5), padx=5)

    # ===== RIGHT SECTION: Image =====
    right = ctk.CTkFrame(main_frame, fg_color="transparent")
    right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

    if "image" in auction and os.path.exists(auction["image"]):
        img = ctk.CTkImage(Image.open(auction["image"]), size=(240, 160))
        ctk.CTkLabel(right, image=img, text="").pack(expand=True)
    else:
        ctk.CTkLabel(right, text="[No Image]", width=240, height=160, fg_color="#444").pack(expand=True)
