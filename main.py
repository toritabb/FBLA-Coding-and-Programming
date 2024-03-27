import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv

## Create the main window
root = tk.Tk()
root.title("HRHS CTE Partners")
root.configure(background='white')


## Text for ReadMe
program_info = """
The HRHS CTE Partners Management System is a Python program built using the Tkinter library.
This system helps in the management of information related to business and community partners 
for HRHS's Career and Technical Education department. It provides a user-friendly interface 
for viewing partner details, searching for partners, and generating reports in CSV format.

Features:
Easily view partner information such as Name, Address, Email, etc.
Quickly search for partners by name using a dynamic search system.
Generate reports on partner information and export them in CSV files for backup and ease of use.

Usage:
Existing Partners - displays current partners' information, allows sorting, and exporting data to CSV.
Add Partner - provides functionality for adding and saving new partners to the system.
Documentation - describes the modules we used to create our program and the copyright for images used.

Dependencies:
Requires Python 3.12 installed on your system.
Install the pillow library using 'pip install pillow'


Program designed in Python 3.12 for FBLA Colorado by Alexander Fiduccia and Joe Hopkins.
"""


## Text for Documentation
library_documentation = """
Libraries Used:

Tkinter
Tkinter is the standard graphical user interface toolkit for Python. It provides various tools for creating GUIs.
In our project, it is used for creating the windows, buttons, text, and other gui elements.

PIL (Python Imaging Library)
PIL is a library for opening, manipulating, and saving images.
We used PIL in order to add our school's logo and to make our program more visually enticing.

CSV
CSV is a simple file format used to store data, such as a spreadsheet or a database.
We incorporated the CSV library to allow users to export partner information to a file for backup and ease of use.

All images are used under public domain or are original creations.
"""

## Display Text Function
def display_text(text):
  global current_window
  current_window = tk.Toplevel(root)  # Store the current window for back button navigation
  current_window.title("Basic Program Information")
  text_label = tk.Label(current_window, text=text)
  text_label.pack()
  back_button = tk.Button(current_window, text="Back", command=back_to_selection_screen)
  back_button.pack()

## Back Button
def back_to_selection_screen():
  current_window.destroy()  # Close the current window

##################
#Existing Partners
##################
## Data for the chart
partners = []
# Function to read CSV file and populate the partners list
with open(r'C:\Users\tkmou\OneDrive\Desktop\FBLA-Coding-and-Programming-Project\partners.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        partners.append(row)
      
## Existing Partners Button
def display_existing_partners():
  existing_partners_window = tk.Toplevel(root)
  existing_partners_window.title("Existing Partners")   # Create a new window
  
  ## Create a Treeview widget for the chart
  partners_chart = tk.ttk.Treeview(existing_partners_window, columns=("Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"))
  partners_chart.heading("Number", text="#")
  partners_chart.heading("Name", text="Name")
  partners_chart.heading("Address", text="Address")
  partners_chart.heading("Phone", text="Phone")
  partners_chart.heading("Email", text="Email")
  partners_chart.heading("Contact", text="Contact")
  partners_chart.heading("Industry", text="Industry")
  partners_chart.column("Number", width=40)
  partners_chart.column("Name", width=175)
  partners_chart.column("Address", width=175)
  partners_chart.column("Phone", width=100)
  partners_chart.column("Email", width=200)
  partners_chart.column("Contact", width=120)
  partners_chart.column("Industry", width=160)
  partners_chart.pack()
  
  ## Insert the partner data into the chart
  for partner in partners:
      partners_chart.insert("", tk.END, values=(partner["Number"], partner["Name"], partner["Address"], partner["Phone"], partner["Email"], partner["Contact"], partner["Industry"]))
    
  ## Add the Back Button
  back_button = tk.Button(existing_partners_window, text="Back", command=lambda: existing_partners_window.destroy())
  back_button.pack()
  
  ## Export Button
  def export_to_csv():
    # Ask for Filename and location
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not filename:
      return

    # Open the file in write mode
    with open(filename, "w", newline="") as csvfile:
      writer = csv.writer(csvfile)

      # Write Partner Header Rows
      writer.writerow(["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"])

      # Write Partner Data Rows
      for partner in partners:
        writer.writerow([partner["Number"], partner["Name"], partner["Address"], partner["Phone"], partner["Email"], partner["Contact"], partner["Industry"]])

  ## GUI Export Button
  export_button = tk.Button(existing_partners_window, text="Export Chart", command=export_to_csv)
  export_button.pack(side="left")

  ## Add a Search Bar
  search_label = tk.Label(existing_partners_window, text="Search:")
  search_label.pack(side="left", padx=(800, 0))
  search_bar = ttk.Entry(existing_partners_window, width=30)  # Create a search bar widget

  # Filter Partner Names Based on input
  def filter_partners(A):
      search_text = search_bar.get().lower()  # Any capitalization works
      filtered_partners = [partner for partner in partners if search_text in partner["Name"].lower()]

      # Sort by deleting and re-entering partners
      partners_chart.delete(*partners_chart.get_children())
      for partner in filtered_partners:
          partners_chart.insert("", tk.END, values=(partner["Number"], partner["Name"], partner["Address"], partner["Phone"], partner["Email"], partner["Contact"], partner["Industry"]))

  search_bar.bind("<KeyRelease>", filter_partners)  # Trigger search on every key release (no need for enter)
  search_bar.pack()  # Display the search bar



##################
#Add Partners
##################

## Format the information for the CSV file
def save_partners():
  with open(r"C:\Users\tkmou\OneDrive\Desktop\FBLA-Coding-and-Programming-Project\partners.csv", "w", newline="") as csvfile:  # Open in write mode
      fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      # Only write header if the file is empty
      if csvfile.tell() == 0:
          writer.writeheader()

      # Determine the next partner number
      next_number = 1
      if any("Number" in partner for partner in partners):  # Check if any partner has "Number"
          next_number = max(int(partner["Number"]) for partner in partners if "Number" in partner) + 1

      # Add the number to each partner and write them to the CSV file if missing
      for partner in partners:
          if "Number" not in partner:
              partner["Number"] = str(next_number) 
          writer.writerow(partner)
          next_number += 1


## All the Buttons and GUI interaction for adding info
def add_partner():
  add_partner_window = tk.Toplevel(root)
  add_partner_window.title("Add Partner")

  # User input labels and entry fields
  name_label = tk.Label(add_partner_window, text="Name:")
  name_label.pack()
  name_entry = tk.Entry(add_partner_window)
  name_entry.pack()

  address_label = tk.Label(add_partner_window, text="Address:")
  address_label.pack()
  address_entry = tk.Entry(add_partner_window)
  address_entry.pack()

  phone_label = tk.Label(add_partner_window, text="Phone:")
  phone_label.pack()
  phone_entry = tk.Entry(add_partner_window)
  phone_entry.pack()

  email_label = tk.Label(add_partner_window, text="Email:")
  email_label.pack()
  email_entry = tk.Entry(add_partner_window)
  email_entry.pack()

  contact_label = tk.Label(add_partner_window, text="Contact:")
  contact_label.pack()
  contact_entry = tk.Entry(add_partner_window)
  contact_entry.pack()

  industry_label = tk.Label(add_partner_window, text="Industry:")
  industry_label.pack()
  industry_entry = tk.Entry(add_partner_window)
  industry_entry.pack()

  # Add the Submit Button
  submit_button = ttk.Button(add_partner_window, text="Add Partner", command=lambda: submit_partner(name_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), contact_entry.get(), industry_entry.get()))
  submit_button.pack()

  # Add the Back Button
  back_button = tk.Button(add_partner_window, text="Back", command=lambda: add_partner_window.destroy())
  back_button.pack()

  
## Submit Partner info into CSV
  def submit_partner(name, address, phone, email, contact, industry):
    # Create new partner dictionary
    new_partner = {"Number": str(len(partners) + 1), "Name": name, "Address": address, "Phone": phone, "Email": email, "Contact": contact, "Industry": industry}

    # Add new partner to partners list
    partners.append(new_partner)

    # Save partners to CSV and close page
    save_partners()
    add_partner_window.destroy()


##################
#Main Screen
##################

# Define Main-Screen-Button Click Functions
def button_click(page):
  if page == "ReadMe":
      display_text(program_info)  # Display basic program information and instructions
  elif page == "Existing Partners":
      display_existing_partners() # Display current partners and allow for sorting and exporting
  elif page == "Add Partner":
      add_partner()  # Provide functionality for adding new partners
  elif page == "Documentation":
      display_text(library_documentation)  # Display library documentation and copyright information


# Button Addition
readme_button = tk.Button(root, text="ReadMe", command=lambda: button_click("ReadMe"))
partners_button = tk.Button(root, text="Existing Partners", command=lambda: button_click("Existing Partners"))
add_partner_button = tk.Button(root, text="Add Partner", command=lambda: button_click("Add Partner"))
documentation_button = tk.Button(root, text="Documentation", command=lambda: button_click("Documentation"))

# Image Addition
image = Image.open(r"C:\Users\tkmou\OneDrive\Desktop\FBLA-Coding-and-Programming-Project\falcon.jpg")
resized_image = image.resize((100, 100))  # Adjust width and height as needed
photo_image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(root, image=photo_image, borderwidth=0)

# Arrange credits
credits_label = tk.Label(root, text="Program Designed in Python 3.12 for FBLA Colorado by Joe Hopkins and Alexander Fiduccia", font=("Arial", 6,), fg="black", background="white")
credits_label.grid(row=8, column=1, columnspan=4, padx=10, pady=10)
# Arrange title
title_label = tk.Label(root, text="HRHS CTE Partners", font=("Helvetica", 24, "bold"), fg="blue", background="white")
title_label.grid(row=0, column=2, columnspan=4, padx=10, pady=10)
# Arrange image
image_label.grid(row=0, column=0)
# Arrange buttons
readme_button.grid(row=5, column=0, pady=10)
partners_button.grid(row=6, column=0, pady=10)
add_partner_button.grid(row=7, column=0,pady=10)
documentation_button.grid(row=8, column=0, pady=10)

# Start the GUI event loop
root.mainloop()
