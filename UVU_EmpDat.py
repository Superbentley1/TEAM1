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
from msilib.schema import Class
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo, askokcancel, askyesno, WARNING
import os  # use if helpful to delete files. Can just overwrite?
import os.path
from functools import partial


class Classification():
    """Used for tracking the payment type and rate of an employee, and
    calculating how much they will be paid. An abstract class.
    """
    def __init__(self):
        """Initialize the abstract class.
        """
        pass

    def calculate_pay(self):
        """Calculates the employee's pay. Implemented differently in child
        classes based on payment type.
        """
        pass

    def __str__(self):
        """Returns the employee's payment type, i.e. the name of the
        class.
        """
        pass

    def num(self):
        """Returns an integer that represents the classification of the
        employee.
        """
        pass


class Hourly(Classification):
    """Used for tracking the payment rate of an hourly-paid employee, and
    to store the hours they've worked, and calculate their pay.
    """
    def __init__(self, hourly_rate):
        """Initialize the hourly employee's data members, with no
        timecards stored.
        """
        super().__init__()
        self.hourly_rate = hourly_rate
        self.timecards = []

    def add_timecard(self, hours):
        """Adds the hours worked in a day to the hourly employee's
        timecards record.
        """
        self.timecards.append(hours)

    def calculate_pay(self):
        """Calculates the amount that will be paid to the hourly employee,
        hours worked x hourly rate.
        """
        payment = 0
        for hours in self.timecards:
            payment += hours * self.hourly_rate

        # Clear timecards so they are not reused.
        self.timecards = []

        return payment

    def __str__(self):
        """Returns a string representing employee's payment type.
        """
        return "hourly"

    def num(self):
        """Returns an integer representing the hourly classification type.
        """
        return 1


class Salary(Classification):
    """Used to track the salary of a salaried employee, and to calculate
    their pay.
    """
    def __init__(self, salary):
        """Initialize the salaried employee's data members.
        """
        super().__init__()
        self.salary = salary

    def calculate_pay(self):
        """Calculates the amount that will be paid to the salaried
        employee, 1/24th of their salary.
        """
        payment = self.salary / 24
        
        return payment

    def __str__(self):
        """Return's a string representing employee's payment type.
        """
        return "salary"
    
    def num(self):
        """Returns an integer representing the salary classification type.
        """
        return 2


class Commissioned(Salary):
    """Used for tracking the salary of a commissioned employee and storing
    their commission rate and the commissions they've made. Also used to
    calculate their pay.
    """
    def __init__(self, salary, commission_rate):
        """Initialize the commissioned employee's data members, with no
        commission receipts stored.
        """
        super().__init__(salary)
        self.commission_rate = commission_rate
        self.receipts = []

    def add_receipt(self, receipt):
        """Adds the number of commissions made in a day to the employee's
        receipts record.
        """
        self.receipts.append(receipt)

    def calculate_pay(self):
        """Calculates the amount that will be paid to the commissioned
        employee, 1/24th of their salary, and their commissions x
        commission rate.
        """
        payment = super().calculate_pay()
        for receipt in self.receipts:
            payment += self.commission_rate * receipt
        
        # Clear receipts so they are not reused.
        self.receipts = []

        return payment

    def __str__(self):
        """Return's a string representing employee's payment type.
        """
        return "commissioned"
    
    def num(self):
        """Returns an integer representing the commissioned classification
        type.
        """
        return 3


class PayMethod():
    """Used to track an employee's payment method, and print an applicable
    message about how and how much they will be paid. An abstract class.
    """
    def __init__(self, employee):
        """Initialize data members.

        Input: Employee object ("employee" param)
        """
        self.employee = employee

    def payment_message(self, amount):
        """Used to print an applicable message about how much employee
        will be paid, and in what method.
        """
        pass

    def num(self):
        """Returns an integer that represents the payment method in the
        data file.
        """
        pass


class DirectMethod(PayMethod):
    """Used for employees who opt to be paid by direct deposit. Stores
    their bank account information, and prints an applicable message about
    how much they will be paid via direct deposit on their next payday.
    """
    def __init__(self, employee, route_num, account_num):
        """Initialize data members for direct deposit. Keeps track of
        associated employee, their bank's routing number, and their bank
        account number.
        """
        super().__init__(employee)
        self.route_num = route_num
        self.account_num = account_num

    def payment_message(self, amount):
        """Used to print a message about how much the employee will be
        paid via direct deposit on their next payday.
        """
        return f'Will transfer ${amount:.2f} for {self.employee.name} to {self.route_num} at {self.account_num}'

    def __str__(self):
        """Returns a string representing the desired pay method.
        """
        return "direct deposit"

    def num(self):
        """Returns an integer that represents the direct pay method in the
        database file.
        """
        return 1


class MailedMethod(PayMethod):
    """Used for employees who opt to be paid by mail. Prints an applicable
    message about how much they will be paid via mail on their next
    payday.
    """
    def __init__(self, employee):
        """Initialize data members for mail method. Keeps track of the
        employee, and can access employee's mailing address.
        """
        super().__init__(employee)

    def payment_message(self, amount):
        """Used to print a message about how much the employee will be
        paid via mail on their next payday.
        """
        return f'Will mail ${amount:.2f} to {self.employee.name} at {self.employee.full_address()}'

    def __str__(self):
        """Returns a string representing the desired pay method.
        """
        return "mail"

    def num(self):
        """Returns an integer that represents the mail pay method in the
        database file.
        """
        return 2


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

    def __init__(self, id, name, birth_date, SSN, phone, email, permission):
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
        self.classification = None
        self.pay_method = None
        self.birth_date = birth_date
        self.ssn = SSN
        self.phone = phone
        self.email = email
        self.start_date = None
        self.end_date = None
        self.title = None
        self.dept = None
        self.permission = permission
        self.password = None


    def set_classification(self, class_num, pay_val_1, pay_val_2=0):
        """Sets the self.classification member of the employee class
        properly to an Hourly, Salary or Commissioned object, and stores
        the appropriate payment info within it.
        This function can be used to set/change an employee's pay, as
        well.

        Input: The int 1, 2, or 3 for classification type of Hourly,
                Salary, or Commissioned, respectively.

                For Hourly, input just hourly pay rate (float).
                For Salaried, input just salary (float).
                For Commissioned, input salary first (float), then
                    commission pay rate (float).
        """
        if class_num == 1:
            self.classification = Hourly(pay_val_1)
        elif class_num == 2:
            self.classification = Salary(pay_val_1)
        elif class_num == 3:
            self.classification = Commissioned(pay_val_1, pay_val_2)
        else:
            raise Exception(f'Classification for emp: "{self.name}" invalid.')

    def set_pay_method(self, pay_method_num, route=0, account=0):
        """Sets the self.pay_method member of the employee class properly
        to a DirectMethod or MailedMethod object, and stores the route and
        account number if DirectMethod.
        """
        if pay_method_num == 1:
            self.pay_method = DirectMethod(self, route, account)
        elif pay_method_num == 2:
            self.pay_method = MailedMethod(self)
        else:
            raise Exception(f'Pay method for emp: "{self.name}" invalid.')

    def set_address(self, address, city, state, zip):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip


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
        
        # Set the appropriate classification type:
        classification = int(row["Classification"])
        if classification == 1:
            self.classification = Hourly(float(row["Hourly"]))
        elif classification == 2:
            self.classification = Salary(float(row["Salary"]))
        elif classification == 3:
            self.classification = Commissioned(float(row["Salary"]),
                                    float(row["Commission"]))
        else:
            raise Exception(f'Classification for emp: "{self.name}" invalid.')

        self.ssn = row["Social Security Number"]
        self.phone = row["Phone Number"]
        self.email = row["Email"]
        self.address = row["Address"]
        self.city = row["City"]
        self.state = row["State"]
        self.zip = row["Zip"]

        # Set the desired pay method:
        pay_method = int(row["PayMethod"])
        if pay_method == 1:
            self.pay_method = DirectMethod(self, row["Route"], row["Account"])
        elif pay_method == 2:
            self.pay_method = MailedMethod(self)
        else:
            raise Exception(f'Pay method for emp: "{self.name}" invalid.')

        self.birth_date = row["Date of Birth"]
        self.start_date = row["Start Date"]
        self.end_date = row["End Date"]
        self.title = row["Title"]
        self.dept = row["Department"]
        self.permission = row["Permission Level"]
        self.password = row["Password"]

    def payment_report(self):
        """Returns a message that states how much the employee will be
        paid, and in what method.
        """
        payment = self.classification.calculate_pay()

        return self.pay_method.payment_message(payment)

    def full_address(self):
        """Returns the employee's full address.
        """
        return f'{self.address}, {self.city}, {self.state} {self.zip}'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False


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
        # Create employee csv file if it does not exist
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

        # Make Admin csv file if it doesn't exist
        if os.path.exists("admins.csv") != True:
            with open("admins.csv", "x") as DB:
                writer = csv.writer(DB)
                writer.writerow("ID,Name".split(','))
                self.admins = DB
        else:
            self.admins = open("admins.csv")

        if os.path.exists("archived.csv") != True:
            with open("archived.csv", "x") as DB:
                writer = csv.writer(DB)
                writer.writerow(
                    "ID,Name,Address,City,State,Zip,Classification,\
                    PayMethod,Salary,Hourly,Commission,Route,Account,\
                    Social Security Number,Phone Number,Email,\
                    Start Date,End Date,Title,Department,\
                    Password".split(','))
                self.archived = DB
        else:
            self.archived = open("archived.csv")
        self.emp_list = []
        self.archived_list = []
        self.update_emp_list()

    # Pulls data from the CSV to the emp list
    def update_emp_list(self):
        archDict = csv.DictReader(self.archived)
        for row in archDict:
            emp = Employee(None, None, None, None, None, None, None)
            emp.populate_from_row(row)
            self.archived_list.append(emp)
        empDict = csv.DictReader(self.db)
        for row in empDict:
            emp = Employee(None, None, None, None, None, None, None)
            emp.populate_from_row(row)
            if emp not in self.archived_list:
                self.emp_list.append(emp)

    def _add_row(self, emp: Employee, file):
        with open(file, "x") as DB:
            writer = csv.writer(DB)
            if str(emp.classification) == "hourly":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), -1, emp.classification.hourly_rate, -1, emp.pay_method.route_num,
                                emp.pay_method.account_num, emp.ssn, emp.phone, emp.email, emp.start_date, emp.end_date,
                                emp.title, emp.dept, emp.password)
                elif str(emp.pay_method) == "mail":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), -1, emp.classification.hourly_rate, -1, -1, -1, emp.ssn, emp.phone,
                                emp.email, emp.start_date, emp.end_date, emp.title, emp.dept, emp.password)
            elif str(emp.classification) == "salary":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), emp.classification.salary, -1, -1, emp.pay_method.route_num,
                                emp.pay_method.account_num, emp.ssn, emp.phone, emp.email, emp.start_date, emp.end_date,
                                emp.title, emp.dept, emp.password)
                elif str(emp.pay_method) == "mail":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), emp.classification.salary, -1, -1, -1, -1, emp.ssn, emp.phone,
                                emp.email, emp.start_date, emp.end_date, emp.title, emp.dept, emp.password)
            elif str(emp.classification) == "commissioned":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), emp.classification.salary, -1, emp.classification.commission_rate,
                                emp.pay_method.route_num, emp.pay_method.account_num, emp.ssn, emp.phone, emp.email,
                                emp.start_date, emp.end_date, emp.title, emp.dept, emp.password)
                elif str(emp.pay_method) == "mail":
                    writer.writerow(emp.id, emp.name, emp.address, emp.city, emp.state, emp.zip, emp.classification.num(),
                                emp.pay_method.num(), emp.classification.salary, -1, emp.classification.commission_rate,
                                -1, -1, emp.ssn, emp.phone, emp.email, emp.start_date, emp.end_date, emp.title, emp.dept,
                                emp.password)

    def archive_employee(self, id):
        """Removes from emp list and adds them to the archived file.
        """
        emp = find_employee_by_id(id, self.emp_list)
        self.emp_list.remove(emp)
        self._add_row(emp,"archived.csv")

    def add_employee(self,employee:Employee):
        self._add_row(employee, "employees.csv")


def open_file(the_file):
    """Function to open a file"""
    os.system(the_file)


def read_timecards():
    """Reads in all timecard lists from the "timecards.csv" file, and adds
    them to the hourly employees' individual records.
    """
    with open("timecards.csv", 'r') as timecards:
        for line in timecards:
            times = line.split(',')
            emp_id = int(times.pop(0))
            employee = find_employee_by_id(emp_id, uvuEmpDat.emp_list)

            if employee:
                if str(employee.classification) == "hourly":
                    for time in times:
                        employee.classification.add_timecard(float(time))


def read_receipts():
    """Reads in all receipt lists from the "receipts.csv" file, and adds
    them to the commissioned employees' individual records.
    """
    with open("receipts.csv", 'r') as receipts:
        for line in receipts:
            sales = line.split(',')
            emp_id = int(sales.pop(0))
            employee = find_employee_by_id(emp_id, uvuEmpDat.emp_list)

            if employee:
                if str(employee.classification) == "commissioned":
                    for receipt in sales:
                        employee.classification.add_receipt(float(receipt))


# Define global EmployeeDB object:
# EmployeeDatabase object should be global, so all functions can access
#   it?
uvuEmpDat = EmployeeDB()


# emp_list should be a list of Employee objects.
def find_employee_by_id(employee_id, emp_list):
    """Finds an employee with the given ID in the given employee list, and
    returns it. Returns None if no employee has the given ID.

    Input: int, list of Employee objects
    Output: Employee object with matching id, or None.
    """
    for employee in emp_list:
        if employee.id == employee_id:
            return employee
    return None


def validate_login(username, password): # working as designed.
    """Checks whether there is a user with the given username, and whether
    the given password matches that user's password.
    
    Input: int, string
    Output: Two bool values, the first saying whether the username was
            valid, the second saying whether the password was valid.
    """
    valid_username = False
    valid_password = False
    for employee in uvuEmpDat.emp_list:
        if employee.id == username:
            valid_username = True
            if employee.password == password:
                valid_password = True
    return valid_username, valid_password


def login():
    """Initiates the login process, and if login is valid, logs the user
    in. Logs them in according to their permission level. Admins see the
    admin screen, and normal employees just see their own data.
    """    
    # Allow for exception if username is not a string.
    try:
        # Get username and password variables from entries on login GUI
        #   screen.
        users_id = int(user_id.get())
        user_password = password.get()

        # Validate login with username and password from the login GUI
        #   screen entries.
        username_valid, password_valid = validate_login(users_id,
                                            user_password)
        if username_valid and password_valid:
            employee = find_employee_by_id(users_id, uvuEmpDat.emp_list)
            if employee.permission == "admin":
                open_admin()
            else:
                open_employee(employee, employee.permission)
            pass
        else:
            login_error()
    # If username is not a string:
    except:
        print("Username was not an integer.")
        login_error()
    


def open_admin():
    """Generates a GUI window of the admin view, a list of all employees,
    and generates all of its functionality, so that you can click on
    employees to view their data, and can generate a report of all
    employees.
    """

    #Admin Window
    admin_window = Toplevel(login_window)
    #Menu Bar of Admin Employee list screen    
    menu_bar = Menu(admin_window)
    #Adds option of File to menu bar
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=add_employee_screen)
    file_menu.add_separator()
    file_menu.add_command(label="Close All", command=button_close_warning)
    menu_bar.add_cascade(label="File", menu=file_menu)
    #Adds option of Help to menu bar
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=under_construction)
    help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
    menu_bar.add_cascade(label="Help", menu=help_menu)
    #Adds the menu bar
    admin_window.config(menu=menu_bar)    
    #Title of Admin Window
    admin_window.title("UVU Employee Database")
    
    #Style - default coloring
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="whitesmoke", \
        foreground="black", rowheight=35, fieldbackground="whitesmoke")

    style.map("Treeview", background=[("selected", "olivedrab")])
    
    
    #Create Employee Tree Frame
    emp_frame = Frame(admin_window)
    emp_frame.pack(pady=0)
    
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

    employee_list = ttk.Treeview(emp_frame, columns=columns_list, \
        show="headings")
    for column in columns_list:
        employee_list.column(column, width=130)

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
                        str(emp.classification), \
                        emp.title, emp.dept), tags=("evenrows",))
        else:
            employee_list.insert('', END, values=(emp.id, emp.first_name,\
                        emp.last_name, emp.ssn, emp.phone, emp.email, \
                        emp.start_date, emp.end_date, \
                        str(emp.classification), \
                        emp.title, emp.dept), tags=("oddrows",))
        count+=1
    
    #Button frame on Admin list
    button_frame = Frame(admin_window)
    button_frame.pack(pady=0)
    #Report button
    report_button = Button(button_frame, text="Report", \
                           command=under_construction).grid(row=0, column=0, padx=5, pady=5)

    
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
    scrollbar = ttk.Scrollbar(emp_frame, orient=VERTICAL, \
                        command=employee_list.yview)
                        
    employee_list.config(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky="ns")
    
    #Run the window
    admin_window.mainloop()


def add_employee_screen():
    """Opens a screen for entering information to add a new user to the
    UVU Employee Database.
    """
    add_emp_window = Toplevel()
    
    hourly_rate = StringVar(add_emp_window)
    salary = StringVar(add_emp_window)
    commission_rate = StringVar(add_emp_window)
    route_num = StringVar(add_emp_window)
    account_num = StringVar(add_emp_window)
    
    def generate_pay_fields(var, index, mode):
        """Generates the correct pay fields on the create employee screen
        based on the selected employee classification.

        Takes parameters from a trace_add event.
        """
        delete_pay_fields()

        if classification.get() == "Hourly":
            # Field to set hourly pay rate:
            global hourly_label
            global hourly_entry
            hourly_label = Label(add_emp_window, text="Hourly Pay Rate:")
            hourly_label.grid(row=6, column=3, padx=25, pady=5)
            hourly_entry = Entry(add_emp_window,\
                textvariable=hourly_rate)
            hourly_entry.grid(row=6, column=4, padx=50,
                pady=5)
        
        elif classification.get() == "Salary":
            # Field to set salary:
            global salary_label
            global salary_entry
            salary_label = Label(add_emp_window, text="Salary:")
            salary_label.grid(row=6, column=3, padx=25, pady=5)
            salary_entry = Entry(add_emp_window,textvariable=salary)
            salary_entry.grid(row=6, column=4, padx=50, pady=5)
        
        elif classification.get() == "Commission":
            # Field to set salary:
            global com_salary_label
            global com_salary_entry
            global commission_label
            global commission_entry
            com_salary_label = Label(add_emp_window, text="Salary:")
            com_salary_label.grid(row=6, column=3, padx=25, pady=5)
            com_salary_entry = Entry(add_emp_window,textvariable=salary)
            com_salary_entry.grid(row=6, column=4, padx=50, pady=5)
            
            # Field to set commission pay rate:
            commission_label = Label(add_emp_window,
                text="Commission Pay Rate:")
            commission_label.grid(row=7, column=3,
                padx=10, pady=10)
            commission_entry = Entry(add_emp_window,
                textvariable=commission_rate)
            commission_entry.grid(row=7, column=4,
                padx=10, pady=10)

    def delete_pay_fields():
        """Deletes extra pay fields and labels that are not needed from
        the create employee screen.
        """
        # Delete any non-applicable pay fields.
        try:
            hourly_label.destroy()
            hourly_entry.destroy()
        except Exception:
            pass

        try:
            salary_label.destroy()
            salary_entry.destroy()
        except Exception:
            pass

        try:
            commission_label.destroy()
            commission_entry.destroy()
            com_salary_label.destroy()
            com_salary_entry.destroy()
        except Exception:
            pass

    def generate_bank_fields(var, index, mode):
        """Generates the bank info fields on the create employee screen
        when the employee payment type is direct deposit.

        Takes parameters from a trace_add event.
        """
        if pay_method.get() == "Direct Deposit":
            # Routing number entry:
            global route_label
            global route_entry
            route_label = Label(add_emp_window, text="Bank Routing Number:")
            route_label.grid(row=9, column=3, padx=25, pady=5)
            route_entry = Entry(add_emp_window,
                textvariable=route_num)
            route_entry.grid(row=9, column=4, padx=50, pady=5)
            
            # Account number entry:
            global account_label
            global account_entry
            account_label = Label(add_emp_window, text="Bank Account Number:")
            account_label.grid(row=10, column=3, padx=25, pady=5)
            account_entry = Entry(add_emp_window,
                textvariable=account_num)
            account_entry.grid(row=10, column=4, padx=50, pady=5)

        else:
            try:
                route_label.destroy()
                route_entry.destroy()
                account_label.destroy()
                account_entry.destroy()
            except Exception:
                pass

    max_id = 0
    for emp in uvuEmpDat.emp_list + uvuEmpDat.archived_list:
        if emp.id > max_id:
            max_id = emp.id
        
    new_id = max_id + 1

    # ID Entry:
    id_title = Label(add_emp_window, text="Employee ID:").grid(row=1,
            column=1, padx=25, pady=5)
    id_label = Label(add_emp_window, text=new_id)\
            .grid(row=1, column=2, padx=50, pady=5)
    
    # First name entry:
    first_name_label = Label(add_emp_window, text="First Name:").grid(row=2,
            column=1, padx=25, pady=5)
    first_name = StringVar(add_emp_window)
    id_first_name = Entry(add_emp_window, textvariable=first_name)\
            .grid(row=2, column=2, padx=50, pady=5)

    # Last name entry:
    last_name_label = Label(add_emp_window, text="Last Name:").grid(row=3,
            column=1, padx=25, pady=5)
    last_name = StringVar(add_emp_window)
    last_name_entry = Entry(add_emp_window, textvariable=last_name)\
            .grid(row=3, column=2, padx=50, pady=5)

    # Social security number entry:
    ssn_label = Label(add_emp_window, text="SSN:").grid(row=4,
            column=1, padx=25, pady=5)
    ssn = StringVar(add_emp_window)
    ssn_entry = Entry(add_emp_window, textvariable=ssn)\
            .grid(row=4, column=2, padx=50, pady=5)

    # Phone entry:
    phone_label = Label(add_emp_window, text="Phone:").grid(row=5,
            column=1, padx=25, pady=5)
    phone = StringVar(add_emp_window)
    phone_entry = Entry(add_emp_window, textvariable=phone)\
            .grid(row=5, column=2, padx=50, pady=5)

    # Email entry:
    email_label = Label(add_emp_window, text="Email:").grid(row=6,
            column=1, padx=25, pady=5)
    email = StringVar(add_emp_window)
    email_entry = Entry(add_emp_window, textvariable=email)\
            .grid(row=6, column=2, padx=50, pady=5)

    # Address entry:
    address_label = Label(add_emp_window, text="Street Address:").grid(row=7,
            column=1, padx=25, pady=5)
    address = StringVar(add_emp_window)
    address_entry = Entry(add_emp_window, textvariable=address)\
            .grid(row=7, column=2, padx=50, pady=5)

    # City entry:
    city_label = Label(add_emp_window, text="City:").grid(row=8,
            column=1, padx=25, pady=5)
    city = StringVar(add_emp_window)
    city_entry = Entry(add_emp_window, textvariable=city)\
            .grid(row=8, column=2, padx=50, pady=5)

    # State entry:
    state_label = Label(add_emp_window, text="State:").grid(row=9,
            column=1, padx=25, pady=5)
    state = StringVar(add_emp_window)
    state_entry = Entry(add_emp_window, textvariable=state)\
            .grid(row=9, column=2, padx=50, pady=5)

    # Zip code entry:
    zip_label = Label(add_emp_window, text="Zip Code:").grid(row=10,
            column=1, padx=25, pady=5)
    zip = StringVar(add_emp_window)
    zip_entry = Entry(add_emp_window, textvariable=zip)\
            .grid(row=10, column=2, padx=50, pady=5)

    # Birth date entry:
    birth_date_label = Label(add_emp_window, text="Birth Date:").grid(row=11,
            column=1, padx=25, pady=5)
    birth_date = StringVar(add_emp_window)
    birth_date_entry = Entry(add_emp_window, textvariable=birth_date)\
            .grid(row=11, column=2, padx=50, pady=5)

    # Start date entry:
    start_date_label = Label(add_emp_window, text="Start Date:").grid(row=1,
            column=3, padx=25, pady=5)
    start_date = StringVar(add_emp_window)
    start_date_entry = Entry(add_emp_window, textvariable=start_date)\
            .grid(row=1, column=4, padx=50, pady=5)

    # Title entry:
    title_label = Label(add_emp_window, text="Title:").grid(row=2,
            column=3, padx=25, pady=5)
    title = StringVar(add_emp_window)
    title_entry = Entry(add_emp_window, textvariable=title)\
            .grid(row=2, column=4, padx=50, pady=5)

    # Dept entry:
    dept_label = Label(add_emp_window, text="Department:").grid(row=3,
            column=3, padx=25, pady=5)
    dept = StringVar(add_emp_window)
    dept_entry = Entry(add_emp_window, textvariable=dept)\
            .grid(row=3, column=4, padx=50, pady=5)

    # Admin entry:
    # Some sort of entry or radio button or drop-down to select if admin.

    # Password entry:
    password_label = Label(add_emp_window, text="Password:").grid(row=4,
            column=3, padx=25, pady=5)
    password = StringVar(add_emp_window)
    password_entry = Entry(add_emp_window, textvariable=password)\
            .grid(row=4, column=4, padx=50, pady=5)

    # Classification entry:
    classification_label = Label(add_emp_window, text="Classification:")\
        .grid(row=5, column=3, padx=25, pady=5)
    classification = StringVar(add_emp_window)
    classification.set("Classficiation Type")
    class_drop = OptionMenu(add_emp_window, classification, "Hourly",
        "Salary", "Commission").grid(row=5, column=4, padx=50, pady=5)
    classification.trace_add('write', generate_pay_fields)
    # Make a classification drop-down box. Also a way to say what their
    #   pay is, based on their classification's pay type.

    # PayMethod entry:
    # Make a dropdown box to select PayMethod.
    method_label = Label(add_emp_window, text="Pay Method:")\
        .grid(row=8, column=3, padx=25, pady=5)
    pay_method = StringVar(add_emp_window)
    pay_method.set("Payment Method")
    method_drop = OptionMenu(add_emp_window, pay_method,
        "Direct Deposit", "Mail").grid(row=8, column=4, padx=50, pady=5)
    pay_method.trace_add('write', generate_bank_fields)

    create_button = Button(add_emp_window, text="Create",
        command=under_construction).grid(row=12, column=4, padx=10,
        pady=10)    

    add_emp_window.mainloop()


def edit_employee_info(the_edit):
    """Generates a GUI window with information of the employee.
    Also generates an entry box and a button to update information"""
    #Creates the edit window
    edit_window = Toplevel(login_window)
    #Shows previous information before edit
    prev_info = Label(edit_window, text="Previous Information:  ").grid(row=0, column=0, padx=10, pady=10)
    edit_this = Label(edit_window, text=the_edit).grid(row=0, column=1, padx=10, pady=10)
    #Label what the entry box is for
    info_here_label = Label(edit_window, text="Enter new info here:  ").grid(row=1, column=0, padx=10, pady=10)
    new_info = StringVar()
    #New information entry box
    updated_info = Entry(edit_window, textvariable=new_info).grid(row=1, column=1, padx=10, pady=10)
    #Button to update information
    update_button = Button(edit_window, text="Update Information", command=under_construction).grid(row=2, columnspan=2, padx=10, pady=10)



# Need to fill the fields for a single employee's data.
def open_employee(employee, permission_level):
    """Generates a GUI window populated with the data of the given
    employee. Also creates buttons to allow for editing an employee's data
    and printing a report for that employee. Will have a back button as
    well if permission_level is "admin".
    Input: Employee object, string.
    """
    #Employee Window
    employee_window = Toplevel(login_window)
    #Menu Bar of Employee Information screen
    menu_bar = Menu(employee_window)
    #Adds option of Edit to menu bar
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    #The sub-options under 'Edit'
    edit_menu.add_command(label="First Name", command=lambda:edit_employee_info(employee.first_name))
    edit_menu.add_command(label="Last Name", command=lambda:edit_employee_info(employee.last_name))
    edit_menu.add_command(label="Social Security Number", command=lambda:edit_employee_info(employee.ssn))
    edit_menu.add_command(label="Phone Number", command=lambda:edit_employee_info(employee.phone))
    edit_menu.add_command(label="Email", command=lambda:edit_employee_info(employee.email))
    edit_menu.add_command(label="Street Address", command=lambda:edit_employee_info(employee.address))
    edit_menu.add_command(label="City", command=lambda:edit_employee_info(employee.city))
    edit_menu.add_command(label="State", command=lambda:edit_employee_info(employee.state))
    edit_menu.add_command(label="Zip Code", command=lambda:edit_employee_info(employee.zip))
    edit_menu.add_command(label="Date of Birth", command=lambda:edit_employee_info(employee.birth_date))
    edit_menu.add_command(label="Password", command=lambda:edit_employee_info(employee.password))
    edit_menu.add_command(label="Employee ID", command=lambda:edit_employee_info(employee.id))
    edit_menu.add_command(label="Job Title", command=lambda:edit_employee_info(employee.title))
    edit_menu.add_command(label="Department", command=lambda:edit_employee_info(employee.dept))
    edit_menu.add_command(label="Start Date", command=lambda:edit_employee_info(employee.start_date))
    edit_menu.add_command(label="End Date", command=lambda:edit_employee_info(employee.end_date))
    edit_menu.add_command(label="Account Number", command=lambda:edit_employee_info(employee.pay_method.account_num))
    edit_menu.add_command(label="Routing Number", command=lambda:edit_employee_info(employee.pay_method.route_num))
    edit_menu.add_command(label="Payment Method", command=lambda:edit_employee_info(employee.pay_method))
    edit_menu.add_command(label="Classification", command=lambda:edit_employee_info(employee.classification))
    #Adds 'Edit' options
    file_menu.add_cascade(label="Edit", menu=edit_menu)
    #Puts in a line in the menu list
    file_menu.add_separator()
    #Option to close the file
    file_menu.add_command(label="Close All", command=button_close_warning)
    #Adds'File' options
    menu_bar.add_cascade(label="File", menu=file_menu)
    #Adds option of Help to menu bar
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=under_construction)
    help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
    menu_bar.add_cascade(label="Help", menu=help_menu)
    #Adds the menu bar
    employee_window.config(menu=menu_bar)
    
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

    #Account and Routing Numbers, if employee uses direct deposit:
    if str(employee.pay_method) == "direct deposit":
        account_title = Label(employee_window, text="Account Number")\
            .grid(row=7, column=3, padx=10, pady=10)
        # FIXME: Have the account_label connect with the employee's payment
        #   method. Only shows account if they are paid by direct method.
        account_label = Label(employee_window, text=str(employee.pay_method.account_num))\
            .grid(row=8, column=3, padx=10, pady=10)

        routing_title = Label(employee_window, text="Routing Number")\
            .grid(row=7, column=4, padx=10, pady=10)
        # FIXME: Have the routing_label connect with the employee's payment
        #   method. Only shows routing num if they are paid by direct method.
        routing_label = Label(employee_window, text=employee.pay_method.route_num)\
            .grid(row=8, column=4, padx=10, pady=10)

    #Payment Method
    payment_title = Label(employee_window, text="Payment Method")\
        .grid(row=7, column=5, padx=10, pady=10)
    # FIXME: Give PayMethod class a "print()" method that prints "Direct
    #   Deposit" or "Mail", whichever child class they have.
    payment_label = Label(employee_window, text=str(employee.pay_method))\
        .grid(row=8, column=5, padx=10, pady=10)

    #Classification
    classification_title = Label(employee_window, text="Classification")\
        .grid(row=9, column=3, padx=10, pady=10)
    classification_label = Label(employee_window, \
        text=str(employee.classification))\
        .grid(row=10, column=3, padx=10, pady=10)

    # Show pay amounts, based on classification type:
    if str(employee.classification) == "hourly":
        hourly_title = Label(employee_window, text="Hourly Rate")\
            .grid(row=11, column=3, padx=10, pady=10)
        hourly_label = Label(employee_window, text=f'${employee.classification.hourly_rate:.2f}')\
            .grid(row=12, column=3, padx=10, pady=10)
    #Salary
    elif str(employee.classification) == "salary":
        salary_title = Label(employee_window, text="Salary")\
            .grid(row=11, column=3, padx=10, pady=10)
        salary_label = Label(employee_window, text=f'${employee.classification.salary:.2f}')\
            .grid(row=12, column=3, padx=10, pady=10)
    #Commission
    elif str(employee.classification) == "commissioned":
        salary_title = Label(employee_window, text="Salary")\
            .grid(row=11, column=3, padx=10, pady=10)
        salary_label = Label(employee_window, text=f'${employee.classification.salary:.2f}')\
            .grid(row=12, column=3, padx=10, pady=10)
        commission_title = Label(employee_window, text="Commission Rate")\
            .grid(row=11, column=4, padx=10, pady=10)
        commission_label = Label(employee_window, text=f'${employee.classification.commission_rate:.2f}')\
            .grid(row=12, column=4, padx=10, pady=10)

    # Buttons
    pay_stub_button = Button(employee_window, text="Get Pay Stub",
        command=partial(generate_pay_stub, employee)).grid(row=13,
        column=5, padx=10, pady=10)

    if permission_level == "admin":
        back_button = Button(employee_window, text="Back", 
            command=partial(exit_window, employee_window)).grid(row=13, 
            column=4, padx=10, pady=10)
        report_all_button = Button(employee_window,
            text="All Emps Report", command=prompt_report_all_employees)\
                .grid(row=13, column=0, padx=10, pady=10)




def prompt_report_all_employees():
    """Generates a GUI prompt asking whether the user wants to include
    archived employees in the report, and generates the proper report
    based on the user's response. Also allows user to click a cancel
    button to close the window without generating a report.
    """
    res = askyesno("Employee Report", "Do you want to include archived employees in the report?")
    print(res)
    if res == True:
        print("Generating archive report.")
        generate_report_all_employees(True)
    else:
        print("Generating non-archive report.")
        generate_report_all_employees(False)


# Should this report be a payment report, just a general info report, or
#   both?
def generate_report_all_employees(include_archived):
    """Generates a report of all employees in the database, in the form of
    a text document titled report.csv. The report will include the info of
    archived employees if include_archived is True, and will not if it is
    False.
    """
    # If include_archived, then emp_list will be all employees
    if include_archived:
    #   (from EmployeeDatabase.archived and EmployeeDatabase.database).
        emp_list = uvuEmpDat.emp_list + uvuEmpDat.archived_list
    else: # Otherwise emp_list will be all non-archived employees (from
    #   EmployeeDatabase.database).
        emp_list = uvuEmpDat.emp_list

    read_timecards()
    read_receipts()
    with open("report.csv", "w") as report:
        for employee in emp_list:
            # Write a line to "report.csv" that reports on all data
            #   members for the employee.
            if str(employee.classification) == "hourly":
                if str(employee.pay_method) == "direct deposit":
                    report.write(
                        f"Employee ID: {employee.id}       Name: {employee.name}         Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification}    Hourly pay: ${employee.classification.hourly_rate:.2f}       Payment method: {employee.pay_method}\n"
                        f"Routing num: {employee.pay_method.route_num}   Account num: {employee.pay_method.account_num} Date of birth: {employee.birth_date}\n"
                        f"SSN: {employee.ssn}          Phone: {employee.phone}     Email: {employee.email}\n"
                        f"Start date: {employee.start_date}     End date: {employee.end_date}\n"
                        f"Title: {employee.title}           Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission}   Password: {employee.password}\n\n")
                elif str(employee.pay_method) == "mail":
                    report.write(
                        f"Employee ID: {employee.id}        Name: {employee.name}   Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification}     Hourly pay: ${employee.classification.hourly_rate:.2f}       Payment method: {employee.pay_method}\n"
                        f"Date of birth: {employee.birth_date}  SSN: {employee.ssn}\n"
                        f"Phone: {employee.phone}       Email: {employee.email}\n"
                        f"Start date: {employee.start_date}       End date: {employee.end_date}\n"
                        f"Title: {employee.title}      Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission} Password: {employee.password}\n\n")
            elif str(employee.classification) == "salary":
                if str(employee.pay_method) == "direct deposit":
                    report.write(
                        f"Employee ID: {employee.id}        Name: {employee.name}      Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification}     Salary: ${employee.classification.salary:.2f}    Payment method: {employee.pay_method}\n"
                        f"Routing number: {employee.pay_method.route_num} Account number: {employee.pay_method.account_num}    Date of birth: {employee.birth_date}\n"
                        f"SSN: {employee.ssn}           Phone: {employee.phone}    Email: {employee.email}\n"
                        f"Start date: {employee.start_date}       End date: {employee.end_date}\n"
                        f"Title: {employee.title}           Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission}    Password: {employee.password}\n\n")
                elif str(employee.pay_method) == "mail":
                    report.write(
                        f"Employee ID: {employee.id}      Name: {employee.name}    Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification}   Salary: ${employee.classification.salary:.2f}       Payment method: {employee.pay_method}\n"
                        f"Date of birth: {employee.birth_date} SSN: {employee.ssn}\n"
                        f"Phone: {employee.phone}     Email: {employee.email}\n"
                        f"Start date: {employee.start_date}     End date: {employee.end_date}\n"
                        f"Title: {employee.title}           Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission}  Password: {employee.password}\n\n")                
            elif str(employee.classification) == "commissioned":
                if str(employee.pay_method) == "direct deposit":
                    report.write(
                        f"Employee ID: {employee.id}             Name: {employee.name}      Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification}    Salary: ${employee.classification.salary:.2f}          Commission rate: ${employee.classification.commission_rate:.2f}\n"
                        f"Payment method: {employee.pay_method}  Routing number: {employee.pay_method.route_num} Account number: {employee.pay_method.account_num}\n"
                        f"Date of birth: {employee.birth_date}        SSN: {employee.ssn}           Phone: {employee.phone}\n"
                        f"Email: {employee.email}    Start date: {employee.start_date}      End date: {employee.end_date}\n"
                        f"Title: {employee.title}         Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission}      Password: {employee.password}\n\n")
                elif str(employee.pay_method) == "mail":
                    report.write(
                        f"Employee ID: {employee.id}          Name: {employee.name}    Address: {employee.full_address()}\n"
                        f"Classification: {employee.classification} Salary: ${employee.classification.salary:.2f}        Commission rate: ${employee.classification.commission_rate:.2f}\n"
                        f"Payment method: {employee.pay_method}         Date of birth: {employee.birth_date}\n"
                        f"SSN: {employee.ssn}             Phone: {employee.phone}     Email: {employee.email}\n"
                        f"Start date: {employee.start_date}        End date: {employee.end_date}\n"
                        f"Title: {employee.title}               Dept: {employee.dept}\n"
                        f"Permission level: {employee.permission}      Password: {employee.password}\n\n")
            
            # Write a line to "report.csv" stating what the employee will
            #   be paid.
            pay_report = employee.payment_report()
            report.write(f"\t{pay_report}\n\n\n")
    
    # report_window = Toplevel()

    # with open("report.csv", 'r') as report_in:
    #     count = 0
    #     for line in report_in:
    #         count += 1
    #         Label(report_window, text=line).grid(row=count, padx=10,
    #             pady=10)
    # #Scrollbar
    # scrollbar = ttk.Scrollbar(report_window, orient=VERTICAL, \
    #                     command=report_window.yview)
                        
    # report_window.config(yscroll=scrollbar.set)
    # scrollbar.grid(row=1, column=1, sticky="ns")

    # report_window.mainloop()
    
    # Print message in GUI screen saying that report can also be viewed
    #   and shared from "report.csv".
    # Bind event listener to "Back" button to exit the report's window.


def generate_pay_stub(employee):
    """Generates a pay stub/report for the given employee, with the name:
    {employee.last_name}_{employee.first_name}_pay_stub.csv.
    """
    def export_pay_stub_csv(name_message, pay_message, rate_message_1, rate_message_2):
        """Exports the pay stub to a .csv file, named with the employee's
        name and saved in the same directory as this program.
        
        Input: the text that should be printed on the pay stub.
        Output: writes to a pay stub file, named based on the employee's
                name.
        """
        with open(f'{employee.last_name}_{employee.first_name}_pay_stub.csv', 'w') as pay_file:
            pay_file.write(
                f'{name_message}\n'
                f'{rate_message_1}\n'
                f'{rate_message_2}\n'
                f'{pay_message}\n'
            )

    def pay_stub_screen(name_message, pay_message, rate_message_1, rate_message_2): # If we don't use this function, bypass
        # straight to export_pay_stub_csv, and just generate a stub file.
        """Initialize a GUI screen that shows the text for how much the
        employee was payed on their last pay date, and any other
        applicable pay stub info, like hours worked or commissions made.
        Also allows the user the option to export the pay stub to .csv
        format.
        """
        pay_stub_window = Toplevel()
        # pay_stub_window.geometry("500x250")
        
        # Message:
        name_label = Label(pay_stub_window, text=name_message)\
            .grid(row=1, column=0, padx=10, pady=10)
        rate_1_label = Label(pay_stub_window, text=rate_message_1)\
            .grid(row=2, column=0, padx=10, pady=10)
        rate_2_label = Label(pay_stub_window, text=rate_message_2)\
            .grid(row=3, column=0, padx=10, pady=10)
        pay_message_label = Label(pay_stub_window, text=pay_message)\
            .grid(row=5, column=0, padx=10, pady=10)

        export_button = Button(pay_stub_window, text="Export to CSV",
        command=partial(export_pay_stub_csv, name_message, pay_message,
            rate_message_1, rate_message_2)).grid(row=7, column=3,
            padx=10, pady=10)     

        pay_stub_window.mainloop()
        
    pay_date = "" # Not sure if this will be used.
    pay_num = 0   # For storing hours or commissions.
    with open("report.csv", 'r') as report:
        line_count = 0
        for line in report:
            line_count += 1

            # Check if the line is a line with an employee id (only 
            #   certain lines have them). Skip iteration if not.
            if not (line_count - 1) % 11 == 0:
                continue
            info = line.strip().split(' ')
            if int(info[2]) == employee.id:
                for num in range(7):
                    report.readline()
                pay_info = report.readline().split(' ')
            
                # Get the payment amount without the dollar sign? Use [1:]
                pay_amount = pay_info[2][1:]
                pay_message = f"Paid ${pay_amount} to {employee.name}."
                rate_message_1=""
                rate_message_2=""
                if str(employee.classification) == "hourly":
                    rate_message_1 = f'Hourly pay: ${employee.classification.hourly_rate}'
                elif str(employee.classification) == "salary":
                    rate_message_1 = f'Salary: ${employee.classification.salary}'
                elif str(employee.classification) == "commissioned":
                    rate_message_1 = f'Salary: ${employee.classification.salary}'
                    rate_message_2 = f'Commission rate: ${employee.classification.commission_rate}'
                else:
                    raise Exception(f'Error with employee "{employee.name}\'s" classification')
                
                name_message = f'Employee Name: {employee.name}'

                pay_stub_screen(name_message, pay_message, rate_message_1, rate_message_2)
                
                break
               
            # Else:
                # Show an error pop-up message, that the employee was not payed in
                #   the last pay period (may happen before any "report.csv" file
                #   is generated).


def login_error():
    """Displays an error message in relation to logging in. To be
    displayed if a user tries to login with invalid information.
    """
    showinfo("Invalid Login", "The username or password entered was invalid.",
        icon=WARNING)


def under_construction():
    """Displays a warning message that the section is still under
    development.
    """
    showinfo("Warning", "This function is still under development.",
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
login_window.update()
#Menu Bar of Login screen
menu_bar = Menu(login_window)
#Adds option of File to menu bar
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Close All", command=button_close_warning)
menu_bar.add_cascade(label="File", menu=file_menu)
#Adds option of Help to menu bar
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=under_construction)
help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
menu_bar.add_cascade(label="Help", menu=help_menu)
#Adds the menu bar
login_window.config(menu=menu_bar)

#Size of Login Window
login_window.geometry("515x360")
#Title of Login Window
login_window.title("UVU Employee Database")
#Login Window Name
login_window_label = Label(login_window, text="Login").grid(row=1, \
    columnspan=3, padx=50, pady=50)

#User ID Text
user_id_label = Label(login_window, text="User ID").grid(row=2, \
    column=1, padx=25, pady=5)
#User ID Textbox
user_id = StringVar(login_window)
user_id_entry = Entry(login_window, textvariable=user_id)\
    .grid(row=2, column=2, padx=50, pady=5)  

#Password Text
password_label = Label(login_window,text="Password").grid(row=3, \
    column=1, padx=25, pady=5)
#Password Textbox
password = StringVar(login_window)
password_entry = Entry(login_window, textvariable=password, show='*')\
    .grid(row=3, column=2, padx=5, pady=5)  

#Login Button
login_button = Button(login_window, text="Login", \
    command=login).grid(row=4, column=2, padx=25, pady=25)

#Close Button
exit_button = Button(login_window, text="Close", \
    command=button_close_warning).grid(row=5, column = 4, padx=5, pady=5)


def main():   
    """Starts up the entire application, starting with the login screen.
    """
    #Run the window
    login_window.mainloop()
    

if __name__ == "__main__":
    main()

