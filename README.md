# Hindalco-Renusagar-Monthly-MIS

------------


There are two types of the login:-
1. Admin Login
1. Master Admin (E-Mail - admin Password - admin)
1. Department Admin (Created By Master Admin)
1. User Login (Created By Master Admin)

Master Admin has the following function:-
1. Export CSV To E-Mail 
Complete MIS can mail to admin using the SMTP protocol
1. Display Indicator 
Display complete MIS of all the admin
1. Add Admin 
Made admin to the available user.
1. Add User 
Here new E-Mail ID and password is created.
1. Update Password
Update Password of the available user.

Department Admin has the following function:-
1. Export CSV to E-Mail
1. Add User
Add MIS user
1. Add Indicator
Add indicator of MIS user
1. Display Indicator

MIS Admin has the following function:-
1. Update Data
Here User can update the given indicator of the particular month
1. Display Indicor

------------



MySQL Command to create database and table
-------------

    CREATE DATABASE it_employee;
    
    CREATE TABLE user_login(
      username varchar(255),
      password varchar(255)
    );
    
    CREATE TABLE add_action(
      username varchar(255),
      action varchar(255),
      unit varchar(255),
      target varchar(255),
      january varchar(255),
      february varchar(255),
      march varchar(255),
      april varchar(255),
      may varchar(255),
      june varchar(255),
      july varchar(255),
      august varchar(255),
      september varchar(255),
      october varchar(255),
      november varchar(255),
      december varchar(255),
      Owner varchar(255)
    );
    
    CREATE TABLE admin(
      username varchar(255)
    );
    
    CREATE TABLE user(
      owner varchar(255),
      username varchar(255) 
    );
-------------
Python Libary required -
-------------
    pip install python-csv
    pip install mime
    pip install smtplib
    pip install email-to
    pip install Flask
-------------
**Main Login Page**

![Main Login Page](/image/Main%20Login%20Page.jpg "Main Login Page")

**Master Admin Dashboard**

![Main Login Page](/image/Master%20Admin%20Dashboard.jpg "Master Admin Dashboard")

**Display Indicator**

![Display Indicator](/image/Display%20Indicator.jpg "Display Indicator")

**Add Admin**

![add admin](/image/add%20admin.jpg "add admin")

**Add User**

![add user](/image/add%20user.jpg "add user")

**Update Password**

![update password](/image/update%20password.jpg "update password")

**Department Admin Page**

![Department Admin Page](/image/Department%20Admin%20Page.jpg "Department Admin Page")

**Add MIS User**

![add mis user](/image/add%20mis%20user.jpg "add mis user")
add mis user

**Add MIS User Indicator**

![add mis user indicator](/image/add%20mis%20user%20indicator.jpg "add mis user indicator")
add mis user

**User Dashboard**

![user Dashboard](/image/user%20Dashboard.jpg "user Dashboard")

**user update data**

![user update data](/image/user%20update%20data%201.jpg "user update data")

**user update data**

![user update data](/image/user%20update%20data%202.jpg "user update data")
