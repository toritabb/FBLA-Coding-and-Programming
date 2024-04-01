import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import smtplib
import datetime
import os


# Creates a partners.csv file if there isn't one
open("partners.csv", "a").close() if not os.path.exists("partners.csv") else None
program_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(program_directory, "partners.csv")


# Creates a backup folder if there isn't one
backup_folder = os.path.join(program_directory, "Partner Backups")
os.makedirs(backup_folder, exist_ok=True)
backup_date = datetime.datetime.now().strftime("%Y-%m-%d")
backup_file_name = f"partners-COPY-{backup_date}.csv"
backup_file_path = os.path.join(backup_folder, backup_file_name)
with open(file_path, 'r') as f_in:
    with open(backup_file_path, 'w') as f_out:
        for line in f_in:
            f_out.write(line)


# Text for ReadMe
program_info = ""
with open("README.md") as f:
    program_info = f.read()[29:]


# Text for documentation
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

SMTP
SMTP is a simple mail service and is used for user questions through the app



All images are used under public domain or are original creations.
"""


# Function to display a window with the given text
def display_text_window(text: str) -> None:
    # Create the window
    text_window = tk.Toplevel(root, background=bg_color)
    text_window.title("Basic Program Information")

    # Hide the main window and focus on the new window
    text_window.focus()
    text_window.protocol("WM_DELETE_WINDOW", lambda: close_window(text_window))
    text_window.resizable(False, False)
    root.withdraw()

    # Display the text
    text_label = tk.Label(text_window, text=text, background=bg_color)
    text_label.place(x=20, y=20)

    # Add the back button
    back_button = tk.Button(text_window, text="Back", command=lambda: close_window(text_window), background=button_color)
    back_button.place(x=text_label.winfo_reqwidth() * 0.5 + 2, y=text_label.winfo_reqheight() + 40)

    # Center the window
    center_window(text_window, text_label.winfo_reqwidth() + 40, text_label.winfo_reqheight() + 86)


# Function to display the existing partners window
def display_existing_partners_window() -> None:
    # Create the window
    existing_partners_window = tk.Toplevel(root, background=bg_color)
    existing_partners_window.title("Existing Partners")

    # Hide the main window and focus on the existing partners window
    center_window(existing_partners_window, 1012, 412)
    existing_partners_window.focus()
    existing_partners_window.protocol("WM_DELETE_WINDOW", lambda: close_window(existing_partners_window))
    existing_partners_window.resizable(False, False)
    root.withdraw()

    # Function to sort the table by column
    def partner_chart_sort_column(chart: ttk.Treeview, column: str, mode: int) -> None:
        # Different sort modes
        if mode == 0:
            column_values = [(int(chart.set(child, "Number")), child) for child in chart.get_children()]
            column_values.sort()
        else:
            column_values = [(chart.set(child, column).lower(), child) for child in chart.get_children()]
            column_values.sort(reverse=bool(mode - 1))

        # Rearrange items in sorted positions
        for i, (_, k) in enumerate(column_values):
            chart.move(k, '', i)

        # Change sort mode next time
        chart.heading(column, command=lambda: partner_chart_sort_column(chart, column, (mode + 1) % 3))

    # Create a Treeview widget for the chart
    fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=button_color, bordercolor=border_color)
    style.configure("Treeview.Heading", background=button_color, bordercolor=border_color)
    partners_chart = ttk.Treeview(existing_partners_window, columns=fieldnames, show="headings", height=15)

    partners_chart.heading("Number",   text="#")    # Doesn't need sort
    partners_chart.heading("Name",     text="Name",     command=lambda: partner_chart_sort_column(partners_chart, "Name",     1))
    partners_chart.heading("Address",  text="Address",  command=lambda: partner_chart_sort_column(partners_chart, "Address",  1))
    partners_chart.heading("Phone",    text="Phone",    command=lambda: partner_chart_sort_column(partners_chart, "Phone",    1))
    partners_chart.heading("Email",    text="Email",    command=lambda: partner_chart_sort_column(partners_chart, "Email",    1))
    partners_chart.heading("Contact",  text="Contact",  command=lambda: partner_chart_sort_column(partners_chart, "Contact",  1))
    partners_chart.heading("Industry", text="Industry", command=lambda: partner_chart_sort_column(partners_chart, "Industry", 1))

    partners_chart.column("Number",   width=40)
    partners_chart.column("Name",     width=175)
    partners_chart.column("Address",  width=175)
    partners_chart.column("Phone",    width=100)
    partners_chart.column("Email",    width=200)
    partners_chart.column("Contact",  width=120)
    partners_chart.column("Industry", width=160)

    partners_chart.place(x=20, y=20)

    # Function to insert the partner data into the chart
    def update_partner_chart(_) -> None:
        partners_chart.delete(*partners_chart.get_children())
        for partner in partners:
            partners_chart.insert("", tk.END, values=[partner[field] for field in fieldnames])

    # Update the chart and allow it to be updated in the future
    partners_chart.bind("<<Update>>", update_partner_chart)
    partners_chart.event_generate("<<Update>>")

    # Add the back button
    back_button = tk.Button(existing_partners_window, text="Back", command=lambda: close_window(existing_partners_window), background=button_color)
    back_button.place(x=20, y=366)

    # Add the add partner button (functionality is marked later)
    add_partner_button = tk.Button(existing_partners_window, text="Add Partner", command=lambda: display_add_partner_window(existing_partners_window, partners_chart), background=button_color)
    add_partner_button.place(x=173, y=366)

    # Function for the export button
    def export_to_csv() -> None:
        # Ask for filename and location
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        # Cancel if none is given
        if not filename:
            return

        # Open the file in write mode
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write partner header rows
            writer.writerow(fieldnames)

            # Write partner data rows
            for partner in partners:
                writer.writerow([partner[field] for field in fieldnames])

    # Add export button
    export_button = tk.Button(existing_partners_window, text="Export Chart", command=export_to_csv, background=button_color)
    export_button.place(x=76, y=366)

    # Function for deleting the selected partners
    def delete_partners() -> None:
        # Get selected partners
        partner_ids = partners_chart.selection()

        if partner_ids:
            # Delete all of the partners
            def delete() -> None:
                for id in reversed(partner_ids):
                    partners.pop(partners_chart.index(id))

                save_partners()
                partners_chart.event_generate("<<Update>>")

                conformation_window.destroy()

            # Create a window asking the user to confirm if they want to delete
            conformation_window = tk.Toplevel(existing_partners_window, background=bg_color)
            conformation_window.title("Partner Deletion Conformation")
            center_window(conformation_window, 359, 122)
            conformation_window.focus()
            conformation_window.resizable(False, False)

            # Add question text
            question_label = tk.Label(conformation_window, text="Are you sure you want to delete all of the selected partners?\nThis action cannot be undone!")
            question_label.place(x=20, y=20)

            # Add cancel button
            cancel_button = tk.Button(conformation_window, text="Cancel", command=conformation_window.destroy, background=button_color)
            cancel_button.place(x=85.7, y=76)

            # Add confirm button
            confirm_button = tk.Button(conformation_window, text="Confirm", command=delete, background=button_color)
            confirm_button.place(x=208.7, y=76)

    # Add delete partner bButton
    delete_button = tk.Button(existing_partners_window, text="Delete Selected Partners", command=delete_partners, background=button_color)
    delete_button.place(x=267, y=366)

    # Add search field customization
    search_customization_lable = tk.Label(existing_partners_window, text="Search By:", background=bg_color)
    search_customization_lable.place(x=593, y=368)

    search_by = tk.StringVar(value="Name")
    search_by_dropdown = tk.OptionMenu(existing_partners_window, search_by, *fieldnames[1:], command=lambda _: filter_partners())
    search_by_dropdown.config(padx=5, pady=1, width=7, bg=button_color, highlightthickness=0)
    search_by_dropdown.place(x=656, y=369)

    # Add a search bar
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
    with open(file_path, "w", newline="") as csvfile:  # Open in write mode
        fieldnames = ["Number", "Name", "Address", "Phone", "Email", "Contact", "Industry"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Only write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        # Add the number to each partner and write them to the CSV file if missing
        for i, partner in enumerate(partners):
            partner["Number"] = str(i + 1) 
            writer.writerow(partner)


# Function to display the add partner window
def display_add_partner_window(parent_window: tk.Toplevel, partners_chart: ttk.Treeview) -> None:
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

    # Helper function to add hover text to a label
    def add_hover_text(label: tk.Label, text: str) -> None:
        # Create the hover text label
        hover_text = tk.Label(add_partner_window, text=text, font=("Arial", 7), background=hover_tip_color)
        label_pos_x = int(label.place_info()["x"]) - (hover_text.winfo_reqwidth() - label.winfo_reqwidth()) * 0.5
        label_pos_y = int(label.place_info()["y"]) - hover_text.winfo_reqheight()

        # Show it when the label is hovered, and hide it otherwise
        label.bind("<Enter>", lambda _: hover_text.place(x=label_pos_x, y=label_pos_y))
        label.bind("<Leave>", lambda _: hover_text.place_forget())

    # User input labels, entry fields, and hover text

    # Name
    name_label = tk.Label(add_partner_window, text="Name:", background=bg_color)
    name_label.place(x=106.5, y=70)
    name_entry = tk.Entry(add_partner_window, background=text_box_color)
    name_entry.place(x=65, y=91)
    add_hover_text(name_label, "Name must be less than 30 characters long.")

    # Address
    address_label = tk.Label(add_partner_window, text="Address:", background=bg_color)
    address_label.place(x=101.5, y=115)
    address_entry = tk.Entry(add_partner_window, background=text_box_color)
    address_entry.place(x=65, y=136)
    add_hover_text(address_label, "Address must start with a street number.")

    # Phone number
    phone_label = tk.Label(add_partner_window, text="Phone:", background=bg_color)
    phone_label.place(x=105.5, y=160)
    phone_entry = tk.Entry(add_partner_window, background=text_box_color)
    phone_entry.place(x=65, y=181)
    add_hover_text(phone_label, "Phone must be in the format: +12 (345)-678-9876\nCountry code, parenthesis, and dashes are optional.")

    # Email
    email_label = tk.Label(add_partner_window, text="Email:", background=bg_color)
    email_label.place(x=108, y=205)
    email_entry = tk.Entry(add_partner_window, background=text_box_color)
    email_entry.place(x=65, y=226)
    add_hover_text(email_label, "Email must contain an @ and a domain.")

    # Contact information
    contact_label = tk.Label(add_partner_window, text="Contact:", background=bg_color)
    contact_label.place(x=101.5, y=250)
    contact_entry = tk.Entry(add_partner_window, background=text_box_color)
    contact_entry.place(x=65, y=271)
    add_hover_text(contact_label, "Contact can only contain letters and spaces.")

    # Industry
    industry_label = tk.Label(add_partner_window, text="Industry:", background=bg_color)
    industry_label.place(x=101, y=295)
    industry_entry = tk.Entry(add_partner_window, background=text_box_color)
    industry_entry.place(x=65, y=316)
    add_hover_text(industry_label, "Industry can only contain letters and spaces.")

    # Validate the input and then add partner
    def submit_partner(name: str, address: str, phone: str, email: str, contact: str, industry: str) -> None:
        # Helper function to remove given characters from a string
        def remove_chars(string: str, *chars: str):
            for char in chars:
                string = string.replace(char, "")
            return string

        # generate all of the validation requirement bools
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
            # Create new partner dictionary and add it to partners list
            new_partner = {"Number": str(len(partners) + 1), "Name": name, "Address": address, "Phone": phone, "Email": email, "Contact": contact, "Industry": industry}
            partners.append(new_partner)

            # Update partner list
            partners_chart.event_generate("<<Update>>")

            # Save partners to CSV and close page
            save_partners()
            add_partner_window.destroy()

        # If all requirements aren't met, Issue error pop up box
        else:
            submit_error.place(x=submit_error_pos[0], y=submit_error_pos[1])

            root.after(5000, submit_error.place_forget)

    # Add the Submit Button
    submit_button = tk.Button(add_partner_window, text="Add Partner", command=lambda: submit_partner(name_entry.get(), address_entry.get(), phone_entry.get(), email_entry.get(), contact_entry.get(), industry_entry.get()), background=button_color)
    submit_button.place(x=90, y=356)

    # Create, but don't display, the error button
    submit_error = tk.Label(add_partner_window, text="One or more entered fields are not correct\nTo see syntax rules hover over a field label", font=("Arial", 7), background=hover_tip_color)
    submit_error_pos = (int(submit_button.place_info()["x"]) - (submit_error.winfo_reqwidth() - submit_button.winfo_reqwidth()) * 0.5, int(submit_button.place_info()["y"]) - submit_error.winfo_reqheight())

    # Add the Back Button
    back_button = tk.Button(add_partner_window, text="Back", command=add_partner_window.destroy, background=button_color)
    back_button.place(x=109, y=402)


#################
#   Q&A Page    #
#################

def send_question(question):
    unique_id = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S-%f")

    # Email Credentials
    sender_email = "tkmouse9@gmail.com"
    sender_password = "xfrk qutz depl admq"
    receiver_email = "fiducciaalexander@gmail.com"
    message = f"Subject: Help Request #{unique_id}\n\nQuestion from User: {question}"

    # Connect to SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)

def display_qna_window(): 
    # New Window for Questions
    qna_window = tk.Toplevel(root)
    qna_window.title("Help Request")
    qna_window.configure(background=bg_color)
    center_window(qna_window, 500, 375)
    qna_window.resizable(False, False)

    # Add the question entry box and submit button
    question_label = tk.Label(qna_window, text="Send a Question or Suggestion to Our Developers\nInclude your email at the top of the message so we can get back to you", padx=100, pady=50, background=bg_color, font='Helvetica 10 bold')
    question_label.pack()

    question_box = tk.Text(qna_window, width=50, height=5, background=button_color)
    question_box.pack()

    def submit_question():
        question_text = question_box.get("1.0", "end").strip()

        # Check if question box is empty
        if question_text:
            send_question(question_text)
            question_box.delete("1.0", tk.END)  # Clear question box after submission
            success_label = tk.Label(qna_window, text="Question submitted successfully!", fg="green", background=button_color, font ='Helvetica 10 bold')
            success_label.pack(pady=30)
            root.after(5000, success_label.destroy)

        # Display the error label
        else:
            error_label = tk.Label(qna_window, text="Please enter your question.", fg="red", background=button_color, font='Helvetica 10 bold')
            error_label.pack(pady=30)
            root.after(5000, error_label.destroy)

    # Add the submit button
    submit_button = tk.Button(qna_window, text="Submit Question", command=submit_question, background=button_color)
    submit_button.pack(pady=20)

    # Add the Back Button
    back_button = tk.Button(qna_window, text="Back", command=qna_window.destroy, background=button_color)
    back_button.place(x=233, y=275)


# Helper function to center a window based on the screen size
def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    window.geometry('{}x{}+{}+{}'.format(width, height, int(0.5 * (root.winfo_screenwidth() - width)), int(0.5 * (root.winfo_screenheight() - height))))


# Helper function to close the window and reopen the main window
def close_window(window: tk.Toplevel) -> None:
    root.deiconify()
    window.destroy()


# Data for the chart
partners = []

# Read CSV file and populate the partners list
with open("partners.csv") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        partners.append(row)


#################
#  Main Window  #
#################

# Colors used for everything
bg_color = "#4169e1"
button_color = "#b3c3f3"
hover_tip_color = "#6787e7"
text_box_color = "#b3c3f3"
border_color = "#3454b4"

# Create the main window
root = tk.Tk()
root.title("HRHS CTE Partners")
root.configure(background=bg_color)
center_window(root, 454, 316)
root.resizable(False, False)

# Add school logo
canvas = tk.Canvas(root, width=100, height=100, highlightthickness=0, background=bg_color)
canvas.place(x=20, y=20)

image = Image.open("HRHS_Logo.png").resize((100, 100))
photo_image = ImageTk.PhotoImage(image, width=100, height=100)
canvas.create_image(50, 50, image=photo_image)

# Add title
title_label = tk.Label(root, text="HRHS CTE Partners", font=("Sylfaen", 24, "bold"), fg="blue", background=bg_color)
title_label.place(x=140, y=20)

# Add buttons
readme_button = tk.Button(root, text="ReadMe", command=lambda: display_text_window(program_info[1:-1]), background=button_color)
readme_button.place(x=20, y=140)

partners_button = tk.Button(root, text="Existing Partners", command=lambda: display_existing_partners_window(), background=button_color)
partners_button.place(x=20, y=186)

documentation_button = tk.Button(root, text="Documentation", command=lambda: display_text_window(library_documentation[1:-1]), background=button_color)
documentation_button.place(x=20, y=232)

help_button = tk.Button(root, text="?", command=display_qna_window, background=button_color, font='Helvetica 9 bold')
help_button.place(x=90, y=140)

# Add credits
credits_label = tk.Label(root, text="Program Designed in Python 3.12 for FBLA by Alexander Fiduccia and Joe Hopkins", font=("Arial", 7), background=bg_color)
credits_label.place(x=48.5, y=278)

# Start the GUI event loop
root.mainloop()
