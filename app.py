
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect('ShopEase.db')
cursor = conn.cursor()

# Global variables
login_type_var = None
session = {}
cart = []
order_frame = None
cart_frame = None


# Create trigger to block account after 3 login failures
login_blocked_trigger_sql = '''
CREATE TRIGGER IF NOT EXISTS BlockAccountAfterFailures
AFTER INSERT ON LoginAttempts
FOR EACH ROW
BEGIN
    UPDATE Users
    SET Account_Status = 'Blocked'
    WHERE User_ID = NEW.User_ID
        AND (
            SELECT COUNT(*)
            FROM LoginAttempts
            WHERE User_ID = NEW.User_ID AND Success = 0
        ) >= 3;
END;
'''

# Create trigger to apply discount
# Create trigger to apply discount
# Create trigger to apply discount
apply_discount_trigger_sql = '''
CREATE TRIGGER IF NOT EXISTS ApplyDiscount
AFTER INSERT ON Cart
BEGIN
    -- Calculate the total amount for the newly inserted row
    UPDATE Cart
    SET Total_Amount = (NEW.Quantity * NEW.Item_Price) -
                       CASE 
                           WHEN (SELECT COUNT(*) FROM Cart) > 1000 THEN (NEW.Quantity * NEW.Item_Price * 0.1)
                           ELSE 0
                       END
    WHERE rowid = NEW.rowid;
END;
'''



cursor.execute(login_blocked_trigger_sql)
cursor.execute(apply_discount_trigger_sql)
conn.commit()


# Function to authenticate user
# Function to authenticate user
def authenticate_user():
    name = name_entry.get()
    password = password_entry.get()
    login_type = login_type_var.get()
    
    if login_type == "User":
        cursor.execute('''SELECT User_ID FROM Users WHERE Name=? AND Password=?''', (name, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            session['user_type'] = 'User'  # Add user type to session
            display_items()
            order_frame.pack()
            cart_frame.pack()
            messagebox.showinfo("Success", "Logged in successfully!")
        else:
            # Increment the login attempts and check if the account should be blocked
            cursor.execute('''INSERT INTO LoginAttempts (User_ID, Success) VALUES (?, 0)''', (name,))
            conn.commit()
            cursor.execute('''SELECT COUNT(*) FROM LoginAttempts WHERE User_ID=? AND Success=0''', (name,))
            failed_attempts = cursor.fetchone()[0]
            if failed_attempts >= 3:
                cursor.execute('''UPDATE Users SET Account_Status = 'Blocked' WHERE Name = ?''', (name,))
                conn.commit()
                messagebox.showerror("Error", "Invalid credentials. Your account has been blocked. Please contact support.")
            else:
                messagebox.showerror("Error", "Invalid credentials.")
    elif login_type == "Admin":
        admin_login()
    else:
        messagebox.showerror("Error", "Please select login type.")

# Function for admin login
def admin_login():
    admin_id = admin_id_entry.get()
    password = password_entry.get()
    cursor.execute('''SELECT * FROM Admin WHERE Admin_ID=? AND Password=?''', (admin_id, password))
    admin = cursor.fetchone()
    if admin:
        session['user_type'] = 'Admin'
        display_admin_options()
        display_inventory("Admin")  # Display inventory for admin
        messagebox.showinfo("Success", "Admin logged in successfully!")
    else:
        messagebox.showerror("Error", "Invalid admin credentials.")
        
def register_user(name, password, phone_no, address):
    try:
        cursor.execute('''INSERT INTO Users (Name, Password, Phone_No, Address) VALUES (?, ?, ?, ?)''', (name, password, phone_no, address))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", "Failed to register user.")
        
        
# Function to display items list
def display_items():
    cursor.execute('''SELECT Item_Name, Item_Price FROM Items''')
    items = cursor.fetchall()
    items_listbox.delete(0, tk.END)
    for item in items:
        items_listbox.insert(tk.END, f"{item[0]} - Price: {item[1]}")

# Function to display current inventory
def display_inventory(user_type):
    if user_type == 'Admin':
        cursor.execute('''SELECT Item_Name, Quantity FROM Items''')
        inventory = cursor.fetchall()
        inventory_text.delete(1.0, tk.END)  # Clear previous inventory display
        inventory_text.insert(tk.END, "Current Inventory:\n")
        for item in inventory:
            inventory_text.insert(tk.END, f"{item[0]} - Quantity: {item[1]}\n")
    else:
        messagebox.showerror("Error", "You do not have permission to view the inventory.")
    
        

def order_items():
    if 'user_id' not in session:
        messagebox.showerror("Error", "Please login first.")
        return
    
    item_name = item_entry.get().strip()
    quantity_str = quantity_entry.get().strip()
    
    if not item_name or not quantity_str:
        if cart:  # Check if the cart is not empty before showing the success message
            # Calculate total cart price before applying discount
            total_cart_price = sum(item[2] for item in cart)
            
            if total_cart_price > 1000:
                # Apply discount if total cart price is greater than $1000
                discount = total_cart_price * 0.1
                total_cart_price -= discount
                for i, item in enumerate(cart):
                    cart[i] = (item[0], item[1], item[1] * item[2] - (item[1] * item[2] * 0.1))
                messagebox.showinfo("Discount Applied", f"You have received a discount of 10% ({discount:.2f})!")
            
            # Calculate total cart price after discount
            total_cart_price_after_discount = sum(item[2] for item in cart)
            
            # Show total cart price after discount
            
            messagebox.showinfo("Success", "Order placed successfully!")
            
            # Increment the order history only if an order is placed successfully
            user_id = session['user_id']
            cursor.execute('''UPDATE Users SET Order_History = Order_History + 1 WHERE User_ID = ?''', (user_id,))
            conn.commit()
        else:
            messagebox.showerror("Error", "Please enter both item name and quantity.")
        return
    
    try:
        quantity = int(quantity_str)
        cursor.execute('''SELECT Quantity, Item_Price FROM Items WHERE Item_Name=?''', (item_name,))
        item_data = cursor.fetchone()
        if item_data:
            current_quantity, item_price = item_data
            if quantity < 0 and abs(quantity) > sum(item[1] for item in cart if item[0] == item_name):
                messagebox.showerror("Error", "Cannot reduce quantity beyond what's in the cart.")
                return
                
            if current_quantity < quantity:
                messagebox.showerror("Error", f"Not enough {item_name} in stock.")
                return
                
            # Update inventory
            new_quantity = max(0, current_quantity - quantity)  # Ensure quantity does not go below 0
            cursor.execute('''UPDATE Items SET Quantity=? WHERE Item_Name=?''', (new_quantity, item_name))
            conn.commit()
            
            # Update cart
            item_in_cart = False
            for i, item in enumerate(cart):
                if item[0] == item_name:
                    new_item_quantity = item[1] + quantity
                    if new_item_quantity <= 0:
                        # Remove the item from the cart if the quantity becomes 0 or negative
                        del cart[i]
                    else:
                        cart[i] = (item[0], new_item_quantity, item[2] + quantity * item_price)
                    item_in_cart = True
                    break
            
            if not item_in_cart and quantity > 0:
                # If the item is not in the cart and quantity is positive, add it
                cart.append((item_name, quantity, quantity * item_price))
            
            # Calculate total cart price after discount, if applied
            
            # if total_cart_price > 1000:
            #     discount = total_cart_price * 0.1
            #     total_cart_price -= discount
            
            show_cart()
            
            return
        else:
            messagebox.showerror("Error", "Item not found.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity.")
        return





# Function to show cart details
def show_cart():
    if 'user_id' not in session:
        messagebox.showerror("Error", "Please login first.")
        return
    
    cart_text.delete(1.0, tk.END)
    if cart:
        total_cart_price = sum(item[2] for item in cart)
        
        if total_cart_price > 1000:
            # Apply discount if total cart price is greater than $1000
            discount = total_cart_price * 0.1
            total_cart_price -= discount
            cart_text.insert(tk.END, f"Discount Applied: You have received a discount of 10% ({discount:.2f})!\n\n")
        
        cart_text.insert(tk.END, "Cart Details:\n")
        for item in cart:
            cart_text.insert(tk.END, f"Item: {item[0]}, Quantity: {item[1]}, Price: {item[2]}\n")
        cart_text.insert(tk.END, f"\nTotal Cart Price: {total_cart_price:.2f}\n")
    else:
        cart_text.insert(tk.END, "Cart is empty.")


# Function to display admin options
def display_admin_options():
    # Implement your admin options here
    pass

def display_all_customer_analysis():
    # Check if the logged-in user is an admin
    if session.get('user_type') != 'Admin':
        messagebox.showerror("Error", "Only admins can view all customer analysis.")
        return

    cursor.execute('''SELECT User_ID, Name, Phone_No, Address, Order_History FROM Users''')
    all_customers = cursor.fetchall()

    all_customer_analysis_text.delete(1.0, tk.END)  # Clear previous data
    all_customer_analysis_text.insert(tk.END, "All Customer Analysis:\n")
    for customer in all_customers:
        all_customer_analysis_text.insert(tk.END, f"User ID: {customer[0]}\n")
        all_customer_analysis_text.insert(tk.END, f"Name: {customer[1]}\n")
        all_customer_analysis_text.insert(tk.END, f"Phone No: {customer[2]}\n")
        all_customer_analysis_text.insert(tk.END, f"Address: {customer[3]}\n")
        all_customer_analysis_text.insert(tk.END, f"Order History: {customer[4]}\n\n")
        
        
def display_customer_analysis_for_current_user():
    if 'user_id' not in session:
        messagebox.showerror("Error", "Only Users can Access this")
        return
    
    user_id = session['user_id']
    cursor.execute('''SELECT User_ID, Name, Phone_No, Address, Order_History FROM Users WHERE User_ID=?''', (user_id,))
    user_details = cursor.fetchone()
    
    if user_details:
        my_details_text.delete(1.0, tk.END)  # Clear previous data
        my_details_text.insert(tk.END, "My Details:\n")
        my_details_text.insert(tk.END, f"User ID: {user_details[0]}\n")
        my_details_text.insert(tk.END, f"Name: {user_details[1]}\n")
        my_details_text.insert(tk.END, f"Phone No: {user_details[2]}\n")
        my_details_text.insert(tk.END, f"Address: {user_details[3]}\n")
        my_details_text.insert(tk.END, f"Order History: {user_details[4]}\n\n")
    else:
        messagebox.showerror("Error", "User details not found.")
        


# Main function
def main():
    # Create main window
    root = tk.Tk()
    root.title("ShopEase")
    
    # Login frame
    login_frame = tk.Frame(root)
    login_frame.pack(pady=5)
    tk.Label(login_frame, text="Login As:").grid(row=0, column=0)
    global login_type_var
    login_type_var = tk.StringVar()
    login_type_var.set("User")
    tk.Radiobutton(login_frame, text="User", variable=login_type_var, value="User").grid(row=0, column=1)
    tk.Radiobutton(login_frame, text="Admin", variable=login_type_var, value="Admin").grid(row=0, column=2)
    
    tk.Label(login_frame, text="Name/Admin ID:").grid(row=1, column=0)
    global name_entry, password_entry, admin_id_entry
    name_entry = tk.Entry(login_frame, width=20)
    name_entry.grid(row=1, column=1)
    password_entry = tk.Entry(login_frame, show="*", width=20)
    password_entry.grid(row=2, column=1)
    admin_id_entry = tk.Entry(login_frame, width=20)
    admin_id_entry.grid(row=1, column=2)
    
    tk.Label(login_frame, text="Password:").grid(row=2, column=0)
    
    tk.Button(login_frame, text="Login", command=authenticate_user, width=15).grid(row=3, columnspan=3)
    
    # Items frame
    global items_frame
    items_frame = tk.Frame(root)
    items_frame.pack(pady=5)
    tk.Label(items_frame, text="Items List:").grid(row=0, column=0)
    global items_listbox
    items_listbox = tk.Listbox(items_frame, width=50, height=5)
    items_listbox.grid(row=1, column=0)

    # Order frame
    global order_frame
    order_frame = tk.Frame(root)
    global item_entry, quantity_entry
    tk.Label(order_frame, text="Item Name:").grid(row=0, column=0)
    tk.Label(order_frame, text="Quantity:").grid(row=1, column=0)
    item_entry = tk.Entry(order_frame, width=20)
    item_entry.grid(row=0, column=1)
    quantity_entry = tk.Entry(order_frame, width=20)
    quantity_entry.grid(row=1, column=1)
    tk.Button(order_frame, text="Order", command=order_items, width=15).grid(row=2, columnspan=2)

    # Cart frame
    global cart_frame
    cart_frame = tk.Frame(root)
    tk.Label(cart_frame, text="Cart:").grid(row=0, column=0)
    global cart_text
    cart_text = tk.Text(cart_frame, width=50, height=5)
    cart_text.grid(row=1, column=0)

    # Button to display current inventory
    tk.Button(root, text="Display Inventory", command=display_inventory, width=20).pack()
    
    # Text widget to display inventory
    global inventory_text
    inventory_text = tk.Text(root, width=50, height=5)
    inventory_text.pack()
    
    # tk.Button(root, text="Display My Details", command=display_customer_analysis_for_current_user, width=20).pack()
    # Text widget to display customer analysis
    
    # Button to display current user's details
    tk.Button(root, text="Display My Details", command=display_customer_analysis_for_current_user, width=20).pack(pady=5)

# Text widget to display current user's details
    global my_details_text
    my_details_text = tk.Text(root, width=30, height=5)
    my_details_text.pack(padx=10, pady=5)
    
    
    tk.Button(root, text="Display All Customer Analysis", command=lambda: display_all_customer_analysis(), width=30).pack(pady=5)
    
    # Text widget to display all customer analysis
    global all_customer_analysis_text
    all_customer_analysis_text = tk.Text(root, width=30, height=5)
    all_customer_analysis_text.pack(padx=10, pady=5)

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()




