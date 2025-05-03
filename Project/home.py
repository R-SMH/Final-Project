# home.py
import customtkinter as ctk
from PIL import Image
import os, json

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.controller = controller  # reference to Dashboard
        self.build()

    def build(self):
        # Place your summary_label, summary_frame, and auction_section code here
        # Just like how you have it now, but use self instead of master

        # Example:
        summary_label = ctk.CTkLabel(self, text="Summary", font=("Arial", 18, "bold"))
        summary_label.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 0))

        # etc...
