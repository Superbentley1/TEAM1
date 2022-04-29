Sprint 6 readme:

To open the UVU Employee Database, simply run the Main_UVU.py file,
making sure that it is in the same directory as all of the other UVU
database files ("employee_database.py", "employees.csv", "timecards.csv",
etc.).

Upon running the program to open the database, you will see the login
screen. Enter one of the following sets of user ID and password to log in
(or any other user ID and password from "employees.csv"):

For admin access:
User ID: 502141
Password: V6ygCWaaD

For regular employee access:
User ID: 939825
Password: EaQ^mej6`

If you log in as a regular employee, you will see the employee data screen
that will show just that employee's data. You will have the option to view
a pay stub for that employee, and if you view the pay stub, you can also
click "Export to CSV", and it will create a .csv file in your current
directory named using the employee's name.

From the employee data screen, you can also click the "File" option at the
top, and go to file -> edit -> where you can select data members you want
to edit. Regular employees are only able to edit a few of their data
members. Once you have edited employee data, you can click "Refresh" to
view the saved changes that you have made to the data on that screen.

On any screen in the UVU Employee Database, if you click file -> Close
All, it will close the program.

If you log in as an admin user, you will see the admin employee list, that
lists out all employees. On the bottom of the admin employee list, there
is a search bar. You can search for an employee by name by typing their
first or last name in the search bar, and clicking "Search". To bring back
the full employee list, click "Refresh".

On the bottom of the admin employee list, there is also a button that says
"Report." If you click on this button, a screen will pop up with a report
of all employees and what they will be payed in their next paychecks, and
a report file called "report.csv" is generated with the same report.

If you click file -> new, it brings up a screen to create a new employee.
Fill in all of the fields there and select from all drop-down boxes, then
click "Create" to create a new employee in the database.

From the admin employee list, if you double-click on an employee, it will
open that employee's data screen. This is similar to the employee view of
their data, except that there is also a "Back" button that closes the
employee data screen, an "Archive" button that allows you to archive the
employee if they no longer work at UVU, and that when you go to
File -> Edit, you are able to edit more employee data members than regular
employees can (all data members except for employee ID).

Generating an employee's pay stub won't be functional unless the
"report.csv" file is in the same directory as Main_UVU.py. If the file is
not there, then simply click the "Report" button on the admin employee
list screen and "report.csv" will be generated. This is required because
pay stubs are based off of pay from the previous pay period, and not the
current pay period.

At any time, you can click "Help" on top menu. The Help -> Read Me option
will open this readme message. The Help -> Help option will open the User
Manual on how to use this product. 

Thank you for your time!
