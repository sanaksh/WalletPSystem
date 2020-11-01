# Connect Python to SQL Server using pyodbc and rendering data using Flask

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
	
# Web pages:
There are few webpages which are already there. You can make your own html pages and save them under templates directory and make an app route for that.

# Database:
You can deploy databse either on windows or linux.
Note: If you wish to install on linux you need Ubuntu 18.04 LTS.
For Deployment on linux visit https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver15

# Starting Flask Server:
	python3 api.py
	
# Note:
Pyodbc is python module which runs only on Windows operating system or Windows Datacenter server.
This project is tested on Windows server 2019 and Windows 10.

# Credits:
https://thedevashish.in
