
# Wallet Payment System

# Woking of the Project

The aim of the project at this phase is to design a database system for the wallet payment network that has all the tables needed and able to select, view, and manipulate data as required, satisfying the conditions set at the beginning of the project. The database has tables with primary and foreign keys, designated based on the ER diagram and the relational schema designed and delivered in the previous phases of the project respectively. It is ensured that the basic functionalities such as sending and receiving money are promptly implemented with possibility of aggregating transactions. 

The project back-end has been implemented with SQL Server Management Studio of Microsoft that has capabilities to work on MSSQL. The front-end UI design has been implemented with Python Flask framework. 


# Pre-requirements:
Install python3 and pip3
(This project is tested on Python 3.8)

# Install modules using pip:
	pip install pyodbc
	pip install flask
	pip install pandas

# Quickstart:
# Fill the following details in api.py file: 
	server = '' 
	database = '' 
	username = '' 
	password = ''

## Mac/Linux

1. Install ODBC Driver 17 for SQL Server
2. Create virtual env with python 3.6: `virtualenv venv --python=python3.6` and activate it using: `source venv/bin/activate`
3. Run `python api.py`

## Windows

1. Install ODBC Driver 17 for SQL Server (https://www.microsoft.com/en-us/download/details.aspx?id=56567)
2. Create virtual env with python 3.6: `virtualenv venv`
3. Activate virtual env: `venv\Scripts\activate.bat`
4. Run `python api.py`

# Web pages:
There are few webpages which are already there. You can make your own html pages and save them under templates directory and make an app route for that.

# Database:
You can deploy databse either on windows or linux.
Note: If you wish to install on linux you need Ubuntu 18.04 LTS.
For Deployment on linux visit https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver15

# Starting Flask Server:
	python3 api.py

# Credits:
Devashish Upadhyay
https://thedevashish.in
