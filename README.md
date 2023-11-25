# Invoice-Management-System-DBMS
An invoice management system built for the Database Management Systems course using MySQL, Python (Flask), HTML and CSS

### To Create Database and Tables:
Run the database_setup_new.sql file to create the database tables and additional requirements (triggers, procedures etc.) using MySQL Workbench. 
If re-running the database_setup_new.sql file later for some changes, ensure to drop the existing database before running the file. Else, add "CREATE IF NOT EXISTS" constraints to all create statements in the file. 

### To Run main app.py file:
cd to the directry containing the invoice_management app.py file, and run it using "python app.py". 
Make sure to change the database connection password in the app.py file to your database password before running.
