import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import requests


# Text for ReadMe
program_info = """
The HRHS CTE Partners Management System is a Python program built using the Tkinter library.
This system helps in the management of information related to business and community partners 
for HRHS"s Career and Technical Education department. It provides a user-friendly interface 
for viewing partner details, searching for partners, and generating reports in CSV format.

Features:
Easily view partner information such as Name, Address, Email, etc.
Quickly search for partners by name using a dynamic search system.
Generate reports on partner information and export them in CSV files for backup and ease of use.

Usage:
Existing Partners - displays current partners" information, allows sorting, and exporting data to CSV.
Add Partner - provides functionality for adding and saving new partners to the system.
Documentation - describes the modules we used to create our program and the copyright for images used.

Dependencies:
Requires Python 3.12 installed on your system.
Install the pillow library using "pip install pillow"


Program designed in Python 3.12 for FBLA Colorado by Alexander Fiduccia and Joe Hopkins.
"""


# Text for Documentation
library_documentation = """
Libraries Used:

Tkinter
Tkinter is the standard graphical user interface toolkit for Python. It provides various tools for creating GUIs.
In our project, it is used for creating the windows, buttons, text, and other gui elements.

PIL (Python Imaging Library)
PIL is a library for opening, manipulating, and saving images.
We used PIL in order to add our school"s logo and to make our program more visually enticing.

CSV
CSV is a simple file format used to store data, such as a spreadsheet or a database.
We incorporated the CSV library to allow users to export partner information to a file for backup and ease of use.

All images are used under public domain or are original creations.
"""


# Display Text Function
def display_text_window(text):
    text_window = tk.Toplevel(root)  # Store the current window for back button navigation
    text_window.title("Basic Program Information")

    # Hide the main window and focus on the new window
    text_window.focus()
    text_window.protocol("WM_DELETE_WINDOW", lambda: close_window(text_window))
    text_window.resizable(False, False)
    root.withdraw()

    # Display the text
    text_label = tk.Label(text_window, text=text)
    text_label.place(x=20, y=20)

    # Add the back button
    back_button = tk.Button(text_window, text="Back", command=lambda: close_window(text_window))
    back_button.place(x=text_label.winfo_reqwidth() * 0.5 + 2, y=text_label.winfo_reqheight() + 40)

    print(back_button.winfo_reqwidth())

    # Center the window
    center_window(text_window, text_label.winfo_reqwidth() + 40, text_label.winfo_reqheight() + 86)


#######################
#  Existing Partners  #
#######################

# Data for the chart
partners = []

# Function to read CSV file and populate the partners list
with open("partners.csv") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        partners.append(row)


# Existing Partners Button
def display_existing_partners_window():
    existing_partners_window = tk.Toplevel(root)
    existing_partners_window.title("Existing Partners")   # Create a new window

    # Hide the main window and focus on the existing partners window
    center_window(existing_partners_window, 1012, 412)
    existing_partners_window.focus()
    existing_partners_window.protocol("WM_DELETE_WINDOW", lambda: close_window(existing_partners_window))
    existing_partners_window.resizable(False, False)
    root.withdraw()

    fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]

    # Create a Treeview widget for the chart
    partners_chart = ttk.Treeview(existing_partners_window, columns=("Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"), height=15)
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

    partners_chart["show"] = "headings"
    partners_chart.place(x=20, y=20)

    # Insert the partner data into the chart
    def update_partner_chart(_):
        partners_chart.delete(*partners_chart.get_children())
        for partner in partners:
            partners_chart.insert("", tk.END, values=[partner[field] for field in fieldnames])

    partners_chart.bind("<<Update>>", update_partner_chart)
    partners_chart.event_generate("<<Update>>")
 
    # Add the Back Button
    back_button = tk.Button(existing_partners_window, text="Back", command=lambda: close_window(existing_partners_window))
    back_button.place(x=20, y=366)

    add_partner_button = tk.Button(existing_partners_window, text="Add Partner", command=lambda: display_add_partner_window(partners_chart))
    add_partner_button.place(x=173, y=366)

    # Export Button
    def export_to_csv():
        # Ask for Filename and location
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        if not filename:
            return

        # Open the file in write mode
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write Partner Header Rows
            writer.writerow(fieldnames)

            # Write Partner Data Rows
            for partner in partners:
                writer.writerow([partner[field] for field in fieldnames])

    # GUI Export Button
    export_button = tk.Button(existing_partners_window, text="Export Chart", command=export_to_csv)
    export_button.place(x=76, y=366)

    # Deletes the selected partners
    def delete_partners():
        partner_ids = partners_chart.selection()

        if partner_ids:
            for id in reversed(partner_ids):
                partners.pop(partners_chart.index(id))

            save_partners()

            partners_chart.event_generate("<<Update>>")

    # Delete Partner Button
    delete_button = tk.Button(existing_partners_window, text="Delete Selected Partners", command=delete_partners)
    delete_button.place(x=267, y=366)

    # Add search field customization
    search_customization_lable = tk.Label(existing_partners_window, text="Search By:")
    search_customization_lable.place(x=593, y=368)

    search_by = tk.StringVar(value="Name")
    search_by_dropdown = tk.OptionMenu(existing_partners_window, search_by, *fieldnames[1:], command=lambda _: filter_partners())
    search_by_dropdown.config(pady=1, width=7)
    search_by_dropdown.place(x=653, y=366)

    # Add a Search Bar
    search_label = tk.Label(existing_partners_window, text="Search:")
    search_label.place(x=760, y=368)

    search_bar = ttk.Entry(existing_partners_window, width=30)
    search_bar.bind("<KeyRelease>", lambda _: filter_partners()) # Trigger search on every key release (no need for enter)
    search_bar.place(x=806, y=368)

    # Filter partners based on search bar input
    def filter_partners():
        search_text = search_bar.get().lower()  # Ignore capitalization
        filtered_partners = [partner for partner in partners if search_text in partner[search_by.get()].lower()]

        # Sort by deleting and re-entering partners
        partners_chart.delete(*partners_chart.get_children())
        for partner in filtered_partners:
            partners_chart.insert("", tk.END, values=[partner[field] for field in fieldnames])


##################
#  Add Partners  #
##################

# Format the information for the CSV file
def save_partners():
    with open("partners.csv", "w", newline="") as csvfile:  # Open in write mode
        fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Add the number to each partner and write them to the CSV file if missing
        for i, partner in enumerate(partners):
            partner["Number"] = str(i + 1) 
            writer.writerow(partner)


# All the Buttons and GUI interaction for adding info
def display_add_partner_window(partners_chart):
    add_partner_window = tk.Toplevel(root)
    add_partner_window.title("Add Partner")

    # Hide the main window and focus on the add partner window
    center_window(add_partner_window, 164, 448)
    add_partner_window.focus_force()
    add_partner_window.protocol("WM_DELETE_WINDOW", add_partner_window.destroy)
    add_partner_window.resizable(False, False)

    # Add title
    title_label = tk.Label(add_partner_window, text="Add Partner", font=("Arial", 15, "bold"))
    title_label.place(x=22.5, y=20)
    print(title_label.winfo_reqwidth(), title_label.winfo_reqheight())

    # User input labels and entry fields
    name_label = tk.Label(add_partner_window, text="Name:")
    name_label.place(x=61.5, y=70)
    name_entry = tk.Entry(add_partner_window)
    name_entry.place(x=20, y=91)

    address_label = tk.Label(add_partner_window, text="Address:")
    address_label.place(x=56.5, y=115)
    address_entry = tk.Entry(add_partner_window)
    address_entry.place(x=20, y=136)

    phone_label = tk.Label(add_partner_window, text="Phone:")
    phone_label.place(x=56, y=160)
    phone_entry = tk.Entry(add_partner_window)
    phone_entry.place(x=20, y=181)

    email_label = tk.Label(add_partner_window, text="Email:")
    email_label.place(x=63, y=205)
    email_entry = tk.Entry(add_partner_window)
    email_entry.place(x=20, y=226)

    contact_label = tk.Label(add_partner_window, text="Contact:")
    contact_label.place(x=56.5, y=250)
    contact_entry = tk.Entry(add_partner_window)
    contact_entry.place(x=20, y=271)

    industry_label = tk.Label(add_partner_window, text="Industry:")
    industry_label.place(x=56, y=295)
    industry_entry = tk.Entry(add_partner_window)
    industry_entry.place(x=20, y=316)

    # Validate the input and then add partner
    def submit_partner(name: str, address: str, phone: str, email: str, contact: str, industry: str):
        requirements = [
            address.split(' ')[0].isdigit(),
            '-' in phone,
            all(part.isdigit() for part in phone.split('-')),
        ]
        if all(requirements):
            pass

        # Create new partner dictionary
        new_partner = {"Number": str(len(partners) + 1), "Name": name, "Address": address, "Phone": phone, "Email": email, "Contact": contact, "Industry": industry}

        # Add new partner to partners list
        partners.append(new_partner)
        
        # Update partner list
        partners_chart.event_generate("<<Update>>")

        # Save partners to CSV and close page
        save_partners()
        add_partner_window.destroy()

    # Add the Submit Button
    submit_button = tk.Button(add_partner_window, text="Add Partner", command=lambda: submit_partner(name_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), contact_entry.get(), industry_entry.get()))
    submit_button.place(x=45, y=356)

    # Add the Back Button
    back_button = tk.Button(add_partner_window, text="Back", command=add_partner_window.destroy)
    back_button.place(x=64, y=402)


# center the window based on the screen size
def center_window(window, width, height):
    window.geometry('{}x{}+{}+{}'.format(width, height, int(0.5 * (root.winfo_screenwidth() - width)), int(0.5 * (root.winfo_screenheight() - height))))


# Close the window and reopen the main window
def close_window(window):
    root.deiconify()
    window.destroy()


# Define Main-Screen-Button Click Functions
def button_click(page):
    match page:
        case "ReadMe":
            display_text_window(program_info[1:-1])  # Display basic program information and instructions
        case "Existing Partners":
            display_existing_partners_window() # Display current partners and allow for sorting and exporting
        case "Documentation":
            display_text_window(library_documentation[1:-1])  # Display library documentation and copyright information


#################
#  Main Window  #
#################

# Create the main window
root = tk.Tk()
root.title("HRHS CTE Partners")
root.configure(background="white")
center_window(root, 465, 316)
root.resizable(False, False)

# Add school logo
image = Image.open(requests.get("https://upload.wikimedia.org/wikipedia/en/2/2f/HRHS_logo.png", stream=True).raw).resize((100, 100))  # load the image from wikipedia and resize it
photo_image = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo_image, borderwidth=0)
image_label.place(x=20, y=20)

# Add title
title_label = tk.Label(root, text="HRHS CTE Partners", font=("Helvetica", 24, "bold"), fg="blue", background="white")
title_label.place(x=140, y=20)

# Add buttons
readme_button = tk.Button(root, text="ReadMe", command=lambda: button_click("ReadMe"))
readme_button.place(x=20, y=140)

partners_button = tk.Button(root, text="Existing Partners", command=lambda: button_click("Existing Partners"))
partners_button.place(x=20, y=186)

documentation_button = tk.Button(root, text="Documentation", command=lambda: button_click("Documentation"))
documentation_button.place(x=20, y=232)

# Add credits
credits_label = tk.Label(root, text="Program Designed in Python 3.12 for FBLA by Alexander Fiduccia and Joe Hopkins", font=("Arial", 7), background="white")
credits_label.place(x=54, y=278)

# Start the GUI event loop
root.mainloop()
