import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- 1. DATABASE SETUP ---
def setup_database():
    """Creates the database and the customers table if they don't exist."""
    conn = sqlite3.connect('customer_info.db')
    cursor = conn.cursor()
    
    # Create table with the specified fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birthday TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            contact_method TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- 2. GUI AND DATABASE INTERACTION ---
def submit_data():
    """Gets data from GUI, inserts it into the database, and clears the form."""
    # Get data from entry fields
    name = name_entry.get()
    birthday = birthday_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    contact_method = contact_method_combo.get()

    # Simple validation to ensure name is entered
    if not name:
        messagebox.showwarning("Input Error", "Name is a required field.")
        return

    # Insert data into the database
    try:
        conn = sqlite3.connect('customer_info.db')
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute('''
            INSERT INTO customers (name, birthday, email, phone, address, contact_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, birthday, email, phone, address, contact_method))
        
        conn.commit()
        conn.close()
        
        # Clear the form and show success message
        clear_form()
        messagebox.showinfo("Success", "Customer information submitted successfully!")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def clear_form():
    """Clears all input fields in the GUI."""
    name_entry.delete(0, tk.END)
    birthday_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    contact_method_combo.set('') # Clears the combobox selection

# --- 3. GUI DESIGN ---
# Main application window
root = tk.Tk()
root.title("Customer Information Management System")
root.geometry("450x350")

# Use a frame for better organization
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# --- Input Fields and Labels ---
# Create and place labels and corresponding entry widgets in a grid
labels_texts = ["Name:", "Birthday (YYYY-MM-DD):", "Email:", "Phone Number:", "Address:", "Preferred Contact:"]
for i, text in enumerate(labels_texts):
    label = ttk.Label(main_frame, text=text)
    label.grid(row=i, column=0, padx=5, pady=10, sticky="w")

# Entry widgets
name_entry = ttk.Entry(main_frame, width=40)
birthday_entry = ttk.Entry(main_frame, width=40)
email_entry = ttk.Entry(main_frame, width=40)
phone_entry = ttk.Entry(main_frame, width=40)
address_entry = ttk.Entry(main_frame, width=40)

# Dropdown menu for contact method
contact_options = ["Email", "Phone", "Mail"]
contact_method_combo = ttk.Combobox(main_frame, values=contact_options, width=37, state="readonly")

# Place entry widgets on the grid
name_entry.grid(row=0, column=1, padx=5, pady=10)
birthday_entry.grid(row=1, column=1, padx=5, pady=10)
email_entry.grid(row=2, column=1, padx=5, pady=10)
phone_entry.grid(row=3, column=1, padx=5, pady=10)
address_entry.grid(row=4, column=1, padx=5, pady=10)
contact_method_combo.grid(row=5, column=1, padx=5, pady=10)

# Submit Button
submit_button = ttk.Button(main_frame, text="Submit", command=submit_data)
submit_button.grid(row=6, column=1, padx=5, pady=20, sticky="e")


# --- 4. RUN THE APPLICATION ---
if __name__ == "__main__":
    setup_database()  # Ensure the database and table exist
    root.mainloop()   # Start the GUI event loop