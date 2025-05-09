import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def round_corners(img: Image.Image, radius: int) -> Image.Image:
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + img.size, radius=radius, fill=255)
    img.putalpha(mask)
    return img

class ProfileWindow(ctk.CTkToplevel):
    def __init__(self, master, user_data, on_save=None):
        super().__init__(master)
        self.title(f"{user_data.get('username', 'User')}'s Profile")
        self.geometry("480x650")
        self.resizable(False, False)

        self.user_data = user_data
        self.on_save = on_save
        self.edit_mode = False
        self.profile_image_path = "assets/profile.png"

        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.pack(padx=20, pady=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.container,
                                        text=f"{self.user_data.get('username', 'User')}'s Profile",
                                        font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(10, 5))

        self.image_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.image_frame.pack(pady=10)

        self.load_profile_image()

        self.info_frame = ctk.CTkFrame(self.container, corner_radius=10)
        self.info_frame.pack(pady=20, fill="x", expand=True)

        fields = [
            ("Username", "username"),
            ("User ID", "user_id"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Date of Birth", "dob"),
            ("Balance", "balance")
        ]

        self.entries = {}
        for label_text, key in fields:
            row = ctk.CTkFrame(self.info_frame, fg_color="transparent")
            row.pack(fill="x", pady=8, padx=10)

            label = ctk.CTkLabel(row, text=f"{label_text}:", font=("Arial", 16), width=120, anchor="w")
            label.pack(side="left")

            entry = ctk.CTkEntry(row, font=("Arial", 16))
            entry.insert(0, str(user_data.get(key, "")))
            entry.configure(state="disabled")
            entry.pack(side="left", fill="x", expand=True)

            self.entries[key] = entry

        self.action_button = ctk.CTkButton(self.container, text="Edit Profile", command=self.toggle_edit_mode)
        self.action_button.pack(pady=10, anchor="e", padx=20)

    def load_profile_image(self):
        try:
            original_img = Image.open(self.profile_image_path).resize((200, 200))
            rounded_img = round_corners(original_img, radius=15)
            self.profile_image = ctk.CTkImage(rounded_img, size=(200, 200))
            self.image_label = ctk.CTkLabel(self.image_frame, image=self.profile_image, text="")
            self.image_label.pack()
        except Exception:
            self.image_label = ctk.CTkLabel(self.image_frame, text="[Image Not Found]", font=("Arial", 14, "italic"))
            self.image_label.pack()


    def toggle_edit_mode(self):
        if not self.edit_mode:
            self.edit_mode = True
            for key in ("username", "first_name", "last_name"):
                self.entries[key].configure(state="normal")

            self.image_label.bind("<Button-1>", self.change_profile_picture)
            self.action_button.configure(text="Save Changes")
        else:
            try:
                for key, entry in self.entries.items():
                    val = entry.get()
                    if key == "balance":
                        val = float(val)
                    self.user_data[key] = val

                self.user_data["profile_pic"] = self.profile_image_path  # Save the new profile picture path

            # ✅ Save to JSON
                with open("profile_data.json", "w") as f:
                    json.dump({
                        "username": self.user_data["username"],
                        "first_name": self.user_data["first_name"],
                        "last_name": self.user_data["last_name"],
                        "profile_pic": self.profile_image_path
                    }, f, indent=4)

                if self.on_save:
                    self.on_save(self.user_data)

                messagebox.showinfo("Success", "Profile updated successfully!")

                self.title(f"{self.user_data.get('username', 'User')}'s Profile")
                self.title_label.configure(text=f"{self.user_data.get('username', 'User')}'s Profile")

                for key in self.entries:
                    self.entries[key].configure(state="disabled")

                self.image_label.unbind("<Button-1>")
                self.action_button.configure(text="Edit Profile")
                self.edit_mode = False

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for balance.")


    def change_profile_picture(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            self.profile_image_path = file_path
            self.image_label.destroy()
            self.load_profile_image()

if __name__ == "__main__":
    import os
    import json

    root = ctk.CTk()
    root.withdraw()

    if os.path.exists("profile_data.json"):
        with open("profile_data.json", "r") as f:
            saved_data = json.load(f)
    else:
        saved_data = {
            "username": "SBA",
            "first_name": "Shreyastha",
            "last_name": "Banik",
            "profile_pic": "assets/profile.png"
        }

    sample_user = {
        "user_id": "123456",
        "dob": "2006-01-01",
        "balance": "1000.00",
        **saved_data
    }

    def save_callback(data):
        print("Updated data:", data)

    ProfileWindow(root, sample_user, save_callback)
    root.mainloop()
    root.destroy()