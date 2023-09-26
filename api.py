##libraries
import os
from IPython.display import HTML
import flask
from datetime import datetime, timezone
import pyodbc
import pandas as pd
import numpy as np
import json
from flask import jsonify, request
from flask import Flask, render_template, redirect, url_for, request, session, flash
import time
import random
from datetime import datetime

###database connectioon
server = 'DESKTOP-DF44E9B\SQLEXPRESS' 
database = 'WalletDB' 
print("connecting.......")
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
cursor = cnxn.cursor()
print("connected!")

##flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "my precious"
## routes to each webpage

# @app.route('/login')
# def login():
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        SSN = request.form['SSN']

        # # Connect to the SQL Server database
        # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server_name;DATABASE=your_database_name;UID=your_username;PWD=your_password')
        # cursor = conn.cursor()

        # Execute a SQL query to check if the email and password match
        query = "SELECT * FROM User_Account WHERE SSN = ? AND PBAVerified = 1"
        user = cursor.execute(query, (SSN))
        acc = user.fetchone()

        # If there is a match, redirect to the account page
        if acc:
            session['loggedin'] = True
            session['id'] = acc[0]
            session['email'] = acc[1]
            # Redirect to home page
            return redirect('/account')

        # If there is no match, show an error message
        else:
            error_message = 'Invalid SSN'
            return render_template('login.html', error=error_message)

    # If the request method is GET, show the login page
    else:
        return render_template('login.html')
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']

    #     # Connect to the SQL Server database
    #     conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server_name;DATABASE=your_database_name;UID=your_username;PWD=your_password')
    #     cursor = conn.cursor()

    #     # Execute a SQL query to check if the email and password match
    #     query = "SELECT * FROM Users WHERE email = ? AND password = ?"
    #     cursor.execute(query, (email, password))

    #     # If there is a match, redirect to the account page
    #     if cursor.fetchone():
    #         return redirect('/account')

    #     # If there is no match, show an error message
    # else:
    #     error_message = 'Invalid email or password'
    #     return render_template('login.html', error=error_message)

    # # If the request method is GET, show the login page

@app.route('/account')
def account():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        
        user_id = session['id']
        user = cursor.execute("SELECT * FROM User_Account WHERE SSN = ?", (user_id,)).fetchone()
        return render_template('account.html',  name=user[1] , balance=user[3], ssn=user[0])
    else:
        flash('You must log in first')
        return redirect(url_for('login'))
    #

@app.route('/sendmoney', methods=['GET', 'POST'])
def sendmoney():
    if request.method == 'POST':
        # Get form data
        # first_name = request.form['first_name']
        # last_name = request.form['last_name']
        email = request.form['email']

        # account_type = request.form['account_type']
        # if account_type == 'Other':
        #     account_number = request.form['account_number']
        # else:
        #     account_number = None
        amount = request.form['amount']
        memo = request.form['memo']

        # Process form data and send money
        if 'loggedin' in session:
            user_id = session['id']
            receiver_ssn = cursor.execute("SELECT * FROM Email WHERE EmailAdd = ? ", (email))
            rec = cursor.fetchone()

            if rec is None:
                flash('Receiver with provided email/phone does not exist')
                return redirect('/account')

            sender = cursor.execute("UPDATE User_Account SET balance = balance - ? WHERE ssn = ?", (amount, user_id))
            receiver = cursor.execute("UPDATE User_Account SET balance = balance + ? WHERE ssn = ?", (amount, rec[1]))
            transaction_id = random.randint(1000, 9999)
            now = datetime.now()
            Date = now.strftime("%Y-%m-%d %H:%M:%S")

            # Save the transaction details to a new table
            cursor.execute("INSERT INTO SEND_TRANSACTION (STid, Amount, date_time, Memo,cancel_reason, SSN, Identifier) VALUES (?, ?, ?, ?, ? ,?, ?)",
                           (transaction_id, amount, now, memo, None, user_id,email))
            cnxn.commit()


            return redirect('/account')
        
    else:
        flash('You must log in first')
        return redirect(url_for('login'))



@app.route('/requestmoney', methods=['GET', 'POST'])
def requestmoney():
    if request.method == 'POST':
        
        amount = float(request.form['amount'])
        emails = request.form.getlist('email[]')
        percents = [int(p) for p in request.form.getlist('percent[]')]
        memo = request.form['Memo']

        # Check that the percentages add up to 100
        total_percent = sum(percents)
        if total_percent != 100:
            error_msg = {'error': 'Percentages must add up to 100.'}
            return jsonify(error_msg), 400
        
        amounts = [(amount * p / 100) for p in percents]
        total_amount = sum(amounts)

        for i in range(len(emails)):
            email = emails[i]
            amount = amounts[i]
            # Insert transactions into database
            sender_id = session['id']
            now = datetime.now()
            Date = now.strftime("%Y-%m-%d %H:%M:%S")
            transaction_id = random.randint(1000, 9999)
            cursor.execute("INSERT INTO Request_transaction (RTid, Amount, date_of_transaction, Memo,SSN) VALUES (?, ?, ?, ?,? )", (transaction_id, amount, Date, memo, sender_id))
            cnxn.commit()

            recipient_ssn = cursor.execute("SELECT ssn FROM Email WHERE EmailAdd = ? ", (email,)).fetchone()
            if recipient_ssn is not None:
                rec = recipient_ssn[0]
                cursor.execute("INSERT INTO From_User (RTid, Identifier,Percentage) VALUES (?, ?, ?)", (transaction_id, email, percents[i]))
                sender = cursor.execute("UPDATE User_Account SET balance = balance + ? WHERE ssn = ?", (amount ,sender_id))
                receiver = cursor.execute("UPDATE User_Account SET balance = balance - ? WHERE ssn = ?", (amount, rec))
                cnxn.commit()
            else:
                cursor.execute("DELETE FROM Request_transaction WHERE RTid =?", (transaction_id,))
                cnxn.commit()

        return redirect('/account')
    
    else:
        return redirect('/account')
    


@app.route('/statements', methods=['GET', 'POST'])
def statements():
    if request.method == 'GET':
        user_id = session.get("id")
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        total_send = cursor.execute("SELECT SUM(Amount) FROM Send_Transaction GROUPBY WHERE ssn = ? AND date_time between ? and ?", (id,start_date,end_date)).fetchall()
        total_request = cursor.execute("SELECT SUM(Amount) FROM Request_Transaction GROUPBY WHERE ssn = ? AND date_of_transaction between ? and ?", (id,start_date,end_date)).fetchall()
        avg_send = cursor.execute("SELECT AVG(Amount) FROM Send_Transaction GROUPBY WHERE ssn = ? AND date_time between ? and ?", (id,start_date,end_date)).fetchall()
        avg_request = cursor.execute("SELECT AVG(Amount) FROM Request_Transaction GROUPBY WHERE ssn = ? AND date_of_transaction between ? and ?", (id,start_date,end_date)).fetchall()
        list_returning = list(total_send,total_request,avg_send,avg_request)
        return render_template('statements.html',list_returning)
    else:
        return render_template('account.html')



@app.route('/search_transactions', methods=['GET', 'POST'])
def search_transactions():
    if 'loggedin' not in session:
        flash('You must log in first')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the search criteria from the form
        transaction_type = request.form['transaction_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        identifier = request.form['identifier']
        
        # Determine which table to search based on the transaction type selected
        if transaction_type == 'sent':
            table_name = 'Send_Transaction'
            date_column_name = 'date_time'
            query="SELECT * FROM Send_Transaction where identifier = ?"
            params=[identifier]
        elif transaction_type == 'received':
            table_name = 'Request_Transaction'
            date_column_name = 'date_of_transaction'
            query="SELECT * FROM request_transaction R JOIN From_User F ON R.RTID=F.RTID where F.identifier = ? "
            params=[identifier]
        else:
            # If no button was clicked, show the search form again
            return render_template('account.html')

        # Build the SQL query to search for transactions
        # query = f"SELECT * FROM {table_name} WHERE SSN = ?"
        # params = [session['id']]

        if start_date:
            query += f" AND {date_column_name} >= ?"
            params.append(start_date)

        if end_date:
            query += f" AND {date_column_name} <= ?"
            params.append(end_date)

        # Execute the query and fetch the results
        transactions = cursor.execute(query, params).fetchall()

        # Render the search results template with the transactions data
        return render_template('search_results.html', transactions=transactions) 
    
    # If the request method is GET, show the search form
    else:
        return render_template('account.html')


@app.route('/modify')
def modify():
    return render_template('modify.html')

@app.route("/modifyemail", methods=["POST"])
def modifyemail():
    
    user_id = session['id']
    if request.method == 'POST':
        if request.form['action'] == 'add':
            email = request.form['email']
            if len(email) > 20:
                error_message = 'Email is too long'
                return render_template('modify.html', error=error_message)
            
            elif cursor.execute("SELECT * FROM Email WHERE EmailAdd = ?", (email)).fetchone() is not None:
                error_message = 'Email already exits!'
                return render_template('modify.html', error=error_message)
            else:
                cursor.execute("INSERT INTO Electronic_Address (identifier, verified,type) VALUES (?, ?, ?)", (email, True, "email"))
                cnxn.commit()
                cursor.execute("UPDATE Email SET EmailAdd = ? WHERE ssn = ?", (email, user_id))
                cnxn.commit()
                message = 'SUCCESS'
                return render_template('modify.html', error=message)
            
        elif request.form['action'] == 'remove':
            email = request.form['remove-email']
            if cursor.execute("SELECT * FROM Email WHERE EmailAdd = ?", (email)).fetchone() is None:
                error_message = 'Invalid Email'
                return render_template('modify.html', error=error_message)
            else:
                cursor.execute("DELETE FROM Email WHERE EmailAdd = ?", (email))
                cursor.execute("DELETE FROM Electronic_Adress WHERE identifier = ?", (email))
                cnxn.commit()
                return jsonify({"success": True}), 200

    else:
        return render_template('modify.html')


@app.route("/modifyphone", methods=["POST"])
def modifyphone():
    user_id = session['id']
    if request.method == 'POST':
        if request.form['action'] == 'add':
            phone = request.form['phone']
            if len(phone) > 20:
                error_message = 'Phone No. is too long'
                return render_template('modify.html', error=error_message)
            
            elif cursor.execute("SELECT * FROM User_Account WHERE Phone_no = ?", (phone)).fetchone() is not None:
                error_message = 'Phone already exits!'
                return render_template('modify.html', error=error_message)
            else:
                user = cursor.execute("SELECT * FROM User_Account WHERE SSN =?",(user_id,phone))
                prev_Phone= user.fetchone()
                cnxn.commit()
                cursor.execute("UPDATE User_Account SET Phone_no = ? WHERE SSN = ?", (phone, user_id))
                cnxn.commit()
                cursor.execute("UPDATE Electronic_Address SET Identifier = ? WHERE Identifier = ?",(phone,prev_Phone[2]))
                cnxn.commit()
                
                message = 'SUCCESS'
                return render_template('modify.html', error=message)
            
        elif request.form['action'] == 'remove':
            email = request.form['remove-email']
            if cursor.execute("SELECT * FROM User_Account WHERE Phone_no = ?", (phone)).fetchone() is None:
                error_message = 'Invalid Email'
                return render_template('modify.html', error=error_message)
            else:
                cursor.execute("DELETE FROM User_Account WHERE Phone_no = ?", (phone))
                cursor.execute("DELETE FROM Electronic_Adress WHERE identifier = ?", (phone))
                cnxn.commit()
                return jsonify({"success": True}), 200

    else:
        return render_template('modify.html')



@app.route('/signout')
def signout():
    return render_template('login.html')

        


    
@app.route('/')
def fe():
    return render_template('login.html')




if __name__ == "__main__": 
    app.run()