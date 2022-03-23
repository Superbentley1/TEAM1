Sprint 4 readme:

To open the UVU Employee Database, simply run the UVU_EmpDat.py file,
making sure that it is in the same directory as all of the other UVU
database files ("employees.csv", "timecards.csv", etc.).

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
top, and go to file -> edit -> where you can select data members to edit.
Currently the edit options don't actually edit the database. We plan to
have that working as soon as possible. Regular employees will only be able
to edit a few data members, which has not yet been implemented.

If you log in as an admin user, you will see the admin employee list, that
lists out all employees. If you click file -> new, it brings up a screen
to create a new employee. This option is not yet functional, and doesn't
add users to the database. We plan to have this working by Sprint 5. If you
click file -> Close All, it will close the program.

From the admin employee list, if you double-click on an employee, it will
open that employee's data screen. This is similar to the employee view of
their data, except that there is also a "Back" button that closes the
employee data screen, and an "All Emps Report" button that generates a
report of all employee information, including their pay, called
"report.csv". By Sprint 5 we plan to have a GUI screen for this report as
well. We plan to move this button to the admin employee list screen when
we are able, instead of on the employee data screen.

Generating an employee's pay stub won't be functional until the "All Emps
Report" has been run, because pay stubs are based off of previous pay, and
not future pay.

At any time, you can click "Help" on top menu. The Help -> Read Me option
will open this readme message. The Help -> Help option will have a user
guide there in a future sprint. Neither option is currently functional,
but will should be working in future Sprints (Sprint 5 for the readme
file).

Thank you for your time!

