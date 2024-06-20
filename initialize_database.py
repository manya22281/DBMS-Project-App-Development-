# import sqlite3

# # Connect to SQLite database
# conn = sqlite3.connect('ShopEase.db')
# cursor = conn.cursor()

# # Create triggers
# create_triggers_sql = """
# CREATE TRIGGER IF NOT EXISTS trg_update_cart_amount 
# AFTER INSERT ON Cart 
# FOR EACH ROW 
# BEGIN
#     UPDATE Cart 
#     SET Total_Amount = (
#         SELECT SUM(Item_Price * Quantity) 
#         FROM Items 
#         WHERE Item_Name IN (SELECT Item_Name FROM Items WHERE Cart_ID = NEW.Cart_ID)
#     ) 
#     WHERE Cart_ID = NEW.Cart_ID;
# END;

# CREATE TRIGGER IF NOT EXISTS trg_update_order_history 
# AFTER INSERT ON Payment 
# FOR EACH ROW 
# BEGIN
#     UPDATE Users 
#     SET Order_History = 
#         CASE 
#             WHEN Order_History IS NULL THEN 'Order' || NEW.Cart_ID
#             ELSE Order_History || ', Order' || NEW.Cart_ID 
#         END
#     WHERE User_ID = NEW.User_ID;
# END;
# """

# # Execute trigger creation statements
# cursor.executescript(create_triggers_sql)

# # Function to order items and return the total price for the ordered items
# def order_item(Item_Name, quantity):  
#     cursor.execute('''SELECT * FROM Items WHERE Item_Name=?''', (Item_Name,))
#     item = cursor.fetchone()
#     if item:
#         available_quantity = item[2]  
#         if available_quantity >= quantity:
#             new_quantity = available_quantity - quantity
#             item_price = item[1] 

#             # Update quantity in the database
#             cursor.execute('''UPDATE Items SET Quantity=? WHERE Item_Name=?''', (new_quantity, Item_Name))
#             conn.commit()

#             # Return the total price for the ordered items
#             return item_price * quantity
#         else:
#             print("Insufficient quantity available for", Item_Name)
#             return 0  # Return 0 if insufficient quantity
#     else:
#         print("Item not found:", Item_Name)
#         return 0  # Return 0 if item not found

# # Function for inventory analysis
# def inventory_analysis():
#     cursor.execute('''SELECT Item_Name, Quantity FROM Items''')
#     inventory = cursor.fetchall()
#     if inventory:
#         print("Inventory Analysis:")
#         for item in inventory:
#             print(f"{item[0]} - Quantity: {item[1]}")
#     else:
#         print("No items in inventory.")

# # Initialize total cart price
# total_cart_price = 0

# # Order items and accumulate total price
# milk_price = order_item('Milk', 3)
# total_cart_price += milk_price

# crocin_price = order_item('Crocin', 5)
# total_cart_price += crocin_price

# # Print total cart price
# print(f"Total cart price: {total_cart_price}")

# # Display inventory analysis
# inventory_analysis()

# # Close connection
# conn.close()


import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('ShopEase.db')
cursor = conn.cursor()

# Function to authenticate user
def authenticate_user():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    cursor.execute('''SELECT User_ID FROM Users WHERE Name=? AND Password=?''', (name, password))
    user = cursor.fetchone()
    if user:
        return user[0]
    else:
        print("Invalid credentials.")
        return None

# Function to display items list
def display_items():
    cursor.execute('''SELECT Item_Name, Item_Price FROM Items''')
    items = cursor.fetchall()
    print("Items List:")
    for item in items:
        print(f"{item[0]} - Price: {item[1]}")

# Function to order items
def order_items(user_id, cart):
    while True:
        item_name = input("Enter the item name (or press Enter to finish): ")
        if not item_name:
            break
        quantity = int(input("Enter the quantity: "))
        cursor.execute('''SELECT * FROM Items WHERE Item_Name=?''', (item_name,))
        item = cursor.fetchone()
        if item:
            # Perform ordering logic here
            # For simplicity, let's assume the order is successful
            cart.append((item_name, quantity, item[1] * quantity))  # Add item to cart
            
        else:
            print("Item not found.")

# Function to show cart details
def show_cart(cart):
    if cart:
        print("Cart Details:")
        for item in cart:
            print(f"Item: {item[0]}, Quantity: {item[1]}")
        total_cart_price = sum(item[2] for item in cart)
        print(f"Total Cart Price: {total_cart_price}")
        print("Item ordered successfully!")
    else:
        print("Cart is empty.")

# Main function
def main():
    # Authenticate user
    user_id = authenticate_user()
    if user_id:
        # Display items list
        display_items()
        
        # Initialize cart
        cart = []
        
        # Order items
        order_items(user_id, cart)
        
        # Show cart details
        show_cart(cart)
        
        
# trigger_script = """
# CREATE TRIGGER BlockAccountAfterFailures
# AFTER INSERT ON LoginAttempts
# FOR EACH ROW
# BEGIN
#     UPDATE Users
#     SET Account_Status = 'Blocked'
#     WHERE User_ID = NEW.User_ID
#         AND (
#             SELECT COUNT(*)
#             FROM LoginAttempts
#             WHERE User_ID = NEW.User_ID AND Success = 0
#         ) >= 3;
# END;
# """
# cursor.executescript(trigger_script)

# Run the main function
if __name__ == "__main__":
    main()