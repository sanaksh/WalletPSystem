# Connect Python to SQL Server using pyodbc and rendering data into HTML using Flask
# Woking of the Project
![alt text](https://github.com/devashishupadhyay/Sql-Server-Flask/blob/main/working.jpg?raw=true)
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
