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
Delete Partners - deletes all selected partners. To select partners, click on them, you can select multiple using shift click or control click
Documentation - describes the modules we used to create our program and the copyright for images used.

Dependencies:
Requires Python 3.12 installed on your system.
Install the pillow and requests libraries using "pip install pillow requests"


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

Requests
requests is the python library for getting data from websites, like the images we use in out application.

All images are used under public domain or are original creations.
"""


# Display Text Function
def display_text_window(text: str) -> None:
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

    # Center the window
    center_window(text_window, text_label.winfo_reqwidth() + 40, text_label.winfo_reqheight() + 86)


# Existing Partners Button
def display_existing_partners_window() -> None:
    bg_color = "#4169e1"
    button_color = "#3454b4"
    hover_tip_color = "#6787e7"
    text_box_color = "#b3c3f3"

    existing_partners_window = tk.Toplevel(root, background=bg_color)
    existing_partners_window.title("Existing Partners")   # Create a new window

    # Hide the main window and focus on the existing partners window
    center_window(existing_partners_window, 1012, 412)
    existing_partners_window.focus()
    existing_partners_window.protocol("WM_DELETE_WINDOW", lambda: close_window(existing_partners_window))
    existing_partners_window.resizable(False, False)
    root.withdraw()

    fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]

    def partner_chart_sort_column(chart: ttk.Treeview, column: str, mode: int) -> None:
        if mode == 0:
            column_values = [(int(chart.set(child, "Number")), child) for child in chart.get_children()]
            column_values.sort()
        else:
            column_values = [(chart.set(child, column).lower(), child) for child in chart.get_children()]
            column_values.sort(reverse=bool(mode - 1))

        # rearrange items in sorted positions
        for i, (_, k) in enumerate(column_values):
            chart.move(k, '', i)

        # change mode next time
        chart.heading(column, text=column, command=lambda _col=column: partner_chart_sort_column(chart, _col, (mode + 1) % 3))

    # Create a Treeview widget for the chart
    partners_chart = ttk.Treeview(existing_partners_window, columns=("Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"), show="headings", height=15)
    partners_chart.heading("Number", text="#")
    partners_chart.heading("Name", text="Name", command=lambda _col="Name": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.heading("Address", text="Address", command=lambda _col="Address": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.heading("Phone", text="Phone", command=lambda _col="Phone": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.heading("Email", text="Email", command=lambda _col="Email": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.heading("Contact", text="Contact", command=lambda _col="Contact": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.heading("Industry", text="Industry", command=lambda _col="Industry": partner_chart_sort_column(partners_chart, _col, 0))
    partners_chart.column("Number", width=40)
    partners_chart.column("Name", width=175)
    partners_chart.column("Address", width=175)
    partners_chart.column("Phone", width=100)
    partners_chart.column("Email", width=200)
    partners_chart.column("Contact", width=120)
    partners_chart.column("Industry", width=160)

    partners_chart.place(x=20, y=20)

    # Insert the partner data into the chart
    def update_partner_chart(_) -> None:
        partners_chart.delete(*partners_chart.get_children())
        for partner in partners:
            partners_chart.insert("", tk.END, values=[partner[field] for field in fieldnames])

    partners_chart.bind("<<Update>>", update_partner_chart)
    partners_chart.event_generate("<<Update>>")
 
    # Add the Back Button
    back_button = tk.Button(existing_partners_window, text="Back", command=lambda: close_window(existing_partners_window), background=text_box_color)
    back_button.place(x=20, y=366)

    # Add the Add Partner Button (functionality is marked later)
    add_partner_button = tk.Button(existing_partners_window, text="Add Partner", command=lambda: display_add_partner_window(existing_partners_window, partners_chart), background=text_box_color)
    add_partner_button.place(x=173, y=366)

    # Export Button
    def export_to_csv() -> None:
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
    export_button = tk.Button(existing_partners_window, text="Export Chart", command=export_to_csv, background=text_box_color)
    export_button.place(x=76, y=366)

    # Deletes the selected partners
    def delete_partners() -> None:
        partner_ids = partners_chart.selection()

        if partner_ids:
            def delete() -> None:
                for id in reversed(partner_ids):
                    partners.pop(partners_chart.index(id))

                save_partners()
                partners_chart.event_generate("<<Update>>")

                conformation_window.destroy()

            conformation_window = tk.Toplevel(existing_partners_window, background=bg_color)
            conformation_window.title("Partner Deletion Conformation")
            center_window(conformation_window, 359, 122)
            conformation_window.focus()
            conformation_window.resizable(False, False)

            question_label = tk.Label(conformation_window, text="Are you sure you want to delete all of the selected partners?\nThis action cannot be undone!")
            question_label.place(x=20, y=20)

            cancel_button = tk.Button(conformation_window, text="Cancel", command=conformation_window.destroy, background=button_color)
            cancel_button.place(x=85.7, y=76)

            confirm_button = tk.Button(conformation_window, text="Confirm", command=delete, background=button_color)
            confirm_button.place(x=208.7, y=76)

    # Delete Partner Button
    delete_button = tk.Button(existing_partners_window, text="Delete Selected Partners", command=delete_partners, background=text_box_color)
    delete_button.place(x=267, y=366)

    # Add search field customization
    search_customization_lable = tk.Label(existing_partners_window, text="Search By:", background=bg_color)
    search_customization_lable.place(x=593, y=368)

    search_by = tk.StringVar(value="Name")
    search_by_dropdown = tk.OptionMenu(existing_partners_window, search_by, *fieldnames[1:], command=lambda _: filter_partners())
    search_by_dropdown.config(pady=1, width=7, bg=text_box_color)
    search_by_dropdown.place(x=653, y=366)

    # Add a Search Bar
    search_label = tk.Label(existing_partners_window, text="Search:", background=bg_color)
    search_label.place(x=760, y=368)

    search_bar = tk.Entry(existing_partners_window, width=30, background=text_box_color)
    search_bar.bind("<KeyRelease>", lambda _: filter_partners()) # Trigger search on every key release (no need for enter)
    search_bar.place(x=806, y=368)

    # Filter partners based on search bar input
    def filter_partners() -> None:
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
def save_partners() -> None:
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
def display_add_partner_window(parent_window: tk.Toplevel, partners_chart: ttk.Treeview) -> None:
    bg_color = "#4169e1"
    button_color = "#3454b4"
    hover_tip_color = "#6787e7"
    text_box_color = "#b3c3f3"

    add_partner_window = tk.Toplevel(parent_window, background=bg_color)
    add_partner_window.title("Add Partner")

    # Hide the main window and focus on the add partner window
    center_window(add_partner_window, 254, 448)
    add_partner_window.focus_force()
    add_partner_window.protocol("WM_DELETE_WINDOW", add_partner_window.destroy)
    add_partner_window.resizable(False, False)

    # Add title
    title_label = tk.Label(add_partner_window, text="Add Partner", font=("Arial", 15, "bold"), background=bg_color)
    title_label.place(x=67.5, y=20)

    def add_hover_text(label: tk.Label, text: str) -> None:
        hover_text = tk.Label(add_partner_window, text=text, font=("Arial", 7), background=hover_tip_color)
        label_pos_x = int(label.place_info()["x"]) - (hover_text.winfo_reqwidth() - label.winfo_reqwidth()) * 0.5
        label_pos_y = int(label.place_info()["y"]) - hover_text.winfo_reqheight()

        label.bind("<Enter>", lambda _: hover_text.place(x=label_pos_x, y=label_pos_y))
        label.bind("<Leave>", lambda _: hover_text.place_forget())

    # User input labels and entry fields
    name_label = tk.Label(add_partner_window, text="Name:", background=bg_color)
    name_label.place(x=106.5, y=70)
    name_entry = tk.Entry(add_partner_window, background=text_box_color)
    name_entry.place(x=65, y=91)

    add_hover_text(name_label, "Name must be less than 30 characters long.")

    address_label = tk.Label(add_partner_window, text="Address:", background=bg_color)
    address_label.place(x=101.5, y=115)
    address_entry = tk.Entry(add_partner_window, background=text_box_color)
    address_entry.place(x=65, y=136)

    add_hover_text(address_label, "Address must start with a street number.")

    phone_label = tk.Label(add_partner_window, text="Phone:", background=bg_color)
    phone_label.place(x=105.5, y=160)
    phone_entry = tk.Entry(add_partner_window, background=text_box_color)
    phone_entry.place(x=65, y=181)

    add_hover_text(phone_label, "Phone must be in the format +12 (345)-678-9876\nCountry code, parenthesis, and dashes are optional.")

    email_label = tk.Label(add_partner_window, text="Email:", background=bg_color)
    email_label.place(x=108, y=205)
    email_entry = tk.Entry(add_partner_window, background=text_box_color)
    email_entry.place(x=65, y=226)

    add_hover_text(email_label, "Email must contain an @ and a domain.")

    contact_label = tk.Label(add_partner_window, text="Contact:", background=bg_color)
    contact_label.place(x=101.5, y=250)
    contact_entry = tk.Entry(add_partner_window, background=text_box_color)
    contact_entry.place(x=65, y=271)

    add_hover_text(contact_label, "Contact can only contain letters and spaces.")

    industry_label = tk.Label(add_partner_window, text="Industry:", background=bg_color)
    industry_label.place(x=101, y=295)
    industry_entry = tk.Entry(add_partner_window, background=text_box_color)
    industry_entry.place(x=65, y=316)

    add_hover_text(industry_label, "Industry can only contain letters and spaces.")

    # Validate the input and then add partner
    def submit_partner(name: str, address: str, phone: str, email: str, contact: str, industry: str) -> None:
        def remove_chars(string: str, *chars: str):
            for char in chars:
                string = string.replace(char, "")
            return string

        raw_phone = remove_chars(phone, "-", " ", "+", "(", ")")
        requirements = [
            len(name) < 30,
            address.split(" ")[0].isdigit(),
            raw_phone.isdigit(),
            7 <= len(raw_phone) <= 15,
            "@" in email,
            "." in email,
            remove_chars(contact, " ").isalpha(),
            remove_chars(industry, " ").isalpha()
        ]

        # If all of the validation requirements are met, add the partner
        if all(requirements):
            # Create new partner dictionary
            new_partner = {"Number": str(len(partners) + 1), "Name": name, "Address": address, "Phone": phone, "Email": email, "Contact": contact, "Industry": industry}

            # Add new partner to partners list
            partners.append(new_partner)

            # Update partner list
            partners_chart.event_generate("<<Update>>")

            # Save partners to CSV and close page
            save_partners()
            add_partner_window.destroy()
        else:
        #Issue pop up box
            label = tk.Label(add_partner_window, text="One or more entered fields are not correct\nFor syntax rules hover over a field label", background=text_box_color)
            label.place(x=13,y=335)
            label.pack
            root.after(5000, label.destroy)

    # Add the Submit Button
    submit_button = tk.Button(add_partner_window, text="Add Partner", command=lambda: submit_partner(name_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), contact_entry.get(), industry_entry.get()), background=button_color)
    submit_button.place(x=90, y=356)

    # Add the Back Button
    back_button = tk.Button(add_partner_window, text="Back", command=add_partner_window.destroy, background=button_color)
    back_button.place(x=109, y=402)


# center the window based on the screen size
def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    window.geometry('{}x{}+{}+{}'.format(width, height, int(0.5 * (root.winfo_screenwidth() - width)), int(0.5 * (root.winfo_screenheight() - height))))


# Close the window and reopen the main window
def close_window(window: tk.Toplevel) -> None:
    root.deiconify()
    window.destroy()


# Define Main-Screen-Button Click Functions
def button_click(page: str) -> None:
    match page:
        case "ReadMe":
            display_text_window(program_info[1:-1])  # Display basic program information and instructions
        case "Existing Partners":
            display_existing_partners_window() # Display current partners and allow for sorting and exporting
        case "Documentation":
            display_text_window(library_documentation[1:-1])  # Display library documentation and copyright information


# Data for the chart
partners = []

# Function to read CSV file and populate the partners list
with open("partners.csv") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        partners.append(row)


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
image = Image.open(requests.get("https://upload.wikimedia.org/wikipedia/en/2/2f/HRHS_logo.png", stream=True).raw, formats=["png"]).resize((100, 100))  # load the image from wikipedia and resize it
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
