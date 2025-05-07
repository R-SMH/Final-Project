import customtkinter as ctk
from PIL import Image
import os
import mysql.connector
import json

def fetch_auction_details(auction_id):
    """Fetch auction details based on auction_id."""
    try:
        connection = mysql.connector.connect(
            host="138.47.226.93",
            user="otheruser",
            passwd="GroupProjectPassword",
            database="AuctionDB"
        )
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT auction_id, itemName, CurrentPrice, StartingPrice, itemDescription, Auctionlength, imageLink, User_ID, bidder_id
            FROM NormalAuction
            WHERE auction_id = %s
        """
        cursor.execute(query, (auction_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"[ERROR] Error fetching auction details: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def open_bid_popup(parent, auction_id, user_id, on_submit=None, refresh_ui=None, add_notification=None):
    auction = fetch_auction_details(auction_id)  # Now fetch_auction_details is accessible
    if not auction:
        print(f"[ERROR] No auction found for auction_id: {auction_id}")
        return

    print(f"[DEBUG] Auction data: {auction}")  # Debug the auction dictionary
    popup = ctk.CTkToplevel(parent)
    popup.title("Bid on Item")
    popup.geometry("700x375")
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
    left.grid_rowconfigure((0, 1, 2, 3, 4, 5,6), weight=0)
    left.grid_rowconfigure(6, weight=1)
    left.grid_columnconfigure(0, weight=1)

    def info_row(text, value, row):
        ctk.CTkLabel(left, text=f"{text}", font=("Arial", 13, "bold")).grid(row=row, column=0, sticky="w", padx=5)
        ctk.CTkLabel(left, text=value, font=("Arial", 13)).grid(row=row, column=0, sticky="e", padx=5)

    print(f"[DEBUG] user_id: {user_id}")

    def fetch_owner_username(owner_id):
        """Fetch the owner's username based on owner_id."""
        try:
            connection = mysql.connector.connect(
                host="138.47.226.93",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT username FROM Users WHERE user_id = %s"
            cursor.execute(query, (owner_id,))
            result = cursor.fetchone()
            return result["username"] if result else "Unknown"
        except mysql.connector.Error as err:
            print(f"[ERROR] Error fetching owner's username: {err}")
            return "Unknown"
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    def fetch_previous_bidder_username(bidder_id):
        """Fetch the username of the previous bidder based on bidder_id."""
        try:
            connection = mysql.connector.connect(
                host="138.47.226.93",
                user="otheruser",
                passwd="GroupProjectPassword",
                database="AuctionDB"
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT username FROM Users WHERE user_id = %s"
            cursor.execute(query, (bidder_id,))
            result = cursor.fetchone()
            return result["username"] if result else "None"
        except mysql.connector.Error as err:
            print(f"[ERROR] Error fetching previous bidder username: {err}")
            return "None"
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    # Fetch owner and previous bidder details
    owner_username = fetch_owner_username(auction["User_ID"])
    previous_bidder_username = fetch_previous_bidder_username(auction["bidder_id"])

    # Display auction details
    info_row("Item:", auction["itemName"], 0)
    info_row("Current Price:", f"${auction['CurrentPrice']}", 1)
    info_row("Owner:", owner_username, 2)
    info_row("Highest Bidder:", previous_bidder_username, 3)
    # Add item description with proper wrapping and padding
    description_label = ctk.CTkLabel(
        left,
        text=f"Item Description: {auction['itemDescription']}",
        font=("Arial", 12),
        wraplength=400,  # Wrap text to fit within the popup
        justify="left"
    )
    description_label.grid(row=4, column=0, sticky="w", padx=5, pady=(10, 20))  # Add padding below the description


  
    ctk.CTkLabel(left, text="Your Bid:", font=("Arial", 13)).grid(row=5, column=0, sticky="w", pady=(20, 2), padx=5)
    bid_entry = ctk.CTkEntry(left, placeholder_text="Enter bid amount")
    bid_entry.grid(row=5, column=0, sticky="ew", padx=5)

    feedback = ctk.CTkLabel(left, text="", text_color="red", font=("Arial", 12))
    feedback.grid(row=6, column=0, sticky="w", pady=(5, 0), padx=5)

    def submit_bid():
        try:
            bid = float(bid_entry.get())
            current_price = float(auction["CurrentPrice"])

            if bid <= current_price:
                feedback.configure(text=f"⚠️ Must be greater than ${current_price:.2f}")
            else:
                connection = mysql.connector.connect(
                    host="138.47.226.93",
                    user="otheruser",
                    passwd="GroupProjectPassword",
                    database="AuctionDB"
                )
                cursor = connection.cursor(dictionary=True)


                 # Fetch the user's current balance
                balance_query = "SELECT balance FROM Users WHERE user_id = %s"
                cursor.execute(balance_query, (user_id,))
                user_data = cursor.fetchone()

                if not user_data:
                    feedback.configure(text="⚠️ Unable to fetch user balance.")
                    return

                user_balance = float(user_data["balance"])
                print(f"[DEBUG] User balance: ${user_balance}")

                # Check if the user has enough balance to place the bid
                if user_balance < bid:
                    feedback.configure(text=f"⚠️ Insufficient balance. Your balance is ${user_balance:.2f}.")
                    return
                # Step 1: Update the bidder_id to the current user's user_id
                update_bidder_query = """
                    UPDATE NormalAuction
                    SET bidder_id = %s
                    WHERE auction_id = %s
                """
                cursor.execute(update_bidder_query, (user_id, auction_id))
                print(f"[DEBUG] Updated bidder_id to {user_id} for auction_id {auction_id}")

                # Step 2: Update the current price to the bid amount
                update_price_query = """
                    UPDATE NormalAuction
                    SET CurrentPrice = %s
                    WHERE auction_id = %s
                """
                cursor.execute(update_price_query, (bid, auction_id))
                print(f"[DEBUG] Updated CurrentPrice to {bid} for auction_id {auction_id}")

                # Step 3: Deduct the bid amount from the user's balance
                deduct_balance_query = """
                    UPDATE Users
                    SET balance = balance - %s
                    WHERE user_id = %s
                """
                cursor.execute(deduct_balance_query, (bid, user_id))
                print(f"[DEBUG] Deducted ${bid} from user_id {user_id}'s balance")

                # Step 4: Refund the previous bidder if they were outbid
                if auction["bidder_id"]:
                    refund_query = """
                        UPDATE Users
                        SET balance = balance + %s
                        WHERE user_id = %s
                    """
                    cursor.execute(refund_query, (current_price, auction["bidder_id"]))
                    print(f"[DEBUG] Refunded ${current_price} to previous bidder_id {auction['bidder_id']}")

                    # Add a notification for the previous bidder
                    if add_notification and auction["bidder_id"]:
                        notification_message = f"You've been outbid on '{auction['itemName']}'!"
                        add_notification(notification_message)  # Send notification to the previous bidder
                        print(f"[DEBUG] Outbid notification sent to bidder_id {auction['bidder_id']}: {notification_message}")

            # Commit the
                # Commit the changes to the database
                connection.commit()

                # Step 5: Fetch the updated highest bidder's username
                highest_bidder_username = fetch_previous_bidder_username(user_id)
                print(f"[DEBUG] Highest bidder username: {highest_bidder_username}")

                # Update the info_row to display the updated highest bidder
                info_row("Highest Bidder:", highest_bidder_username, 3)

                # Notify the user and close the popup
                feedback.configure(text="✅ Bid placed successfully!", text_color="green")
                if add_notification:
                    notification_message = f"✅ You successfully placed a bid of ${bid:.2f} on '{auction['itemName']}'!"
                    add_notification(notification_message)  # Send notification to the current user
                    print(f"[DEBUG] Bid notification sent to user_id {user_id}: {notification_message}")

                if on_submit:
                    on_submit(bid)
                if refresh_ui:
                    refresh_ui()  # Trigger the UI refresh
                popup.destroy()

        except ValueError:
            feedback.configure(text="⚠️ Enter a valid number")
        except mysql.connector.Error as err:
            feedback.configure(text=f"⚠️ Database error: {err}")
            print(f"Database error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    ctk.CTkButton(left, text="Submit Bid", command=submit_bid).grid(row=7, column=0, sticky="ew", pady=(20, 5), padx=5)

   # ===== RIGHT SECTION: Image =====
    right = ctk.CTkFrame(main_frame, fg_color="transparent")
    right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

    # Use "imageLink" instead of "image"
    if "imageLink" in auction and os.path.exists(auction["imageLink"]):
        img = ctk.CTkImage(Image.open(auction["imageLink"]), size=(240, 160))
        ctk.CTkLabel(right, image=img, text="").pack(expand=True)
    else:
        ctk.CTkLabel(right, text="[No Image]", width=240, height=160, fg_color="#444").pack(expand=True)
