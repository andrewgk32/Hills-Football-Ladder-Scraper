import tkinter as tk
import tkinter.ttk as ttk
import json
import subprocess
from tkinter import messagebox
from tkinter import Tk, Label, PhotoImage
from PIL import Image, ImageTk


# Function to load and display the current table
def show_table():
    with open('data.json', 'r') as file:
        data = json.load(file)
        # Display the table using your desired format or widget
        table_window = tk.Toplevel()
        table_window.title("Table")

        # Create the Treeview widget
        table = ttk.Treeview(table_window)
        table.pack(fill='both', expand=True)
        
        # Define columns
        columns = ["Club", "Games Played", "Won", "Drawn", "Lost", "Points", "Goal Difference"]
        
        # Configure column headings
        table['columns'] = columns
        table.column("#0", width=0, stretch=tk.NO)  # Hide the default first column

        for col in columns:
            table.heading(col, text=col)
            table.column(col, anchor=tk.CENTER)

        # Insert data into the table
        for row_data in data:
            table.insert("", tk.END, values=list(row_data.values()))

# Function to request the scraper file to generate new JSON data
def generate_data():
    with open('data.json', 'r') as file:
        previous_data = json.load(file)
    subprocess.run(['python', 'scrape.py'])  # Replace 'scrape.py' with your scraper file name


    # Load the new data
    with open('data.json', 'r') as file:
        new_data = json.load(file)

    if new_data != previous_data:
        print("Data has changed!")
        messagebox.showinfo("Data Change", "Data has changed!")  # Show a pop-up message in the GUI
    else:
        print("No changes in data.")
        messagebox.showinfo("No Data Change", "No changes in data.")
    
    
# Create the main application window
def on_configure(event):
    window_width = event.width
    window_height = event.height

    # Calculate the appropriate font size based on the window size
    button_font_size = min(int(window_width / 60), int(window_height / 30))
    label_font_size = min(int(window_width / 100), int(window_height / 50))

    # Configure the font size for the buttons
    style.configure("TButton", font=("Arial", button_font_size))

    # Configure the font size for the label
    label.config(font=("Arial", label_font_size))

window = tk.Tk()
window.title("Table Viewer")
window.geometry("800x400")
window.configure(bg="#00aeef")  # Set background color to #00aeef

style = ttk.Style(window)
label = ttk.Label(window, text="Football Ladder Generator", font=("Arial", 24), foreground="white", background="#00aeef")
label.pack(pady=10)
sub_heading_label = ttk.Label(window, text="Specifically for AAMen 11", font=("Arial", 14, "bold"), foreground="white", background="#00aeef")
sub_heading_label.pack(pady=5)

# Create the button frame
button_frame = tk.Frame(window, bg="#00aeef")  # Set button frame background color to #00aeef
button_frame.pack(pady=20, side=tk.BOTTOM)

# Create a custom button class with desired styling
class CustomButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(foreground="white", background="#044197", width=15, relief=tk.FLAT, padx=15, pady=20, font=("Arial", 20))

# Create the "Show Table" button using the custom button class
show_table_button = CustomButton(button_frame, text="Show Table", command=show_table)
show_table_button.pack(side=tk.LEFT, padx=30)

# Create the "Generate Data" button using the custom button class
generate_data_button = CustomButton(button_frame, text="Generate Data", command=generate_data)
generate_data_button.pack(side=tk.LEFT, padx=30)

window.mainloop()

# Start the GUI event loop
window.mainloop()
