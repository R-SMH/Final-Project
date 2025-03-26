from flask import Flask, request, jsonify
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import socket
import sqlite3
import requests

# ==========================================
# ✅ SERVER CODE
# ==========================================
app = Flask(__name__)

# Get local IP
def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Initialize the database
def init_db():
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS auctions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        price INTEGER NOT NULL,
        bids TEXT
    )''')
    conn.commit()

    # Add sample auctions if none exist
    cursor.execute("SELECT COUNT(*) FROM auctions")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO auctions (item, price, bids) VALUES (?, ?, ?)", ('Laptop', 100, '[]'))
        cursor.execute("INSERT INTO auctions (item, price, bids) VALUES (?, ?, ?)", ('Phone', 50, '[]'))
        conn.commit()

    conn.close()

# View auctions
@app.route('/auctions', methods=['GET'])
def view_auctions():
    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auctions")
    rows = cursor.fetchall()
    conn.close()

    auctions = {row[0]: {'item': row[1], 'price': row[2], 'bids': eval(row[3])} for row in rows}
    return jsonify(auctions)

# Add new auction
@app.route('/add_auction', methods=['POST'])
def add_auction():
    data = request.get_json()
    item = data.get('item')
    price = data.get('price')

    if not item or not price or not isinstance(price, int):
        return jsonify({'error': 'Invalid auction data'}), 400

    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO auctions (item, price, bids) VALUES (?, ?, ?)", (item, price, '[]'))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Auction added successfully'})

# Place a bid
@app.route('/bid/<int:auction_id>', methods=['POST'])
def place_bid(auction_id):
    data = request.get_json()
    bid = data.get('bid')

    conn = sqlite3.connect('auction.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM auctions WHERE id = ?", (auction_id,))
    row = cursor.fetchone()

    if not row:
        return jsonify({'error': 'Auction not found'}), 404

    bids = eval(row[3])
    bids.append(bid)

    cursor.execute("UPDATE auctions SET bids = ? WHERE id = ?", (str(bids), auction_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Bid placed successfully', 'bids': bids})

# Function to run the server in a separate thread
def run_server():
    init_db()
    ip = get_local_ip()
    print(f"Server running at: http://{ip}:5000")
    app.run(host=ip, port=5000)

# ==========================================
# ✅ GUI FUNCTIONS
# ==========================================
def connect():
    """ Connect to the local server """
    try:
        response = requests.get(f'http://{SERVER_IP}:{PORT}/auctions')
        if response.status_code == 200:
            messagebox.showinfo("Connection", "Connected to Local Auction Server")
        else:
            messagebox.showerror("Error", "Failed to connect")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect: {str(e)}")

def view_auctions():
    """ Fetch and display auction items """
    try:
        response = requests.get(f'http://{SERVER_IP}:{PORT}/auctions')
        auctions = response.json()

        auction_display.delete(1.0, tk.END)
        auction_display.insert(tk.END, f"{'ID':<5}{'Item':<15}{'Price':<10}{'Bids':<20}\n")
        auction_display.insert(tk.END, "-" * 55 + "\n")

        for auction_id, details in auctions.items():
            auction_display.insert(tk.END,
                f"{auction_id:<5}{details['item']:<15}${details['price']:<10}{details['bids']}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch auctions: {str(e)}")

def place_bid():
    """ Place a bid on an auction """
    auction_id = simpledialog.askinteger("Bid", "Enter Auction ID:")
    bid_amount = simpledialog.askinteger("Bid", "Enter your bid amount:")

    if auction_id and bid_amount:
        try:
            response = requests.post(
                f'http://{SERVER_IP}:{PORT}/bid/{auction_id}',
                json={'bid': bid_amount}
            )
            if response.status_code == 200:
                messagebox.showinfo("Success", "Bid placed successfully!")
                view_auctions()
            else:
                messagebox.showerror("Error", "Failed to place bid")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to place bid: {str(e)}")

def add_auction():
    """ Add a new auction """
    item = simpledialog.askstring("New Auction", "Enter item name:")
    price = simpledialog.askinteger("New Auction", "Enter starting price:")

    if item and price:
        try:
            response = requests.post(
                f'http://{SERVER_IP}:{PORT}/add_auction',
                json={'item': item, 'price': price}
            )
            if response.status_code == 200:
                messagebox.showinfo("Success", "Auction added successfully!")
                view_auctions()
            else:
                messagebox.showerror("Error", "Failed to add auction")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add auction: {str(e)}")

# ==========================================
# ✅ START SERVER AND GUI TOGETHER
# ==========================================
# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Wait for the server to start
import time
time.sleep(2)

# Use the local server IP
SERVER_IP = get_local_ip()
PORT = '5000'

# ==========================================
# ✅ GUI DESIGN (AESTHETIC)
# ==========================================
root = tk.Tk()
root.title("Local Auction System")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

# Font and color styling
btn_font = ('Helvetica', 12, 'bold')
btn_color = "#0078D7"
btn_fg = "#ffffff"

# Header label
header = tk.Label(root, text="Auction System", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
header.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Connect", command=connect, width=15, font=btn_font, bg=btn_color, fg=btn_fg).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="View Auctions", command=view_auctions, width=15, font=btn_font, bg=btn_color, fg=btn_fg).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Place Bid", command=place_bid, width=15, font=btn_font, bg=btn_color, fg=btn_fg).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Add Auction", command=add_auction, width=15, font=btn_font, bg="#28a745", fg=btn_fg).grid(row=0, column=3, padx=10)

# Auction display
auction_display = scrolledtext.ScrolledText(root, width=80, height=20)
auction_display.pack(padx=10, pady=10)

# Start the GUI
root.mainloop()
