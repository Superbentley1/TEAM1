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
import re
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo, askokcancel, askyesno, WARNING
from types import new_class

from EmployeeDB import *

uvuEmpDat = EmployeeDB()

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


def validate_login(username, password):  # working as designed.
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
        login_error()


def open_admin():
    """Generates a GUI window of the admin view, a list of all employees,
    and generates all of its functionality, so that you can click on
    employees to view their data, and can generate a report of all
    employees.
    """

    # Admin Window
    global admin_window
    admin_window = Toplevel(login_window)
    # Menu Bar of Admin Employee list screen
    menu_bar = Menu(admin_window)
    # Adds option of File to menu bar
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=add_employee_screen)
    file_menu.add_separator()
    file_menu.add_command(label="Close All", command=button_close_warning)
    menu_bar.add_cascade(label="File", menu=file_menu)
    # Adds option of Help to menu bar
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=under_construction)
    help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # Adds the menu bar
    admin_window.config(menu=menu_bar)
    # Title of Admin Window
    admin_window.title("UVU Employee Database")

    # Style - default coloring
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="whitesmoke", \
                    foreground="black", rowheight=35, fieldbackground="whitesmoke")

    style.map("Treeview", background=[("selected", "olivedrab")])

    # Create Employee Tree Frame
    emp_frame = Frame(admin_window)
    emp_frame.pack(pady=0)
    
    def search_records():
        # Get the entry from search
        lookup_record = search_entry.get()
        # Clear the Treeview
        for record in employee_list.get_children():
            employee_list.delete(record)
        # Populating the treeview with findings of the sort
        count = 0
        for emp in uvuEmpDat.emp_list:
            # Will check if the search is in the name of employee then show
            if lookup_record.lower() in str(emp).lower():
                if count % 2 == 0:
                    employee_list.insert('', END, values=(emp.id, emp.first_name, \
                                                          emp.last_name, emp.ssn, emp.phone, emp.email, \
                                                          emp.start_date, emp.end_date, \
                                                          str(emp.classification), \
                                                          emp.title, emp.dept), tags=("evenrows",))
                else:
                    employee_list.insert('', END, values=(emp.id, emp.first_name, \
                                                          emp.last_name, emp.ssn, emp.phone, emp.email, \
                                                          emp.start_date, emp.end_date, \
                                                          str(emp.classification), \
                                                          emp.title, emp.dept), tags=("oddrows",))
                count += 1
                  
    # Search frame on Admin list
    search_frame = Frame(admin_window)
    search_frame.pack(pady=0)
    # Search Entry Box
    search_entry = Entry(search_frame)
    search_entry.grid(row=0, column=0, padx=5, pady=5)
    # Search Button
    search_button = Button(search_frame, text="Search", command=search_records)
    search_button.grid(row=0, column=1, padx=5, pady=5)
    
    def tree_column_sort(tree, the_column, other_way):
        # Get the values to sort
        information = [(tree.set(k, the_column), k) for k in tree.get_children('')]
        # Rearrange to sorted positions
        information.sort(reverse=other_way)
        for index, data in enumerate(information):
            tree.move(data[1], '', index)
        # Reverse the sort on next click
        tree.heading(the_column,
                     command=lambda c=columns_list[the_column]: tree_column_sort(tree, the_column, not other_way))

    # Define columns
    columns_list = ("employee_id", "first_name", "last_name", \
                    "social_security_number", "phone_number", "email", "start_date", \
                    "end_date", "classification", "title", "department")

    employee_list = ttk.Treeview(emp_frame, columns=columns_list, \
                                 show="headings")
    for column in columns_list:
        employee_list.column(column, width=130)

    # Define headings
    employee_list.heading("employee_id", text="Employee ID",
                          command=lambda c=columns_list[0]: tree_column_sort(employee_list, 0, False))
    employee_list.heading("first_name", text="First Name",
                          command=lambda c=columns_list[1]: tree_column_sort(employee_list, 1, False))
    employee_list.heading("last_name", text="Last Name",
                          command=lambda c=columns_list[2]: tree_column_sort(employee_list, 2, False))
    employee_list.heading("social_security_number", \
                          text="Social Security Number",
                          command=lambda c=columns_list[3]: tree_column_sort(employee_list, 3, False))

    employee_list.heading("phone_number", text="Phone Number",
                          command=lambda c=columns_list[4]: tree_column_sort(employee_list, 4, False))
    employee_list.heading("email", text="Email",
                          command=lambda c=columns_list[5]: tree_column_sort(employee_list, 5, False))
    employee_list.heading("start_date", text="Starting Date",
                          command=lambda c=columns_list[6]: tree_column_sort(employee_list, 6, False))
    employee_list.heading("end_date", text="Ending Date",
                          command=lambda c=columns_list[7]: tree_column_sort(employee_list, 7, False))
    employee_list.heading("classification", text="Classification",
                          command=lambda c=columns_list[8]: tree_column_sort(employee_list, 8, False))
    employee_list.heading("title", text="Title",
                          command=lambda c=columns_list[9]: tree_column_sort(employee_list, 9, False))
    employee_list.heading("department", text="Department",
                          command=lambda c=columns_list[10]: tree_column_sort(employee_list, 10, False))

    # Style - striped rows
    employee_list.tag_configure("evenrows", background="honeydew")
    employee_list.tag_configure("oddrows", background="white")

    # Iterate through all employees to list them out.
    global count
    count = 0
    for emp in uvuEmpDat.emp_list:
        if count % 2 == 0:
            employee_list.insert('', END, values=(emp.id, emp.first_name, \
                                                  emp.last_name, emp.ssn, emp.phone, emp.email, \
                                                  emp.start_date, emp.end_date, \
                                                  str(emp.classification), \
                                                  emp.title, emp.dept), tags=("evenrows",))
        else:
            employee_list.insert('', END, values=(emp.id, emp.first_name, \
                                                  emp.last_name, emp.ssn, emp.phone, emp.email, \
                                                  emp.start_date, emp.end_date, \
                                                  str(emp.classification), \
                                                  emp.title, emp.dept), tags=("oddrows",))
        count += 1

    # Button frame on Admin list
    button_frame = Frame(admin_window)
    button_frame.pack(pady=0)
    # Report button
    report_button = Button(button_frame, text="Report",
                           command=prompt_report_all_employees)
    report_button.grid(row=0, column=0, padx=5, pady=5)

    def employee_selected(event):
        """Brings up an employee's information in a separate GUI window.
        Intended to be called with a double-click event handler, so that
        an employee's info shows up when you click on them.
        """
        # Bring up employee information after double-click
        for selected_emp_idx in employee_list.selection():
            emp_data = employee_list.item(selected_emp_idx)
            emp_id = emp_data["values"][0]
            emp = find_employee_by_id(emp_id, uvuEmpDat.emp_list)
            open_employee(emp, "admin")

    # Double-Click to bring up employee information
    employee_list.bind("<Double 1>", employee_selected)
    employee_list.grid(row=1, column=0, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(emp_frame, orient=VERTICAL, \
                              command=employee_list.yview)

    employee_list.config(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky="ns")

    # Run the window
    admin_window.mainloop()


def add_employee_screen():
    """Opens a screen for entering information to add a new user to the
    UVU Employee Database.
    """
    add_emp_window = Toplevel(admin_window)

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
            hourly_entry = Entry(add_emp_window, \
                                 textvariable=hourly_rate)
            hourly_entry.grid(row=6, column=4, padx=50,
                              pady=5)

        elif classification.get() == "Salary":
            # Field to set salary:
            global salary_label
            global salary_entry
            salary_label = Label(add_emp_window, text="Salary:")
            salary_label.grid(row=6, column=3, padx=25, pady=5)
            salary_entry = Entry(add_emp_window, textvariable=salary)
            salary_entry.grid(row=6, column=4, padx=50, pady=5)

        elif classification.get() == "Commissioned":
            # Field to set salary:
            global com_salary_label
            global com_salary_entry
            global commission_label
            global commission_entry
            com_salary_label = Label(add_emp_window, text="Salary:")
            com_salary_label.grid(row=6, column=3, padx=25, pady=5)
            com_salary_entry = Entry(add_emp_window, textvariable=salary)
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

    def validate_new_emp():
        """Creates a new employee with all of the given data members on
        the create employee GUI screen, after making sure the data in each
        field is valid.
        """
        # Initialize validity checker to False.
        valid = True

        emp_permission = permission.get()

        emp_pay_num = 0
        emp_route_num = 0
        emp_account_num = 0
        pay_method_str = pay_method.get()
        if pay_method_str == "Direct Deposit":
            emp_pay_num = 1

            emp_account_num = account_num.get()
            if re.search("^\d+-?\d+$", emp_account_num) is None:
                valid = False
                msg = f'Bank account number should be numeric, with one ' \
                      'dash allowed.'

            emp_route_num = route_num.get()
            if re.search("^\d+-?\d+-?\d+$", emp_route_num) is None:
                valid = False
                msg = f'Routing number should be numeric, with up to ' \
                      'two dashes allowed.'


        elif pay_method_str == "Mail":
            emp_pay_num = 2
        if emp_pay_num == 0:
            valid = False
            msg = f'You must select a payment method.'

        emp_class = None
        emp_class_str = classification.get()
        if emp_class_str == "Hourly":
            emp_hour_pay = hourly_rate.get()
            try:
                emp_hour_pay = float(emp_hour_pay)
                emp_class = create_classification(1, emp_hour_pay)
            except:
                valid = False
                emp_class = -1
                msg = f'Hourly pay must be a number, with 1 decimal ' \
                      'point allowed.'
        elif emp_class_str == "Salary":
            emp_salary = salary.get()
            try:
                emp_salary = float(emp_salary)
                emp_class = create_classification(2, emp_salary)
            except:
                valid = False
                emp_class = -1
                msg = f'Salary must be a number, with 1 decimal point ' \
                      'allowed.'
        elif emp_class_str == "Commissioned":
            emp_salary = salary.get()
            emp_com_rate = commission_rate.get()
            try:
                emp_salary = float(emp_salary)
                emp_com_rate = float(emp_com_rate)
                emp_class = create_classification(3, emp_salary, emp_com_rate)
            except:
                valid = False
                emp_class = -1
                msg = f'Salary and Commission rate must each be a ' \
                      'number, each with 1 decimal point allowed.'
        if emp_class == None:
            valid = False
            msg = f'You must select a classification type.'

        emp_pwd = password.get()
        if re.search(".+", emp_pwd) is None:
            valid = False
            msg = f'Password must not be empty.'

        emp_dept = dept.get()
        if re.search(".+", emp_dept) is None:
            valid = False
            msg = f'Employee department must not be empty.'

        emp_title = title.get()
        if re.search("^\w+.?\w+$", emp_title) is None:
            valid = False
            msg = f'Employee Title must have letters and numbers only, ' \
                  'with one special character in between characters ' \
                  'allowed.'

        emp_start_date = start_date.get()
        if re.search("^\d\d\/\d\d\/\d\d\d\d$", emp_start_date) is None \
                and re.search("^\d\d-\d\d-\d\d\d\d$", emp_start_date) is \
                None:
            valid = False
            msg = f'Start date must match the format: MM/DD/YYYY or ' \
                  'MM-DD-YYYY'

        emp_b_day = birth_date.get()
        if re.search("^\d\d\/\d\d\/\d\d\d\d$", emp_b_day) is None and \
                re.search("^\d\d-\d\d-\d\d\d\d$", emp_b_day) is None:
            valid = False
            msg = f'Birth date must match the format: MM/DD/YYYY or ' \
                  'MM-DD-YYYY'

        emp_zip = zip.get()
        if re.search("\d\d\d\d\d", emp_zip) is None:
            valid = False
            msg = f'Zip code must contain 5 consecutive digits.'

        emp_state = state.get()
        if re.search("^[A-Z][A-Z]$", emp_state) is None:
            valid = False
            msg = f'State must be a two-letter capital state code.'

        emp_city = city.get()
        if re.search("^[a-zA-Z]+[ -]*[a-zA-Z]+$", emp_city) is None:
            valid = False
            msg = f'City must have letters only, with one space or dash ' \
                  'allowed.'

        emp_address = address.get()
        if re.search("[a-zA-Z]", emp_address) is None or \
                re.search("[0-9]", emp_address) is None:
            valid = False
            msg = f'Address must have letters and numbers.'

        emp_email = email.get()
        if re.search("^.*\w.*@\w.*\.\w+$", emp_email) is None:
            valid = False
            msg = f'Email address is not valid.'

        emp_phone = phone.get()
        if re.search("^\(\d\d\d\) \d\d\d-\d\d\d\d$", emp_phone) is None \
                and re.search("^\d\d\d-\d\d\d-\d\d\d\d$", emp_phone) is \
                None and re.search("^\d\d\d\d\d\d\d\d\d\d$", emp_phone) \
                is None:
            valid = False
            msg = f'Phone number must match the format: (###) ###-#### ' \
                  'or ###-###-#### or ##########'

        emp_ssn = ssn.get()
        if re.search("^\d\d\d-\d\d-\d\d\d\d$", emp_ssn) is None and \
                re.search("^\d\d\d\d\d\d\d\d\d$", emp_ssn) is None:
            valid = False
            msg = f'SSN must match the format: ###-##-#### or ######### ' \
                  '(9 digits)'

        emp_l_name = last_name.get()
        if not emp_l_name.isalpha():
            valid = False
            msg = f'Last name must have letters only.'

        emp_f_name = first_name.get()
        if not emp_f_name.isalpha():
            valid = False
            msg = f'First name must have letters only.'

        if valid:
            add_new_employee(uvuEmpDat, new_id, emp_f_name, emp_l_name,
                             emp_address, emp_city, emp_state, emp_zip, emp_class,
                             emp_pay_num, emp_b_day, emp_ssn, emp_phone, emp_email,
                             emp_start_date, emp_title, emp_dept, emp_permission, emp_pwd,
                             emp_route_num, emp_account_num)

            add_emp_window.destroy()

            admin_window.update()
        else:
            validation_error(msg)

    max_id = 0
    for emp in uvuEmpDat.emp_list + uvuEmpDat.archived_list:
        if emp.id > max_id:
            max_id = emp.id

    new_id = max_id + 1

    # ID Entry:
    id_title = Label(add_emp_window, text="Employee ID:").grid(row=1,
                column=1, padx=25, pady=5)
    id_label = Label(add_emp_window, text=new_id).grid(row=1, column=2,
                padx=50, pady=5)

    # First name entry:
    first_name_label = Label(add_emp_window, text="First Name:")\
        .grid(row=2, column=1, padx=25, pady=5)
    first_name = StringVar(add_emp_window)
    id_first_name = Entry(add_emp_window, textvariable=first_name) \
        .grid(row=2, column=2, padx=50, pady=5)

    # Last name entry:
    last_name_label = Label(add_emp_window, text="Last Name:").grid(row=3,
                                                                    column=1, padx=25, pady=5)
    last_name = StringVar(add_emp_window)
    last_name_entry = Entry(add_emp_window, textvariable=last_name) \
        .grid(row=3, column=2, padx=50, pady=5)

    # Social security number entry:
    ssn_label = Label(add_emp_window, text="SSN:").grid(row=4,
                                                        column=1, padx=25, pady=5)
    ssn = StringVar(add_emp_window)
    ssn_entry = Entry(add_emp_window, textvariable=ssn) \
        .grid(row=4, column=2, padx=50, pady=5)

    # Phone entry:
    phone_label = Label(add_emp_window, text="Phone:").grid(row=5,
                                                            column=1, padx=25, pady=5)
    phone = StringVar(add_emp_window)
    phone_entry = Entry(add_emp_window, textvariable=phone) \
        .grid(row=5, column=2, padx=50, pady=5)

    # Email entry:
    email_label = Label(add_emp_window, text="Email:").grid(row=6,
                                                            column=1, padx=25, pady=5)
    email = StringVar(add_emp_window)
    email_entry = Entry(add_emp_window, textvariable=email) \
        .grid(row=6, column=2, padx=50, pady=5)

    # Address entry:
    address_label = Label(add_emp_window, text="Street Address:").grid(row=7,
                                                                       column=1, padx=25, pady=5)
    address = StringVar(add_emp_window)
    address_entry = Entry(add_emp_window, textvariable=address) \
        .grid(row=7, column=2, padx=50, pady=5)

    # City entry:
    city_label = Label(add_emp_window, text="City:").grid(row=8,
                                                          column=1, padx=25, pady=5)
    city = StringVar(add_emp_window)
    city_entry = Entry(add_emp_window, textvariable=city) \
        .grid(row=8, column=2, padx=50, pady=5)

    # State entry:
    state_label = Label(add_emp_window, text="State:").grid(row=9,
                                                            column=1, padx=25, pady=5)
    state = StringVar(add_emp_window)
    state_entry = Entry(add_emp_window, textvariable=state) \
        .grid(row=9, column=2, padx=50, pady=5)

    # Zip code entry:
    zip_label = Label(add_emp_window, text="Zip Code:").grid(row=10,
                                                             column=1, padx=25, pady=5)
    zip = StringVar(add_emp_window)
    zip_entry = Entry(add_emp_window, textvariable=zip) \
        .grid(row=10, column=2, padx=50, pady=5)

    # Birth date entry:
    birth_date_label = Label(add_emp_window, text="Birth Date:").grid(row=11,
                                                                      column=1, padx=25, pady=5)
    birth_date = StringVar(add_emp_window)
    birth_date_entry = Entry(add_emp_window, textvariable=birth_date) \
        .grid(row=11, column=2, padx=50, pady=5)

    # Start date entry:
    start_date_label = Label(add_emp_window, text="Start Date:").grid(row=1,
                                                                      column=3, padx=25, pady=5)
    start_date = StringVar(add_emp_window)
    start_date_entry = Entry(add_emp_window, textvariable=start_date) \
        .grid(row=1, column=4, padx=50, pady=5)

    # Title entry:
    title_label = Label(add_emp_window, text="Title:").grid(row=2,
                                                            column=3, padx=25, pady=5)
    title = StringVar(add_emp_window)
    title_entry = Entry(add_emp_window, textvariable=title) \
        .grid(row=2, column=4, padx=50, pady=5)

    # Dept entry:
    dept_label = Label(add_emp_window, text="Department:").grid(row=3,
                                                                column=3, padx=25, pady=5)
    dept = StringVar(add_emp_window)
    dept_entry = Entry(add_emp_window, textvariable=dept) \
        .grid(row=3, column=4, padx=50, pady=5)

    # Password entry:
    password_label = Label(add_emp_window, text="Password:").grid(row=4,
                                                                  column=3, padx=25, pady=5)
    password = StringVar(add_emp_window)
    password_entry = Entry(add_emp_window, textvariable=password) \
        .grid(row=4, column=4, padx=50, pady=5)

    # Classification entry:
    classification_label = Label(add_emp_window, text="Classification:") \
        .grid(row=5, column=3, padx=25, pady=5)
    classification = StringVar(add_emp_window)
    classification.set("Classification Type")
    class_drop = OptionMenu(add_emp_window, classification, "Hourly",
                            "Salary", "Commissioned").grid(row=5, column=4, padx=50, pady=5)
    classification.trace_add('write', generate_pay_fields)

    # PayMethod entry:
    method_label = Label(add_emp_window, text="Pay Method:") \
        .grid(row=8, column=3, padx=25, pady=5)
    pay_method = StringVar(add_emp_window)
    pay_method.set("Payment Method")
    method_drop = OptionMenu(add_emp_window, pay_method,
                             "Direct Deposit", "Mail").grid(row=8, column=4, padx=50, pady=5)
    pay_method.trace_add('write', generate_bank_fields)

    # Admin entry:
    permission_label = Label(add_emp_window, text="Permission Level:")
    permission_label.grid(row=11, column=3, padx=25, pady=5)
    permission = StringVar(add_emp_window)
    permission.set("admin")
    permission_drop = OptionMenu(add_emp_window, permission, "admin",
                                 "employee")
    permission_drop.grid(row=11, column=4, padx=50, pady=5)

    create_button = Button(add_emp_window, text="Create",
                           command=validate_new_emp).grid(row=12, column=4, padx=10,
                                                          pady=10)

    add_emp_window.mainloop()


def edit_employee_info(employee, fields, the_edit):
    """Generates a GUI window with information of the employee.
    Also generates an entry box and a button to update information, and
    allows the updating of employee info on the GUI.
    """
    def update_emp(fields):
        """Updates the employee's data members based on the given
        parameters.
        """
        # Initialize variable for validating user input.
        valid = True
        msg = ""

        # For payment method updates:
        if edit_type == 1:
            pay_method = new_info.get()
            if pay_method == "mail":
                uvuEmpDat.edit_employee(employee.id, fields, [2])
            elif pay_method == "direct deposit":
                fields += ["Route", "Account"]
                route_num = new_bank_routing.get()
                account_num = new_bank_account.get()
                if re.search("^\d+-?\d+$", account_num) is None:
                    valid = False
                    msg = f'Bank account number should be numeric, with one ' \
                        'dash allowed.'
                if re.search("^\d+-?\d+-?\d+$", route_num) is None:
                    valid = False
                    msg = f'Routing number should be numeric, with up to ' \
                        'two dashes allowed.'
                if valid:
                    uvuEmpDat.edit_employee(employee.id, fields, [1, route_num, account_num])
                    edit_window.destroy()
                else:
                    fields = fields[:1]
                    validation_error(msg)

        # For classification updates:
        elif edit_type == 2:
            new_classification = new_info.get()
            if new_classification == "hourly":
                fields += ["Hourly"]
                hourly_rate = new_hourly.get()
                try:
                    hourly_rate = float(hourly_rate)
                except:
                    valid = False
                    msg = f'Hourly Rate must be a number, with 1 decimal'\
                        f' point allowed.'
                if valid:
                    uvuEmpDat.edit_employee(employee.id, fields, [1, hourly_rate])
                    edit_window.destroy()
                else:
                    fields = fields[:1]
                    validation_error(msg)

            elif new_classification == "salary":
                fields += ["Salary"]
                salary = new_salary.get()
                try:
                    salary = float(salary)
                except:
                    valid = False
                    msg = f'Salary must be a number, with 1 decimal'\
                        f' point allowed.'
                if valid:
                    uvuEmpDat.edit_employee(employee.id, fields, [2, salary])
                else:
                    fields = fields[:1]
                    validation_error(msg)

            elif new_classification == "commissioned":
                fields += ["Salary", "Commission"]
                com_salary = new_com_salary.get()
                commission_rate = new_commission.get()
                try:
                    com_salary = float(com_salary)
                    commission_rate = float(commission_rate)
                except:
                    valid = False
                    msg = f'Salary and Commission rate must each be a '\
                        f'number, each with 1 decimal point allowed.'
                
                if valid:
                    uvuEmpDat.edit_employee(employee.id, fields, [3, com_salary, commission_rate])
                else:
                    fields = fields[:1]
                    validation_error(msg)

        # For permission updates:
        elif edit_type == 3:
            permission = new_info.get()
            if permission == "employee":
                uvuEmpDat.edit_employee(employee.id, fields, ["employee"])
            elif permission == "admin":
                uvuEmpDat.edit_employee(employee.id, fields, ["admin"])

        # For name updates:
        elif edit_type == 4:
            name = new_info.get()
            if not name.isalpha():
                valid = False
                msg = f'Name must use letters only.'
            if fields[0] == "First_Name":
                first_name = name
                last_name = employee.last_name
            elif fields[0] == "Last_Name":
                first_name = employee.first_name
                last_name = name
            full_name = f'{first_name} {last_name}'
            fields[0] = "Name"
            if valid:
                uvuEmpDat.edit_employee(employee.id, fields, [full_name])            
            else:
                fields = fields[:1]
                validation_error(msg)

        # For all other updates:
        elif edit_type == 5:
            uvuEmpDat.edit_employee(employee.id, fields, [new_info.get()])

    # Creates the edit window
    edit_window = Toplevel(login_window)
    # Initialize variable to keep track of edit type.
    edit_type = 0
    # Shows previous information before edit
    prev_info = Label(edit_window, text="Previous Information:  ").grid(row=0, column=0, padx=10, pady=10)
    edit_this = Label(edit_window, text=the_edit).grid(row=0, column=1, padx=10, pady=10)
    # Label what the entry box is for
    info_here_label = Label(edit_window, text="Enter new info here:  ").grid(row=1, column=0, padx=10, pady=10)
    # New Variables
    new_info = StringVar()
    new_bank_routing = StringVar()
    new_bank_account = StringVar()
    new_hourly = StringVar()
    new_salary = StringVar()
    new_com_salary = StringVar()
    new_commission = StringVar()
    # New information entry box
    if str(the_edit) == "direct deposit" or str(the_edit) == "mail":
        # Payment Method options
        edit_type = 1
        Radiobutton(edit_window, text="Mail", variable=new_info, value="mail").grid(row=1, column=1, padx=10, pady=10)
        Radiobutton(edit_window, text="Direct Deposit", variable=new_info, value="direct deposit").grid(row=2, column=1, padx=10, pady=10)
        label_bank_routing = Label(edit_window, text="Bank Routing Number: ").grid(row=3, column=1, padx=10, pady=10)
        updated_bank_routing = Entry(edit_window, textvariable=new_bank_routing).grid(row=3, column=2, padx=10, pady=10)
        label_bank_account = Label(edit_window, text="Bank Account Number: ").grid(row=4, column=1, padx=10, pady=10)
        updated_bank_account = Entry(edit_window, textvariable=new_bank_account).grid(row=4, column=2, padx=10, pady=10)
        update_button = Button(edit_window, text="Update Information", command=partial(update_emp, fields)).grid(row=6, columnspan=3,
                                                                                                padx=10, pady=10)   
    elif str(the_edit) ==  "hourly" or str(the_edit) ==  "salary" or str(the_edit) ==  "commissioned":
        # Classification options
        edit_type = 2
        Radiobutton(edit_window, text="Hourly", variable=new_info, value="hourly").grid(row=1, column=1, padx=10, pady=10)
        label_hourly = Label(edit_window, text="Hourly Pay Rate: ").grid(row=2, column=1, padx=10, pady=10)
        updated_hourly = Entry(edit_window, textvariable=new_hourly).grid(row=2, column=2, padx=10, pady=10)
        Radiobutton(edit_window, text="Salary", variable=new_info, value="salary").grid(row=3, column=1, padx=10, pady=10)
        label_salary = Label(edit_window, text="Salary: ").grid(row=4, column=1, padx=10, pady=10)        
        updated_salary = Entry(edit_window, textvariable=new_salary).grid(row=4, column=2, padx=10, pady=10)
        Radiobutton(edit_window, text="Commissioned", variable=new_info, value="commissioned").grid(row=5, column=1, padx=10, pady=10)
        label_com_salary = Label(edit_window, text="Salary: ").grid(row=6, column=1, padx=10, pady=10)        
        updated_com_salary = Entry(edit_window, textvariable=new_com_salary).grid(row=6, column=2, padx=10, pady=10)
        label_commissioned = Label(edit_window, text="Commission Pay Rate: ").grid(row=7, column=1, padx=10, pady=10)        
        updated_commissioned = Entry(edit_window, textvariable=new_commission).grid(row=7, column=2, padx=10, pady=10)
        update_button = Button(edit_window, text="Update Information", command=partial(update_emp, fields)).grid(row=8, columnspan=3,
                                                                                                        padx=10, pady=10)
    elif the_edit == "admin" or the_edit == "employee":
        # Permission options.
        edit_type = 3
        Radiobutton(edit_window, text="Employee", variable=new_info, value="employee").grid(row=1, column=1, padx=10, pady=10)
        Radiobutton(edit_window, text="Admin", variable=new_info, value="admin").grid(row=2, column=1, padx=10, pady=10)
        update_button = Button(edit_window, text="Update Information", command=partial(update_emp, fields)).grid(row=3, columnspan=3,
                                                                                                        padx=10, pady=10)

    else:
        # All other options
        if fields[0] == "First_Name" or fields[0] == "Last_Name":
            edit_type = 4
        else:
            edit_type = 5
        updated_info = Entry(edit_window, textvariable=new_info).grid(row=1, column=1, padx=10, pady=10)
        # Button to update information
        update_button = Button(edit_window, text="Update Information", command=partial(update_emp, fields)).grid(row=6, columnspan=3,
                                                                                                        padx=10, pady=10)


# Need to fill the fields for a single employee's data.
def open_employee(employee, permission_level):
    """Generates a GUI window populated with the data of the given
    employee. Also creates buttons to allow for editing an employee's data
    and printing a report for that employee. Will have a back button as
    well if permission_level is "admin".
    Input: Employee object, string.
    """
    # Employee Window
    employee_window = Toplevel(login_window)
    # Menu Bar of Employee Information screen
    menu_bar = Menu(employee_window)
    # Adds option of Edit to menu bar
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    # The sub-options under 'Edit' for all employees:
    edit_menu.add_command(label="Phone Number", command=lambda: edit_employee_info(employee, ["Phone"], employee.phone))
    edit_menu.add_command(label="Email", command=lambda: edit_employee_info(employee, ["Email"], employee.email))
    edit_menu.add_command(label="Street Address", command=lambda: edit_employee_info(employee, ["Address"], employee.address))
    edit_menu.add_command(label="City", command=lambda: edit_employee_info(employee, ["City"], employee.city))
    edit_menu.add_command(label="State", command=lambda: edit_employee_info(employee, ["State"], employee.state))
    edit_menu.add_command(label="Zip Code", command=lambda: edit_employee_info(employee, ["Zip"], employee.zip))
    edit_menu.add_command(label="Payment Method", command=lambda: edit_employee_info(employee, ["Pay_Method"], employee.pay_method))

    # Adds 'Edit' options
    file_menu.add_cascade(label="Edit", menu=edit_menu)
    # Puts in a line in the menu list
    file_menu.add_separator()
    # Option to close the file
    file_menu.add_command(label="Close All", command=button_close_warning)
    # Adds'File' options
    menu_bar.add_cascade(label="File", menu=file_menu)
    # Adds option of Help to menu bar
    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="Help", command=under_construction)
    help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # Adds the menu bar
    employee_window.config(menu=menu_bar)

    # Title of Login Window
    employee_window.title("UVU Employee Database")

    # Fonts
    title_font = "Arial 12 bold underline"
    label_font = "Arial 12"

    # Personal Information
    personal_info_title = Label(employee_window,
        text="Personal Information").grid(row=0, column=0, columnspan=2,
        padx=10, pady=10)
    # First Name
    first_name_title = Label(employee_window, text="First Name:")\
        .grid(row=1, column=0, padx=10, pady=15, sticky=E)
    first_name_label = Label(employee_window, text=employee.first_name)\
        .grid(row=1, column=1, padx=10, pady=10, sticky=W)
    # Last Name
    last_name_title = Label(employee_window, text="Last Name:")\
        .grid(row=2, column=0, padx=10, pady=15, sticky=E)
    last_name_label = Label(employee_window, text=employee.last_name)\
        .grid(row=2, column=1, padx=10, pady=15, sticky=W)
    # Social Security Number
    sss_title = Label(employee_window, text="Social Security Number:")\
        .grid(row=3, column=0, padx=10, pady=15, sticky=E)
    sss_label = Label(employee_window, text=employee.ssn).grid(row=3,
        column=1, padx=10, pady=15, sticky=W)
    # Phone Number
    phone_number_title = Label(employee_window, text="Phone Number:")\
        .grid(row=4, column=0, padx=10, pady=10, sticky=E)
    phone_number_label = Label(employee_window, text=employee.phone)\
        .grid(row=4, column=1, padx=10, pady=10, sticky=W)
    # Email
    email_title = Label(employee_window, text="Email:").grid(row=5,
        column=0, padx=10, pady=10, sticky=E)
    email_label = Label(employee_window, text=employee.email).grid(row=5,
        column=1, padx=10, pady=10, sticky=W)
    # Address
    address_title = Label(employee_window, text="Address:").grid(row=6,
        column=0, padx=10, pady=10, sticky=E)
    address_label = Label(employee_window, text=employee.address)\
        .grid(row=6, column=1, padx=10, pady=10, sticky=W)
    # City
    city_title = Label(employee_window, text="City:").grid(row=7,
        column=0, padx=10, pady=10, sticky=E)
    city_label = Label(employee_window, text=employee.city).grid(row=7,
        column=1, padx=10, pady=10, sticky=W)
    # State Initials
    state_title = Label(employee_window, text="State:").grid(row=8,
        column=0, padx=10, pady=10, sticky=E)
    state_label = Label(employee_window, text=employee.state).grid(row=8,
        column=1, padx=10, pady=10, sticky=W)
    # Zip Code
    zip_code_title = Label(employee_window, text="Zip Code:").grid(row=9,
        column=0, padx=10, pady=10, sticky=E)
    zip_code_label = Label(employee_window, text=employee.zip)\
        .grid(row=9, column=1, padx=10, pady=10, sticky=W)
    # Date of Birth
    birth_date_title = Label(employee_window, text="Date of Birth:")\
        .grid(row=10, column=0, padx=10, pady=10, sticky=E)
    birth_date_label = Label(employee_window, text=employee.birth_date)\
        .grid(row=10, column=1, padx=10, pady=10, sticky=W)
    # Password
    password_title = Label(employee_window, text="Password:").grid(row=11,
        column=0, padx=10, pady=10, sticky=E)
    password_label = Label(employee_window, text=employee.password)\
        .grid(row=11, column=1, padx=10, pady=10, sticky=W)

    # Employee Information
    employee_info_title = Label(employee_window,
        text="Employee Information").grid(row=0, column=3, columnspan=2,
        padx=10, pady=10)
    # Employee ID number
    emp_id_title = Label(employee_window, text="Employee ID:").grid(row=1,
        column=3, padx=10, pady=10, sticky=E)
    emp_id_label = Label(employee_window, text=employee.id).grid(row=1,
        column=4, padx=10, pady=10, sticky=W)
    # Job title
    job_title_title = Label(employee_window, text="Job Title:")\
        .grid(row=2, column=3, padx=10, pady=10, sticky=E)
    job_title_label = Label(employee_window, text=employee.title)\
        .grid(row=2, column=4, padx=10, pady=10, sticky=W)
    # Department
    department_title = Label(employee_window, text="Department:")\
        .grid(row=3, column=3, padx=10, pady=10, sticky=E)
    department_label = Label(employee_window, text=employee.dept)\
        .grid(row=3, column=4, padx=10, pady=10, sticky=W)
    # Start Date
    start_date_title = Label(employee_window, text="Start Date:")\
        .grid(row=4, column=3, padx=10, pady=10, sticky=E)
    start_date_label = Label(employee_window, text=employee.start_date)\
        .grid(row=4, column=4, padx=10, pady=10, sticky=W)
    # End Date
    end_date_title = Label(employee_window, text="End Date:").grid(row=5,
        column=3, padx=10, pady=10, sticky=E)
    end_date_label = Label(employee_window, text=employee.end_date)\
        .grid(row=5, column=4, padx=10, pady=10, sticky=W)

    # Payment Method
    payment_title = Label(employee_window, text="Payment Method:")\
        .grid(row=6, column=3, padx=10, pady=10, sticky=E)
    payment_label = Label(employee_window, text=str(employee.pay_method))\
        .grid(row=6, column=4, padx=10, pady=10, sticky=W)

    # Account and Routing Numbers, if employee uses direct deposit:
    if str(employee.pay_method) == "direct deposit":
        account_title = Label(employee_window, text="Account Number:")\
            .grid(row=7, column=3, padx=10, pady=10, sticky=E)
        account_label = Label(employee_window, text=str(employee.pay_method.account_num)) \
            .grid(row=7, column=4, padx=10, pady=10, sticky=W)

        routing_title = Label(employee_window, text="Routing Number:")\
            .grid(row=8, column=3, padx=10, pady=10, sticky=E)
        routing_label = Label(employee_window, text=employee.pay_method.route_num)\
            .grid(row=8, column=4, padx=10, pady=10, sticky=W)

    
    # Classification
    classification_title = Label(employee_window, text="Classification:")\
        .grid(row=9, column=3, padx=10, pady=10, sticky=E)
    classification_label = Label(employee_window,
        text=str(employee.classification)).grid(row=9, column=4,
        padx=10, pady=10, sticky=W)

    # Show pay amounts, based on classification type:
    if str(employee.classification) == "hourly":
        hourly_title = Label(employee_window, text="Hourly Rate:") \
            .grid(row=10, column=3, padx=10, pady=10, sticky=E)
        hourly_label = Label(employee_window, text=f'${employee.classification.hourly_rate:.2f}') \
            .grid(row=10, column=4, padx=10, pady=10, sticky=W)
    # Salary
    elif str(employee.classification) == "salary":
        salary_title = Label(employee_window, text="Salary:")\
            .grid(row=10, column=3, padx=10, pady=10, sticky=E)
        salary_label = Label(employee_window,
            text=f'${employee.classification.salary:.2f}').grid(row=10,
            column=4, padx=10, pady=10, sticky=W)
    # Commission
    elif str(employee.classification) == "commissioned":
        salary_title = Label(employee_window, text="Salary:") \
            .grid(row=10, column=3, padx=10, pady=10, sticky=E)
        salary_label = Label(employee_window,
            text=f'${employee.classification.salary:.2f}').grid(row=10,
            column=4, padx=10, pady=10, sticky=W)
        commission_title = Label(employee_window,
            text="Commission Rate:").grid(row=11, column=3, padx=10,
            pady=10, sticky=E)
        commission_label = Label(employee_window,
            text=f'${employee.classification.commission_rate:.2f}')\
                .grid(row=11, column=4, padx=10, pady=10, sticky=W)
    
    # Show permission/access level
    permission_title = Label(employee_window,
        text="Permission Level:").grid(row=12, column=3, padx=10,
        pady=10, sticky=E)
    permission_label = Label(employee_window,
        text=f'{employee.permission}').grid(row=12, column=4, padx=10,
        pady=10, sticky=W)

    # Buttons
    pay_stub_button = Button(employee_window, text="Get Pay Stub",
        command=partial(generate_pay_stub, employee)).grid(row=13,
        column=5, padx=10, pady=10)

    if permission_level == "admin":
        back_button = Button(employee_window, text="Back",
            command=partial(exit_window, employee_window)).grid(row=13,
            column=4, padx=10, pady=10)

        archive_button = Button(employee_window, text="Archive", command=
            partial(prompt_archive_employee, employee)).grid(row=13, column=0,
            padx=10, pady=10)

        # The sub-options under "Edit" for admin employees:
        edit_menu.add_command(label="First Name", command=lambda: edit_employee_info(employee, ["First_Name"], employee.first_name))
        edit_menu.add_command(label="Last Name", command=lambda: edit_employee_info(employee, ["Last_Name"], employee.last_name))
        edit_menu.add_command(label="Social Security Number", command=lambda: edit_employee_info(employee, ["SSN"], employee.ssn))
        edit_menu.add_command(label="Date of Birth", command=lambda: edit_employee_info(employee, ["Birth_Date"], employee.birth_date))
        edit_menu.add_command(label="Password", command=lambda: edit_employee_info(employee, ["Password"], employee.password))
        edit_menu.add_command(label="Job Title", command=lambda: edit_employee_info(employee, ["Title"], employee.title))
        edit_menu.add_command(label="Department", command=lambda: edit_employee_info(employee, ["Dept"], employee.dept))
        edit_menu.add_command(label="Start Date", command=lambda: edit_employee_info(employee, ["Start_Date"], employee.start_date))
        edit_menu.add_command(label="End Date", command=lambda: edit_employee_info(employee, ["End_Date"], employee.end_date))
        edit_menu.add_command(label="Classification", command=lambda: edit_employee_info(employee, ["Classification"], employee.classification))
        edit_menu.add_command(label="Permission", command=lambda: edit_employee_info(employee, ["Permission"], employee.permission))


def prompt_archive_employee(employee: Employee):
    """Generates a GUI prompt asking whether the user really wants to
    archive the empoloyee. Archives the employee if they say yes, and
    doesn't if they say no.
    """
    def archive_employee():
        """Captures the data for an employee's last day from the GUI
        last_day_screen, validates the data for the last day, then
        facilitates the archiving of the employee, if no errors.
        """
        valid = True
        msg = ""
        end = last_day.get()
        if re.search("^\d\d\/\d\d\/\d\d\d\d$", end) is None and\
            re.search("^\d\d-\d\d-\d\d\d\d$", end) is None:
            valid = False
            msg = f'End date must match the format: MM/DD/YYYY or ' \
                  'MM-DD-YYYY'
        if valid:
            employee.terminate_employee(end)
            uvuEmpDat.archive_employee(employee.id)
            last_day_screen.destroy()
        else:
            validation_error(msg)

    res = askyesno("Archive Employee", f'Are you sure you want to '\
                                       f'archive {employee.name}?\n'\
                                       f'This action is not easy to '\
                                       f'undo.')
    if res == True:
        last_day_screen = Toplevel(login_window)
        last_day = StringVar(last_day_screen)
        last_day_prompt = Label(last_day_screen,
            text=f'When was {employee.name}\'s last day?').grid(row=0,
            column=0, padx=10, pady=10)
        last_day_title = Label(last_day_screen, text="Last Day:")\
            .grid(row=1, column=0, padx=10, pady=10)
        last_day_entry = Entry(last_day_screen, textvariable=last_day)\
            .grid(row=1, column=1, padx=10, pady=10)
        submit_button = Button(last_day_screen, text="Submit",
            command=archive_employee).grid(row=2,
            column=1, padx=10, pady=10)
    else:
        pass


def prompt_report_all_employees():
    """Generates a GUI prompt asking whether the user wants to include
    archived employees in the report, and generates the proper report
    based on the user's response. Also allows user to click a cancel
    button to close the window without generating a report.
    """
    res = askyesno("Employee Report", "Do you want to include archived employees in the report?")
    if res == True:
        generate_report_all_employees(True)
    else:
        generate_report_all_employees(False)

def open_report_window():
    report_window = Toplevel(login_window)
    report_window.geometry("1475x700")
    # Create Textbox for report data
    report_text = Text(report_window, width=120, height=100)
    # Add report data to textbox
    with open("report.csv", 'r') as file:
        the_report = file.read()
        report_text.insert("1.0", the_report)
    report_text.pack(side=LEFT)
    report_text.config(state='disabled')

    # Scrollbar
    report_scrollbar = Scrollbar(report_window)
    report_scrollbar.pack(side=RIGHT, fill=Y)
    
    # Attach scrollbar to textbox
    report_text.config(yscrollcommand=report_scrollbar.set)
    report_scrollbar.config(command=report_text.yview)
    
    report_window.mainloop()

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
    else:  # Otherwise emp_list will be all non-archived employees (from
        #   EmployeeDatabase.database).
        emp_list = uvuEmpDat.emp_list

    read_timecards()
    read_receipts()
    string = ""
    msg = "A report has been saved to 'report.csv' as well.\n"\
        "All Employee Report:\n\n"

    with open("report.csv", "w") as report:
        for employee in emp_list:
            # Write a line to "report.csv" that reports on all data
            #   members for the employee.
            if str(employee.classification) == "hourly":
                if str(employee.pay_method) == "direct deposit":
                    string = f"Employee ID: {employee.id}       Name: "\
                        f"{employee.name}         Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification}    "\
                        f"Hourly pay: "\
                        f"${employee.classification.hourly_rate:.2f}    "\
                        f"   Payment method: {employee.pay_method}\n"\
                        f"Routing num: {employee.pay_method.route_num}  "\
                        f" Account num: "\
                        f"{employee.pay_method.account_num} Date of "\
                        f"birth: {employee.birth_date}\n"\
                        f"SSN: {employee.ssn}          Phone: "\
                        f"{employee.phone}     Email: {employee.email}\n"\
                        f"Start date: {employee.start_date}     "\
                        f"End date: {employee.end_date}\n"\
                        f"Title: {employee.title}           Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission}   "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
                elif str(employee.pay_method) == "mail":
                    string = f"Employee ID: {employee.id}        Name: "\
                        f"{employee.name}   Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification}     "\
                        f"Hourly pay: "\
                        f"${employee.classification.hourly_rate:.2f}    "\
                        f"   Payment method: {employee.pay_method}\n"\
                        f"Date of birth: {employee.birth_date}  SSN: "\
                        f"{employee.ssn}\n"\
                        f"Phone: {employee.phone}       Email: "\
                        f"{employee.email}\n"\
                        f"Start date: {employee.start_date}       End "\
                        f"date: {employee.end_date}\n"\
                        f"Title: {employee.title}      Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission} "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
            elif str(employee.classification) == "salary":
                if str(employee.pay_method) == "direct deposit":
                    string = f"Employee ID: {employee.id}        Name: "\
                        f"{employee.name}      Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification}     "\
                        f"Salary: ${employee.classification.salary:.2f} "\
                        f"   Payment method: {employee.pay_method}\n"\
                        f"Routing number: "\
                        f"{employee.pay_method.route_num} "\
                        f"Account number: "\
                        f"{employee.pay_method.account_num}    Date of "\
                        f"birth: {employee.birth_date}\n"\
                        f"SSN: {employee.ssn}           Phone: "\
                        f"{employee.phone}    Email: {employee.email}\n"\
                        f"Start date: {employee.start_date}       End "\
                        f"date: {employee.end_date}\n"\
                        f"Title: {employee.title}           Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission}    "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
                elif str(employee.pay_method) == "mail":
                    string = f"Employee ID: {employee.id}      Name: "\
                        f"{employee.name}    Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification}   "\
                        f"Salary: ${employee.classification.salary:.2f} "\
                        f"      Payment method: {employee.pay_method}\n"\
                        f"Date of birth: {employee.birth_date} SSN: "\
                        f"{employee.ssn}\n"\
                        f"Phone: {employee.phone}     Email: "\
                        f"{employee.email}\n"\
                        f"Start date: {employee.start_date}     End "\
                        f"date: {employee.end_date}\n"\
                        f"Title: {employee.title}           Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission}  "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
            elif str(employee.classification) == "commissioned":
                if str(employee.pay_method) == "direct deposit":
                    string = f"Employee ID: {employee.id}             "\
                        f"Name: {employee.name}      Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification}    "\
                        f"Salary: ${employee.classification.salary:.2f} "\
                        f"         Commission rate: "\
                        f"${employee.classification.commission_rate:.2f}"\
                        f"\n"\
                        f"Payment method: {employee.pay_method}  Routing"\
                        f" number: {employee.pay_method.route_num} "\
                        f"Account number: "\
                        f"{employee.pay_method.account_num}\n"\
                        f"Date of birth: {employee.birth_date}        "\
                        f"SSN: {employee.ssn}           Phone: "\
                        f"{employee.phone}\n"\
                        f"Email: {employee.email}    Start date: "\
                        f"{employee.start_date}      End date: "\
                        f"{employee.end_date}\n"\
                        f"Title: {employee.title}         Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission}      "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
                elif str(employee.pay_method) == "mail":
                    string = f"Employee ID: {employee.id}          Name:"\
                        f" {employee.name}    Address: "\
                        f"{employee.full_address()}\n"\
                        f"Classification: {employee.classification} "\
                        f"Salary: ${employee.classification.salary:.2f} "\
                        f"       Commission rate: "\
                        f"${employee.classification.commission_rate:.2f}"\
                        f"\n"\
                        f"Payment method: {employee.pay_method}         "\
                        f"Date of birth: {employee.birth_date}\n"\
                        f"SSN: {employee.ssn}             Phone: "\
                        f"{employee.phone}     Email: {employee.email}\n"\
                        f"Start date: {employee.start_date}        End "\
                        f"date: {employee.end_date}\n"\
                        f"Title: {employee.title}               Dept: "\
                        f"{employee.dept}\n"\
                        f"Permission level: {employee.permission}      "\
                        f"Password: {employee.password}\n\n"
                    report.write(string)
            
            # Save message for report GUI.
            msg += string
            
            # Write a line to "report.csv" stating what the employee will
            #   be paid.
            pay_report = employee.payment_report()
            report.write(f"\t{pay_report}\n\n\n")
    # Opens the report in a GUI window
    open_report_window()

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
        with open(f'{employee.last_name.lower()}_{employee.first_name.lower()}_pay_stub.csv', 'w') as pay_file:
            pay_file.write(
                f'{name_message}\n'
                f'{rate_message_1}\n'
                f'{rate_message_2}\n'
                f'{pay_message}\n'
            )

    def pay_stub_screen(name_message, pay_message, rate_message_1,
                        rate_message_2):  # If we don't use this function, bypass
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
        name_label = Label(pay_stub_window, text=name_message) \
            .grid(row=1, column=0, padx=10, pady=10)
        rate_1_label = Label(pay_stub_window, text=rate_message_1) \
            .grid(row=2, column=0, padx=10, pady=10)
        rate_2_label = Label(pay_stub_window, text=rate_message_2) \
            .grid(row=3, column=0, padx=10, pady=10)
        pay_message_label = Label(pay_stub_window, text=pay_message) \
            .grid(row=5, column=0, padx=10, pady=10)

        export_button = Button(pay_stub_window, text="Export to CSV",
                               command=partial(export_pay_stub_csv, name_message, pay_message,
                                    rate_message_1, rate_message_2)).grid(row=7, column=3,
                                    padx=10, pady=10)

        pay_stub_window.mainloop()

    pay_date = ""  # Not sure if this will be used.
    pay_num = 0  # For storing hours or commissions.
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
                if str(employee.pay_method) == "direct deposit":
                    pay_message = f"Transferred ${pay_amount} for {employee.name} to {employee.pay_method.route_num} at {employee.pay_method.account_num}."
                elif str(employee.pay_method) == "mail":
                    pay_message = f"Mailed ${pay_amount} to {employee.name} at {employee.full_address()}."
                rate_message_1 = ""
                rate_message_2 = ""
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


def validation_error(msg):
    """Displays an error message when a user enters invalid data into the
    database, and tries to save it. Displays the given message. 
    """
    showinfo("Invalid Entry", msg, icon=WARNING)


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
    # Prompt warning about to close program
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


# Login Window functionality. Global so that all functions can access it.
login_window = Tk()
login_window.update()
# Menu Bar of Login screen
menu_bar = Menu(login_window)
# Adds option of File to menu bar
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Close All", command=button_close_warning)
menu_bar.add_cascade(label="File", menu=file_menu)
# Adds option of Help to menu bar
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help", command=under_construction)
help_menu.add_command(label="Read Me", command=lambda: open_file("readme.txt"))
menu_bar.add_cascade(label="Help", menu=help_menu)
# Adds the menu bar
login_window.config(menu=menu_bar)

# Size of Login Window
login_window.geometry("515x360")
# Title of Login Window
login_window.title("UVU Employee Database")
# Login Window Name
login_window_label = Label(login_window, text="Login").grid(row=1, \
                                                            columnspan=3, padx=50, pady=50)

# User ID Text
user_id_label = Label(login_window, text="User ID").grid(row=2, \
                                                         column=1, padx=25, pady=5)
# User ID Textbox
user_id = StringVar(login_window)
user_id_entry = Entry(login_window, textvariable=user_id) \
    .grid(row=2, column=2, padx=50, pady=5)

# Password Text
password_label = Label(login_window, text="Password").grid(row=3, \
                                                           column=1, padx=25, pady=5)
# Password Textbox
password = StringVar(login_window)
password_entry = Entry(login_window, textvariable=password, show='*') \
    .grid(row=3, column=2, padx=5, pady=5)

# Login Button
login_button = Button(login_window, text="Login", \
                      command=login).grid(row=4, column=2, padx=25, pady=25)

# Close Button
exit_button = Button(login_window, text="Close", \
                     command=button_close_warning).grid(row=5, column=4, padx=5, pady=5)


def main():
    """Starts up the entire application, starting with the login screen.
    """
    # Run the window
    login_window.mainloop()


if __name__ == "__main__":
    main()