import os
import csv


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


def create_classification(class_num, pay_num_1, pay_num_2=0):
    """Creates an Hourly, Salary, or Commissioned class object based on
    the class_num, and assigns the proper data members.

    Input: pay_num_1 - a float representing hourly pay or salary,
                depending on the employee's classification.
           pay_num_2 - a float representing commissioned pay rate, used
                only for commissioned employees (class_num = 3).

    Output: Either an Hourly, Salary, or Commissioned class object.
    """
    if class_num == 1:
        return Hourly(pay_num_1)
    elif class_num == 2:
        return Salary(pay_num_1)
    elif class_num == 3:
        return Commissioned(pay_num_1, pay_num_2)
    else:
        raise Exception(f'Invalid classification number {class_num}. Should be 1, 2, or 3.')


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


def create_pay_method(employee, pay_method_num, route_num=0,
                      account_num=0):
    """Creates an DirectMethod or MailedMethod class object based on the
    pay_method_num, and assigns the proper data members.

    Input: employee - an employee class object that the pay method will be
                tied to.
           route_num - a string representing the employee's bank routing
                number, used only if they're using DirectMethod
                (pay_method_num = 1).
           account_num - a string representing the employee's account
                number, used only if they're using DirectMethod
                (pay_method_num = 1).

    Output: Either a DirectMethod or MailedMethod class object.
    """
    if pay_method_num == 1:
        return DirectMethod(employee, route_num, account_num)
    elif pay_method_num == 2:
        return MailedMethod(employee)
    else:
        raise Exception(f'Invalid pay method number {pay_method_num}. Should be 1 or 2.')


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

    def __init__(self, id, name, classification, birth_date, SSN, phone,
                 email, permission, password):
        """Initializes the employee object with basic data members.
        """
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
        self.birth_date = birth_date
        self.ssn = SSN
        self.phone = phone
        self.email = email
        self.start_date = None
        self.end_date = None
        self.title = None
        self.dept = None
        self.permission = permission
        self.password = password

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
            emp = Employee(None, None, None, None, None, None, None, None,
                           None)
            emp.populate_from_row(row)
            self.archived_list.append(emp)
        empDict = csv.DictReader(self.db)
        for row in empDict:
            emp = Employee(None, None, None, None, None, None, None, None,
                           None)
            emp.populate_from_row(row)
            if emp not in self.archived_list:
                self.emp_list.append(emp)

    def _add_row(self, emp: Employee, file):
        with open(file, "a") as DB:
            writer = csv.writer(DB, delimiter=',')
            if str(emp.classification) == "hourly":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(), -1,
                                     emp.classification.hourly_rate, -1,
                                     emp.pay_method.route_num,
                                     emp.pay_method.account_num, emp.birth_date,
                                     emp.ssn, emp.phone, emp.email, emp.start_date,
                                     emp.end_date, emp.title, emp.dept,
                                     emp.permission, emp.password])
                elif str(emp.pay_method) == "mail":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(), -1,
                                     emp.classification.hourly_rate, -1, -1, -1,
                                     emp.birth_date, emp.ssn, emp.phone, emp.email,
                                     emp.start_date, emp.end_date, emp.title,
                                     emp.dept, emp.permission, emp.password])
            elif str(emp.classification) == "salary":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(),
                                     emp.classification.salary, -1, -1,
                                     emp.pay_method.route_num,
                                     emp.pay_method.account_num, emp.birth_date,
                                     emp.ssn, emp.phone, emp.email, emp.start_date,
                                     emp.end_date, emp.title, emp.dept,
                                     emp.permission, emp.password])
                elif str(emp.pay_method) == "mail":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(),
                                     emp.classification.salary, -1, -1, -1, -1,
                                     emp.birth_date, emp.ssn, emp.phone, emp.email,
                                     emp.start_date, emp.end_date, emp.title,
                                     emp.dept, emp.permission, emp.password])
            elif str(emp.classification) == "commissioned":
                if str(emp.pay_method) == "direct deposit":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(),
                                     emp.classification.salary, -1,
                                     emp.classification.commission_rate,
                                     emp.pay_method.route_num,
                                     emp.pay_method.account_num, emp.birth_date,
                                     emp.ssn, emp.phone, emp.email, emp.start_date,
                                     emp.end_date, emp.title, emp.dept,
                                     emp.permission, emp.password])
                elif str(emp.pay_method) == "mail":
                    writer.writerow([emp.id, emp.name, emp.address,
                                     emp.city, emp.state, emp.zip,
                                     emp.classification.num(),
                                     emp.pay_method.num(),
                                     emp.classification.salary, -1,
                                     emp.classification.commission_rate, -1, -1,
                                     emp.birth_date, emp.ssn, emp.phone, emp.email,
                                     emp.start_date, emp.end_date, emp.title,
                                     emp.dept, emp.permission, emp.password])

    def archive_employee(self, id):
        """Removes from emp list and adds them to the archived file.
        """
        emp = find_employee_by_id(id, self.emp_list)
        self.emp_list.remove(emp)
        self._add_row(emp, "archived.csv")

    def add_employee(self, employee: Employee):
        self.emp_list.append(employee)
        self._add_row(employee, "employees.csv")


def add_new_employee(empDB: EmployeeDB, id, first_name, last_name,
                     address, city, state, zip, classification, pay_method_num, birth_date,
                     SSN, phone, email, start_date, title, dept, permission, password,
                     route_num=0, account_num=0):
    """Creates a new employee from given all of the necessary data, and
    adds that employee to the database, and writes them to the
    database file.
    """
    name = f'{first_name} {last_name}'
    employee = Employee(id, name, classification, birth_date,
                        SSN, phone, email, permission, password)

    employee.set_address(address, city, state, zip)
    employee.set_job(start_date, title, dept)
    employee.set_pay_method(pay_method_num, route_num, account_num)

    empDB.add_employee(employee)


def open_file(the_file):
    """Function to open a file"""
    os.system(the_file)





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