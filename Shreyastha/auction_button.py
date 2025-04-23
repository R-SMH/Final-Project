# auction_button.py

import customtkinter as ctk

def create_auction_button(parent, dashboard_instance):
    def clear_right_side():
        # Remove all widgets from right side (col=1) rows 1 to 4
        for widget in dashboard_instance.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    info = child.grid_info()
                    if int(info.get("column", -1)) == 1 and int(info.get("row", -1)) >= 1:
                        child.grid_forget()

        print("Auction view loaded (blank for now)")

    return ctk.CTkButton(
        master=parent,
        text="Auction",
        width=130,
        anchor="w",
        command=clear_right_side
    )