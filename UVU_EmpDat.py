"""
T1-SPR4-CS2450-601
Developed by Team 1 in CS 2450-601, Spring 2022.

UVU Employee Database
Developed by Innovative EmpTrak
See "readme.txt" for a quickstart guide.

This product delivers an Employee Database with a Graphical User Interface
for Utah Valley University. Employee data can be viewed and edited by
administrators, and employees can view their own data as well. Reports of
employee information can also be generated.

Developed with:
Python version 3.7.2
Tkinter version 8.6
"""

# TODO: FIXME:
# Need to go over my notes at the bottom with Abbie, Tristan, and the
#   team.

import csv
from csv import reader
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askokcancel, WARNING
import os  # use if helpful to delete files. Can just overwrite?
import os.path
from functools import partial


class Employee():
    """
    Main employee class

    Initialize it with Name SNN Phone email and its classification, after
    that use the three functions set_address, set_pay and set_job to fill
    in the rest of the info

    The reason it is split so weird is because you might not necessarily
    want to put in 100% of someones info at once so its split into three
    categories
    """

    def __init__(self, id, name, birth_date, SSN, phone, email, classification):
        self.id = id
        if self.id is not None:
            self.id = int(self.id)
        self.name = name
        if isinstance(self.name, str):
            if ' ' in name:
                split_name = name.split(" ")
                first_name = split_name[0]
                last_name = split_name[-1]
            else:
                first_name = name
                last_name = None
        else:
            first_name = None
            last_name = None
        
        self.first_name = first_name
        self.last_name = last_name
        self.address = None
        self.city = None
        self.state = None
        self.zip = None
        self.classification = classification
        self.pay_method = None
        self.salary = None
        self.hourly = None
        self.commission = None
        self.route = None
        self.account = None
        self.birth_date = birth_date
        self.ssn = SSN
        self.phone = phone
        self.email = email
        self.start_date = None
        self.end_date = None
        self.title = None
        self.dept = None
        self.password = None

    def set_address(self, address, city, state, zip):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

    def set_pay(self, method, salary, hourly, commission, route):
        self.pay_method = method
        self.salary = salary
        self.hourly = hourly
        self.commission = commission
        self.route = route

    def set_job(self, start_date, title, dept):
        self.start_date = start_date
        self.title = title
        self.dept = dept

    def terminate_employee(self, end_date):
        self.end_date = end_date

    def populate_from_row(self, row):
        self.id = int(row["ID"])
        self.name = row["Name"]
        name = self.name.split(" ")
        self.first_name = name[0]
        self.last_name = name[-1]
        self.classification = row["Classification"]
        self.ssn = row["Social Security Number"]
        self.phone = row["Phone Number"]
        self.email = row["Email"]
        self.address = row["Address"]
        self.city = row["City"]
        self.state = row["State"]
        self.zip = row["Zip"]
        self.pay_method = row["PayMethod"]
        self.salary = row["Salary"]
        self.hourly = row["Hourly"]
        self.commission = row["Commission"]
        self.route = row["Route"]
        self.account = row["Account"]
        self.birth_date = row["Date of Birth"]
        self.start_date = row["Start Date"]
        self.end_date = row["End Date"]
        self.title = row["Title"]
        self.dept = row["Department"]
        self.password = row["Password"]

    def __str__(self):
        return self.name


class EmployeeDB:
    """
    Database class:

    Creates a csv file with the correct format if one does not already
    exist in the directory.
    Keeps a list of employees within the class and pulls from the csv file

    update_emp_list pulls data from the csv to the list

    TODO:: updateCSV pulls data from the list and fills out the csv file
    """

    def __init__(self):
        # create employee csv file if it does not exist
        if os.path.exists("employees.csv") != True:
            with open("employees.csv", "x") as DB:
                writer = csv.writer(DB)
                writer.writerow(
                    "ID,Name,Address,City,State,Zip,Classification,\
                    PayMethod,Salary,Hourly,Commission,Route,Account,\
                    Social Security Number,Phone Number,Email,\
                    Start Date,End Date,Title,Department,\
                    Password".split(
                        ','))
                self.db = DB
        else:
            self.db = open("employees.csv")
        self.emp_list = []
        self.update_emp_list()

    def update_emp_list(self):
        reader = csv.DictReader(self.db)
        for row in reader:
            emp = Employee(None, None, None, None, None, None, None)
            emp.populate_from_row(row)
            self.emp_list.append(emp)
    # TODO
    # def updateCSV

# Define global EmployeeDB object:
# EmployeeDatabase object should be global, so all functions can access
#   it?
uvuEmpDat = EmployeeDB()


# emp_list should be a list of Employee objects.
def find_employee_by_id(employee_id, emp_list):
    """Finds an employee with the given ID in the given employee list, and
    returns it. Returns None if no employee has the given ID.
    """
    for employee in emp_list:
        if employee.id == employee_id:
            return employee
    return None


# Need to generate the login screen.
def login_screen(): # May need to do at the global level, not sure.
    """Generates a functional login screen for the UVU Employee Database.
    """
    # Initialize the tkinter window for the login screen, and it's size
    #   and geometry.
    # Initialize the "Username" and "Password" labels and fields.
    # Initialize the "Login" button, to call the validate_login function
    #   with the username and password from the Username and Password
    #   fields.
    # If login was valid:
        # If employee.permission_level is "admin":
            # call "open_admin()"
        # Else if employee.permission_level is "employee" (or anything
        #   else):
            # call "open_employee(employee, 'employee')"
    # Else: (if not valid)
        # Show the login error (have a simple tkinter window for this, or
        #   a printed label?)
    
    # Run the mainloop to open the login window.


def validate_login(username, password): # working as designed.
    """Checks whether there is a user with the given username, and whether
    the given password matches that user's password.
    
    Output: Two bool values, the first saying whether the username was
            valid, the second saying whether the password was valid.
    """
    valid_username = False
    valid_password = False
    username = int(username)
    for employee in uvuEmpDat.emp_list:
        if employee.id == username:
            valid_username = True
            if employee.password == password:
                valid_password = True
    return valid_username, valid_password

    
# Need to fill the employee list.
    
def open_admin():
    """Generates a GUI window of the admin view, a list of all employees,
    and generates all of its functionality, so that you can click on
    employees to view their data, and can generate a report of all
    employees.
    """
    #Admin Window
    admin_window = Toplevel(login_window)
    #Title of Admin Window
    admin_window.title("UVU Employee Database")
    
    #Style - default coloring
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="whitesmoke", \
        foreground="black", rowheight=35, fieldbackground="whitesmoke")

    style.map("Treeview", background=[("selected", "olivedrab")])
    
    #File and Help Menu
    # FIXME: create file and help menu bar.
    
    #Create Employee Tree Frame
    emp_frame = Frame(admin_window)
    
    def tree_column_sort(tree, the_column, other_way):
        #Get the values to sort
        information = [(tree.set(k, the_column), k) for k in tree.get_children('')]
        #Rearrange to sorted positions
        information.sort(reverse=other_way)
        for index, data in enumerate(information):
            tree.move(data[1], '', index)
        #Reverse the sort on next click
        tree.heading(the_column, command=lambda c=columns_list[the_column]: tree_column_sort(tree, the_column, not other_way))
    
    #Define columns
    columns_list = ("employee_id", "first_name", "last_name", \
        "social_security_number", "phone_number", "email", "start_date", \
            "end_date", "classification", "title", "department")

    employee_list = ttk.Treeview(admin_window, columns=columns_list, \
        show="headings")

    #Define headings
    employee_list.heading("employee_id", text="Employee ID", command=lambda c=columns_list[0] : tree_column_sort(employee_list, 0, False))
    employee_list.heading("first_name", text="First Name", command=lambda c=columns_list[1] : tree_column_sort(employee_list, 1, False))
    employee_list.heading("last_name", text="Last Name", command=lambda c=columns_list[2] : tree_column_sort(employee_list, 2, False))
    employee_list.heading("social_security_number", \
        text="Social Security Number", command=lambda c=columns_list[3] : tree_column_sort(employee_list, 3, False))

    employee_list.heading("phone_number", text="Phone Number", command=lambda c=columns_list[4] : tree_column_sort(employee_list, 4, False))
    employee_list.heading("email", text="Email", command=lambda c=columns_list[5] : tree_column_sort(employee_list, 5, False))
    employee_list.heading("start_date", text="Starting Date", command=lambda c=columns_list[6] : tree_column_sort(employee_list, 6, False))
    employee_list.heading("end_date", text="Ending Date", command=lambda c=columns_list[7] : tree_column_sort(employee_list, 7, False))
    employee_list.heading("classification", text="Classification", command=lambda c=columns_list[8] : tree_column_sort(employee_list, 8, False))
    employee_list.heading("title", text="Title", command=lambda c=columns_list[9] : tree_column_sort(employee_list, 9, False))
    employee_list.heading("department", text="Department", command=lambda c=columns_list[10] : tree_column_sort(employee_list, 10, False))

    #Style - striped rows
    employee_list.tag_configure("evenrows", background = "honeydew")
    employee_list.tag_configure("oddrows", background = "white")

    # Iterate through all employees to list them out.
    global count
    count = 0
    for emp in uvuEmpDat.emp_list:
        if count % 2 == 0:
            employee_list.insert('', END, values=(emp.id, emp.first_name,\
                        emp.last_name, emp.ssn, emp.phone, emp.email, \
                        emp.start_date, emp.end_date, \
                        classification_translate(emp.classification), \
                        emp.title, emp.dept), tags=("evenrows",))
        else:
            employee_list.insert('', END, values=(emp.id, emp.first_name,\
                        emp.last_name, emp.ssn, emp.phone, emp.email, \
                        emp.start_date, emp.end_date, \
                        classification_translate(emp.classification), \
                        emp.title, emp.dept), tags=("oddrows",))
        count+=1
    
    def employee_selected(event):
        """Brings up an employee's information in a separate GUI window.
        Intended to be called with a double-click event handler, so that
        an employee's info shows up when you click on them.
        """
        #Bring up employee information after double-click
        for selected_emp_idx in employee_list.selection():
            emp_data = employee_list.item(selected_emp_idx)
            emp_id = emp_data["values"][0]
            emp = find_employee_by_id(emp_id, uvuEmpDat.emp_list)
            open_employee(emp, "admin")
            
    #Double-Click to bring up employee information
    employee_list.bind("<Double 1>", employee_selected)
    employee_list.grid(row=1, column=0, sticky="nsew")
    
    #Scrollbar
    scrollbar = ttk.Scrollbar(admin_window, orient=VERTICAL, \
                        command=employee_list.yview)
                        
    employee_list.config(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky="ns")
    
    #Run the window
    admin_window.mainloop()

# FIXME: need to add "Report" button and functionality.
# initialize event listeners for clicking the "report/issue-payment"
#   button:
    # call prompt_report_all_employees().

def open_admin_view():
    #This function is so the warning is shown before admin view is open
    under_construction()
    open_admin()
    



# Need to fill the fields for a single employee's data.
def open_employee(employee, permission_level):
    """Generates a GUI window populated with the data of the given
    employee. Also creates buttons to allow for editing an employee's data
    and printing a report for that employee. Will have a back button as
    well if permission_level is "admin".
    Input: Employee object, string.
    """
    #Under development
    under_construction()
    #Employee Window
    employee_window = Toplevel(login_window)
    
    #Title of Login Window
    employee_window.title("UVU Employee Database")
    
    # Fonts
    title_font = "Arial 12 bold underline"
    label_font = "Arial 12"

    #Personal Information
    personal_info_title = Label(employee_window, \
                text="Personal Information").grid(row=0, column=0, \
                columnspan=3, padx=10, pady=10)
    #First Name
    first_name_title = Label(employee_window, text="First Name")\
        .grid(row=1, column=0, padx=10, pady=15)
    first_name_label = Label(employee_window, text=employee.first_name)\
        .grid(row=2, column=0, padx=10, pady=10)
    #Last Name
    last_name_title = Label(employee_window, text="Last Name").grid(row=1,\
        column=1, padx=10, pady=15)
    last_name_label = Label(employee_window, text=employee.last_name)\
        .grid(row=2, column=1, padx=10, pady=15)
    #Social Security Number
    sss_title = Label(employee_window, text="Social Security Number")\
        .grid(row=1, column=2, padx=10, pady=15)
    sss_label = Label(employee_window, text=employee.ssn).grid(row=2, \
        column=2, padx=10, pady=15)
    #Phone Number
    phone_number_title = Label(employee_window, text="Phone Number")\
        .grid(row=3, column=0, padx=10, pady=10)
    phone_number_label = Label(employee_window, text=employee.phone)\
        .grid(row=4, column=0, padx=10, pady=10)     
    #Email
    email_title = Label(employee_window, text="Email").grid(row=3, \
        column=2, padx=10, pady=10)
    email_label = Label(employee_window, text=employee.email).grid(row=4,\
        column=2, padx=10, pady=10)
    #Address
    address_title = Label(employee_window, text="Address").grid(row=5, \
        columnspan=3, padx=10, pady=10)
    address_label = Label(employee_window, text=employee.address)\
        .grid(row=6, columnspan=3, padx=10, pady=10)
    #City
    city_title = Label(employee_window, text="City").grid(row=7, \
        column=0, padx=10, pady=10)
    city_label = Label(employee_window, text=employee.city).grid(row=8, \
        column=0, padx=10, pady=10)
    #State Initials
    state_title = Label(employee_window, text="State").grid(row=7, \
        column=1, padx=10, pady=10)
    state_label = Label(employee_window, text=employee.state).grid(row=8,\
        column=1, padx=10, pady=10)
    #Zip Code
    zip_code_title = Label(employee_window, text="Zip Code").grid(row=7, \
        column=2, padx=10, pady=10)
    zip_code_label = Label(employee_window, text=employee.zip)\
        .grid(row=8, column=2, padx=10, pady=10)
    #Date of Birth
    birth_date_title = Label(employee_window, text="Date of Birth")\
        .grid(row=9, column=0, padx=10, pady=10)
    birth_date_label = Label(employee_window, text=employee.birth_date)\
        .grid(row=10, column=0, padx=10, pady=10)
    #Password
    password_title = Label(employee_window, text="Password").grid(row=9, \
        column=1, padx=10, pady=10)
    password_label = Label(employee_window, text=employee.password)\
        .grid(row=10, column=1, padx=10, pady=10)

    #Employee Information
    employee_info_title = Label(employee_window, \
        text="Employee Information").grid(row=0, column=3, columnspan=3, \
        padx=10, pady=10)
    #Employee ID number
    emp_id_title = Label(employee_window, text="Employee ID").grid(row=1,\
         column=3, padx=10, pady=10)
    emp_id_label = Label(employee_window, text=employee.id).grid(row=2, \
        column=3, padx=10, pady=10)     
    #Job title
    job_title_title = Label(employee_window, text="Job Title")\
        .grid(row=3, column=3, padx=10, pady=10)
    job_title_label = Label(employee_window, text=employee.title)\
        .grid(row=4, column=3, padx=10, pady=10)     
    #Department
    department_title = Label(employee_window, text="Department")\
        .grid(row=3, column=4, padx=10, pady=10)
    department_label = Label(employee_window, text=employee.dept)\
        .grid(row=4, column=4, padx=10, pady=10)     
    #Start Date
    start_date_title = Label(employee_window, text="Start Date")\
        .grid(row=5, column=3, padx=10, pady=10)
    start_date_label = Label(employee_window, text=employee.start_date)\
        .grid(row=6, column=3, padx=10, pady=10)     
    #End Date
    end_date_title = Label(employee_window, text="End Date").grid(row=5, \
        column=5, padx=10, pady=10)
    end_date_label = Label(employee_window, text=employee.end_date)\
        .grid(row=6, column=5, padx=10, pady=10)     
    #Account Number
    account_title = Label(employee_window, text="Account Number")\
        .grid(row=7, column=3, padx=10, pady=10)
    # FIXME: Have the account_label connect with the employee's payment
    #   method. Only shows account if they are paid by direct method.
    account_label = Label(employee_window, text=employee.account)\
        .grid(row=8, column=3, padx=10, pady=10)     
    #Routing Number
    routing_title = Label(employee_window, text="Routing Number")\
        .grid(row=7, column=4, padx=10, pady=10)
    # FIXME: Have the routing_label connect with the employee's payment
    #   method. Only shows routing num if they are paid by direct method.
    routing_label = Label(employee_window, text=employee.route)\
        .grid(row=8, column=4, padx=10, pady=10)     
    #Payment Method
    payment_title = Label(employee_window, text="Payment Method")\
        .grid(row=7, column=5, padx=10, pady=10)
    # FIXME: Give PayMethod class a "print()" method that prints "Direct
    #   Deposit" or "Mail", whichever child class they have.
    payment_label = Label(employee_window, text=employee.pay_method)\
        .grid(row=8, column=5, padx=10, pady=10)
    #Classification
    classification_title = Label(employee_window, text="Classification")\
        .grid(row=9, column=3, padx=10, pady=10)
    classification_label = Label(employee_window, \
        text=classification_translate(employee.classification))\
        .grid(row=10, column=3, padx=10, pady=10)
    #Hourly
    # FIXME: We can change this in the future to only show the type of pay
    #   they get, based on their classification. Define employee.classification.pay_amount() method.
    hourly_title = Label(employee_window, text="Hourly Rate")\
        .grid(row=11, column=3, padx=10, pady=10)
    hourly_label = Label(employee_window, text=employee.hourly)\
        .grid(row=12, column=3, padx=10, pady=10) 
    #Salary
    salary_title = Label(employee_window, text="Salary Amount")\
        .grid(row=11, column=4, padx=10, pady=10)
    salary_label = Label(employee_window, text=employee.salary)\
        .grid(row=12, column=4, padx=10, pady=10)     
    #Commission
    commission_title = Label(employee_window, text="Commission")\
        .grid(row=11, column=5, padx=10, pady=10)
    commission_label = Label(employee_window, text=employee.commission)\
        .grid(row=12, column=5, padx=10, pady=10)

    # Buttons
    back_button = Button(employee_window, text="Back", \
        command=partial(exit_window, employee_window)).grid(row=13, \
        column=3, padx=10, pady=10)
    edit_button = Button(employee_window, text="Edit", \
        command=partial(edit_employee, "admin")).grid(row=13, column=4, \
        padx=10, pady=10)
    pay_stub_button = Button(employee_window, text="Get Pay Stub", \
        command=partial(generate_pay_stub, employee)).grid(row=13, \
        column=5, padx=10, pady=10)

    # FIXME: add "Edit" button and functionality, and "Pay Stub" and
    #   "Back" buttons and functionalities.

    # bind event listener to the "Edit" button:
        # call the function to edit an individual employee, passing user
        #   permission level in.
    # bind event listener to the "Pay stub" button, tied to the function
    #   to get paystub(s).
    # bind event listener to "back" button, IF the user is admin (can go
    #   back to admin view).

    # run the mainloop to open this window if a regular employee is using
    #   it?


def prompt_report_all_employees():
    """Generates a GUI prompt asking whether the user wants to include
    archived employees in the report, and generates the proper report
    based on the user's response. Also allows user to click a cancel
    button to close the window without generating a report.
    """
    # If user clicks "Yes", calls generate_report_all_employees(True)
    # If user clicks "No", calls generate_report_all_employees(False)
    # If user clicks the "x", the window will go away. Or initialize a
    #   "Cancel" button instead, if needed or helpful.


# Should this report be a payment report, just a general info report, or
#   both?
def generate_report_all_employees(include_archived):
    """Generates a report of all employees in the database, in the form of
    a text document titled uvu_empDat_report.txt? The report will include
    the info of archived employees if include_archived is True, and will
    not if it is False.
    """
    # If include_archived, then emp_list will be all employees
    if include_archived:
    #   (from EmployeeDatabase.archived and EmployeeDatabase.database).
        emp_list = uvuEmpDat.emp_list + uvuEmpDat.archived
    else: # Otherwise emp_list will be all non-archived employees (from
    #   EmployeeDatabase.database).
        emp_list = uvuEmpDat.emp_list

    # os.remove("report.csv")    # Delete the previous "report.csv" file 
    #   (if necessary. Will writing over it be just as good?).

    # Initialize the tkinter generate_report_all_employees window,
    #   configuring formatting and colors, with columns for all employee
    #   data members.
    with open("report.csv", "w") as report:
        for employee in emp_list:
            # Write a line to "report.csv" that includes all of the employee's
            #   data members, separated by commas.
            report.write(f"{employee.id},{employee.first_name},\
                            {employee.last_name},{employee.address},\
                            {employee.city},{employee.state},\
                            {employee.zip},{employee.phone},\
                            {employee.email},\
                            {employee.classification},\
                            {employee.paytype},\
                            {employee.date_of_birth},\
                            {employee.social_security_num},\
                            {employee.start_date},{employee.end_date},\
                            {employee.permission_level},\
                            {employee.password},{employee.title},\
                            {employee.department}\n")            
            # Write the next line in "report.csv" by calling
            #   employee.issue_payment() (and save amount and date they were
            #   paid into variables).
            report.write(f"\t{employee.issue_payment()}\n")
            # Fill tkinter screen (Treeview?) with the employee's data members
            # Fill tkinter screen in next row (formatted nicely) with the info
            #   about what that employee was payed and when, from variables.

    os.remove("timecards.csv")
    os.remove("receipts.csv")  # Delete "timecards.csv" and "receipts.csv".

    # Print message in GUI screen saying that report can also be viewed
    #   and shared from "report.csv".

    # Bind event listener to "Back" button to exit the report's window.


# Need to generate report of an individual employee's data and/or PAYMENT
#   INFO AND PAYMENT TYPE.
    # Is it different than a paystub, or should this be the same?


# Should this just be their pay for the previous two weeks, or pay period?
#   Or all of their pay recorded, based on two-week periods?
def generate_pay_stub(employee):
    """Generates a pay stub/report for the given employee, with the name:
    {employee_full_name}_pay_stub.txt.
    """
    under_construction()
    # Show the pay stub, and allow the option to export it to CSV.
    # To show it, show the amount they were paid, based on their salary,
    #   and their other payment options
    # Initialize variable called pay to 0.
    # Initialize variable called pay_date to "".
    # Initialize variable called pay_num (stores hours or commissions).
    # Initialize found variable to False.
    # Initialize line_count to 0.
    # For each line in "reports.csv":
        # line_count += 1.
        # if line_count is even:
            # continue (skip iteration).
        # parse line items separated by comma into a list.
        # if first item in line = employee.emp_id:
            # found = True.
            # get the next_line from "reports.csv"
            # parse next_line items separated by comma into a list.
            # from next_line list, store their pay into pay variable.
            # from next_line list, store their pay date into pay_date
            #   variable.
            # from next_line list, store hour or commission number based
            #   on index into pay_num variable. (Will be invalid for
            #   salaried employees, that's okay.)
            # break
    # If found:
        # Call pay_stub_screen(employee) to generate GUI screen and finish
        #   report.
    # Else:
        # Show an error pop-up message, that the employee was not payed in
        #   the last pay period (may happen before any "report.csv" file
        #   is generated).


    def pay_stub_screen(employee): # If we don't use this function, bypass
        # straight to export_pay_stub_csv, and just generate a stub file.
        """Initialize a GUI screen that shows the text for how much the
        employee was payed on their last pay date, and any other
        applicable pay stub info, like hours worked or commissions made.
        Also allows the user the option to export the pay stub to .csv
        format.
        """
        # Initialize a variable called classification to be the employee's
        #   classification type (employee.classification.print()).
        # Initialize a variable called pay_stub_message to be the text
        #   that will be printed on the pay stub (start as empty string).
        # Initialize a GUI screen to show the pay stub, along with the
        #   formatting and colors that will be used.
        # if classification = "hourly":
            # Create pay_stub_message using pay, pay_date, and pay_num,
            #   and pay_num will represent the number of hours worked.
            #   Make message applicable by stating pay, hours, and date
            #   received.
        # if classification = "salary":
            # Create pay_stub_message using pay and pay_date. Make message
            #   applicable by stating pay and date received.
        # if classification = "commissioned":
            # Create pay_stub_message using pay, pay_date, and pay_num,
            #   and pay_num will represent the number of commissions made.
            #   Make message applicable by stating pay, number of
            #   commissions, and date received.

        # Add pay_stub_message to the GUI screen.

        # Initalize an "Export to .csv" button on the screen.
        # Bind event listener to "Export to .csv" button that calls
        #   "export_pay_stub_csv(pay_stub_message)"


    def export_pay_stub_csv(pay_stub_message):
        """Exports the pay stub to a .csv file, named with the employee's
        name and saved in the same directory as this program.
        
        Input: the text that should be printed on the pay stub.
        Output: writes to a pay stub file, named based on the employee's
                name.
        """
        # Should open a file named
        #   f'{employee.first_name}_{employee.last_name}_pay_stub.csv'.
            # Write pay_stub_message to the file.
        # Close the file.


def edit_employee(permission_level):
    """Allows you to edit and save an employee's information. If
    permission level is "admin", allows user to edit all information. If
    permission level is "employee", allows user to edit only their
    username, physical address, phone number, email address, and payment
    type.
    """
    under_construction()
    # Replace the "Edit" button with a "Save" button.
    # If permission_level is admin:    
        # Change admin-level data labels to fields.
        # Bind event listener to save button. When clicked:
            # If changes made: (call employee_data_changed(employee))
                # save_employee_changes(employee)
            # Else if no changes made, do nothing.
        # change edit fields back to labels, and "Save" button back to
        #   "Edit" (no more editing until you re-click edit)

    # Else if permission level is employee (or anything else):
        # Change normal employee-level data labels to fields.
        # Bind event listener to save button. When clicked:
            # If changes made: (call employee_data_changed(employee))
                # save_employee_changes(employee)
            # Else if no changes made, do nothing.
        # change edit fields back to labels, and "Save" button back to
        #   "Edit" (no more editing until you re-click edit)

    # Bind event listener to cancel button. When clicked, exits edit mode:
        # if employee data changed: (call employee_data_changed(employee))
            # populate employee fields to match employee object data.
        # change edit fields back to labels, and "Save" button back to
        #   "Edit" (no more editing until you re-click edit)


    def save_employee_changes(employee): # (nested in edit_employee.)
        """Saves any changes made to employee data during editing. Updates
        the employee's data within the database.
        """
        # if permission_level is "admin":
            # calls employee.update_emp_info(with all employee data)
        # else if permission_level is "employee" (or anything else?):
            # calls employee.update_own_info(with data that normal
            #   employees can edit only, from GUI fields)

    # Need a function to handle checking if an employee's data has changed
    #   (saving it if so?).
    def employee_data_changed(employee): # (nested in edit_employee.)
        """Checks the employee fields that are editable, and sees if they
        match the previous data of the employee. If they match, False is
        returned. If they don't match, True is returned (employee data was
        changed).
        """
        # If permission_level is "admin":
            # For each data field that admin can edit:
                # Compare that data field to the matching employee data
                #   field.
                    # If it doesn't match:
                        # return True
        # Else if permission_level is "employee" (or anything else):
            # For each data field that employee can edit:
                # Compare that data field to the matching employee data
                #   field.
                    # If it doesn't match:
                        # return True
        # return False


# Need to archive employee when admin clicks "archive".
def archive_employee(employee):
    """Archives the employee that is referenced in the parameters.
    """
    # Update the employee with all of the employee's current info, and
    #   also an end_date of today's date (datetime object). (or set an
    #   archived data member, etc.) Call employee.update_emp_info(with
    #                                       data, including end_date)
    # Remove employee from the EmployeeDatabase.database, and into the
    #   EmployeeDatabase.archived list.


def under_construction():
    """Displays a warning message that the section is still under
    development.
    """
    showinfo("Warning", "This function is still under development.", \
        icon=WARNING)
    
    
def button_close_warning():
    """Brings up a confirmation window, asking if you want to quit. If yes
    the program exits.
    """
    #Prompt warning about to close program
    answer = askokcancel("Confirmation", "Are you sure you want to quit?", \
        icon=WARNING)
    if answer:
        login_window.destroy()


def exit_window(window):
    """A function to close the given tkinter window, for back buttons.
    """
    window.destroy()



def classification_translate(num):
    if int(num) == 1:
        classification_name = "Hourly"
    elif int(num) == 2:
        classification_name = "Salaried"
    else:
        classification_name = "Commissioned"
    return classification_name


#Login Window functionality. Global so that all functions can access it.

login_window = Tk()
#Size of Login Window
login_window.geometry("515x360")
#Title of Login Window
login_window.title("UVU Employee Database")
#Login Window Name
login_window_label = Label(login_window, text="Login").grid(row=1, \
    columnspan=3, padx=50, pady=50)

#Username Text
username_label = Label(login_window, text="User Name").grid(row=2, \
    column=1, padx=25, pady=5)
#Username Textbox
username = StringVar()
username_entry = Entry(login_window, textvariable=username)\
    .grid(row=2, column=2, padx=50, pady=5)  

#Password Text
password_label = Label(login_window,text="Password").grid(row=3, \
    column=1, padx=25, pady=5)
#Password Textbox
password = StringVar()
password_entry = Entry(login_window, textvariable=password, show='*')\
    .grid(row=3, column=2, padx=5, pady=5)  

#Login Button
login_button = Button(login_window, text="Login", \
    command=open_admin_view).grid(row=4, column=2, padx=25, pady=25)

#Close Button
exit_button = Button(login_window, text="Close", \
    command=button_close_warning).grid(row=5, column = 4, padx=5, pady=5)


#Delete/comment out this next line when login is implemented
under_construction()

#next line is for employee testing
# emp_file.close()

def main():   
    """Starts up the entire application, starting with the login screen.
    """
    # Run the login_screen() function, and (/or?) any mainloops required!
    # Testing:
    # for emp in uvuEmpDat.emp_list:
    #     print(f'{emp.name}\'s ID is {emp.id}')


    #Run the window; real code:
    login_window.mainloop()
    

if __name__ == "__main__":
    main()


# Extra notes and questions:

    # Questions and comments for everyone:
        # NEED A WAY TO INTEGRATE THE PAYMENT FUNCTIONS WITH THE GUI!!!
        # Need a way to upload employee timecards and receipts into the DB
        #   using the GUI.
            # Can only admins do that? Can employees themselves?
        # Whether they have timecards or receipts depends on their
        #   classification!

        # Should reports all be payment reports?
        # Should they include all current timecards, etc., for employees,
        #   and then wipe them? Or should it keep a history of all
        #   payments made to those employees? If so, employee timecards/
        #   receipt files should be added to over time, somewhat like the
        #   employee db file.
        
        # What should be shown when archived employees are included in the
        #   report? Should their payment info from old paychecks be
        #   included?

        # Need to brainstorm what each of the reports should include, and
        #   then write them to do so. (We should have access to all of the
        #   data we need; my real question is simply what the reports
        #   should be.) What do my pay stubs look like?

        # Should the pay stub be the same as the report printed when an
        #   employer looks at an employee's records?

        # (Need to make sure there can't be more than one user with the
        #   same username, when creating new user, to keep bug-free.)

        # Double-check: which data members do we want to show with an
        #   individual employee's data? Different when admin views?

        # Which data should employees be able to edit? Which should admins
        #   be able to edit?

        # Instead of uploading files, does it seem reasonable to say that
        #   we can use files that are in the current directory, and
        #   possibly clear them whenever we "issue payment"/generate the
        #   general report? Just find the files based on their names?

        # Do we need a way to drag and drop/upload files, or can we just
        #   read the files named timecards.csv, receipts.csv, etc., and
        #   assume they'll have the right data? I'm going to assume we can
        #   just use files with those names, and assume they have the
        #   correct data.

        # WE NEED TO VALIDATE DATA PUT INTO THE GUI, TO MAKE SURE IT'S ALL
        #   IN THE RIGHT TYPES.


    # Questions and comments for Tristan:

        # Let Tristan know, we need to write to the file when an employee
        #   is archived, so that when the program restarts, it will
        #   remember that the employee is archived.

        # Do we want an "archived" data member, or should we just read/
        #   check whether they have an end_date? (If so, end date must be
        #   after start date, otherwise they've returned.) Or do we want a
        #   list item that is not a data member, but tells the DB which
        #   list to put that employee in? (Says, ",archived,", or is empty
        #   (",,"), for example?)

        # See if Tristan can add a "print()" method to each of the payment
        #   method and classification classes, so that their types can be
        #   printed easily on the GUI. (e.g., Hourly class prints
        #   "hourly".)

        # Would it work to have "hourly.issue_payment()" also print how
        #   many hours they worked, and "commissioned.issue_payment()"
        #   also print how many commissions they made? (Sum up the numbers
        #   from the timecards/receipts?)


    # Questions and comments for Abbie:

        # Have all of the GUI stuff/listeners put into a function that is
        #   called in main?
        
        # We may need to make a function (or see if Abbie can?) to
        #   validate whether GUI field info still matches employee
        #   object's info, and returns boolean, True if matches. Does that
        #   seem doable with the info users type into the GUI?

        # I have a suggestion for the single employee GUI page:
            # I think it would look nice to have all of the labels in one
            #   column on the left, with all of the data in one column on
            #   the right, with both columns aligned (left col. right-
            #   aligned, right col. left-aligned?).
            # We could still keep personal and employment info separate,
            #   though, if we want. Two separated columns, each with a 
            #   column of labels and data?
            # Also, could style fonts, and buttons, etc., maybe just a
            #   little bit.
