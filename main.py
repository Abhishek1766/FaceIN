import cv2
import numpy as np
import mysql.connector
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os

# Global variable to store database connection details
db_config = {
    "host": " ",
    "user": " ",
    "password": " ",
    "database": " "
}

# MySQL connection
def connect_db():
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

# Test database connection
def test_db_connection():
    try:
        connect_db()
        messagebox.showinfo("Success", "Database connection successful!")
    except mysql.connector.Error as err:
        messagebox.showerror("Connection Error", f"Failed to connect to database: {str(err)}")

# Capture and save image
def capture_image(name):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        image_path = f"images/{name}.jpg"
        cv2.imwrite(image_path, frame)
        cam.release()
        return image_path
    cam.release()
    return None

# Add user to database
def add_user(name):
    image_path = capture_image(name)
    if image_path:
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (name, image_path) VALUES (%s, %s)", (name, image_path))
            db.commit()
            messagebox.showinfo("Success", "User  added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            cursor.close()
            db.close()
    else:
        messagebox.showerror("Error", "Failed to capture image.")

# Delete user from database
def delete_user(name):
    try:
        db = connect_db()
        cursor = db.cursor()
        
        # Execute the SELECT statement
        cursor.execute("SELECT image_path FROM users WHERE name = %s", (name,))
        result = cursor.fetchone()  # Fetch the result
        
        if result:
            image_path = result[0]
            if os.path.exists(image_path):
                os.remove(image_path)  # Delete the image file
            cursor.execute("DELETE FROM users WHERE name = %s", (name,))
            db.commit()
            messagebox.showinfo("Success", "User  deleted successfully!")
        else:
            messagebox.showerror("Error", "User  not found.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        cursor.close()
        db.close()

# View all users
def view_users():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM users")
        users = cursor.fetchall()
        
        user_list = "\n".join([user[0] for user in users]) if users else "No users found."
        messagebox.showinfo("User  List", user_list)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        cursor.close()
        db.close()

# GUI functions
def add_user_gui():
    name = name_entry.get()
    if name:
        add_user(name)
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

def delete_user_gui():
    name = simpledialog.askstring("Delete User", "Enter the name of the user to delete:")
    if name:
        delete_user(name)
    else:
        messagebox.showwarning("Input Error", "Please enter a name.")

def view_users_gui():
    view_users()

def configure_db_gui():
    def save_db_config():
        db_config["host"] = host_entry.get()
        db_config["user"] = user_entry.get()
        db_config["password"] = password_entry.get()
        db_config["database"] = database_entry.get()
        messagebox.showinfo("Success", "Database configuration saved!")
        test_db_connection()  # Test the connection after saving
        config_window.destroy()

    config_window = ctk.CTkToplevel(root)
    config_window.title("Database Configuration")
    config_window.geometry("300x300")

    ctk.CTkLabel(config_window, text="Host:").pack(pady=5)
    host_entry = ctk.CTkEntry(config_window)
    host_entry.pack(pady=5)

    ctk.CTkLabel(config_window, text=":User ").pack(pady=5)
    user_entry = ctk.CTkEntry(config_window)
    user_entry .pack(pady=5)

    ctk.CTkLabel(config_window, text="Password:").pack(pady=5)
    password_entry = ctk.CTkEntry(config_window, show="*")
    password_entry.pack(pady=5)

    ctk.CTkLabel(config_window, text="Database:").pack(pady=5)
    database_entry = ctk.CTkEntry(config_window)
    database_entry.pack(pady=5)

    save_button = ctk.CTkButton(config_window, text="Save", command=save_db_config)
    save_button.pack(pady=20)

# Main application window
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Change the color theme

root = ctk.CTk()  # Create a CustomTkinter window
root.title("FaceIN")
root.geometry("400x400")

# Create a canvas for the background image
canvas = ctk.CTkCanvas(root, width=100, height=100)
canvas.pack()

# Load and set the logo image
image_path = "FaceIN.png"  # Ensure the logo image is in the same directory
logo_image = Image.open(image_path)

# Resize the image (for example, to 200x400 pixels)
new_size = (100, 100)  # Set the desired size
logo_image = logo_image.resize(new_size, Image.LANCZOS)  # Resize the image

# Create a PhotoImage instance with the loaded image
logo_photo = ImageTk.PhotoImage(logo_image)

# Draw the image on the canvas
canvas.create_image(0, 0, anchor='nw', image=logo_photo)

# Set window icon
root.iconbitmap("FaceIN.ico")  # Ensure the icon file is in the same directory

# Name entry
name_label = ctk.CTkLabel(root, text="Enter Name:", text_color="white")
name_label.pack(pady=20)

name_entry = ctk.CTkEntry(root, placeholder_text="Type your name here")
name_entry.pack(pady=10)

# Add user button
add_user_button = ctk.CTkButton(root, text="Add User", command=add_user_gui)
add_user_button.pack(pady=10)

# View users button
view_users_button = ctk.CTkButton(root, text="View Users", command=view_users_gui)
view_users_button.pack(pady=10)

# Delete user button
delete_user_button = ctk.CTkButton(root, text="Delete User", command=delete_user_gui)
delete_user_button.pack(pady=10)

# Configure database button
configure_db_button = ctk.CTkButton(root, text="Configure Database", command=configure_db_gui)
configure_db_button.pack(pady=10)

# Run the application
root.mainloop()
