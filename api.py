##libraries
import os
from IPython.display import HTML
import flask
from datetime import datetime, timezone
import pyodbc
import pandas as pd
import numpy as np
import json
from flask import request
from flask import Flask, render_template, redirect, url_for, request, session

###database connectioon
server = '' 
database = '' 
username = '' 
password = '' 
print("connecting.......")
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
print("connected!")

##flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "my precious"
## routes to each webpage
@app.route('/')
def fe():
    return render_template('home.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=="POST":
        cursor.execute('SELECT * FROM spjain.dbo.student_info WHERE CampusId=' + str(request.form['username']))
        for row in cursor:
            for i in range(0,3):
                if i ==0:
                    Data1 =  "Campus ID : " + str(list(row)[i])
                elif i ==1:
                    Data2 = "Full Name : " + str(list(row)[i])
                elif i ==2:
                    Data3 =  "Batch : " + str(list(row)[i])
        return render_template('html.html', d1=Data1, d2 =Data2, d3=Data3)
    return render_template('input.html')
@app.route('/updatedb', methods=['GET', 'POST'])
def updatedb():
    if request.method=='POST':
        values = "(" +"'"+ str(request.form['campusid']) +"'"+ ","+"'"+ str(request.form['fullname'])+"'"+ ","+"'"+ str(request.form['batch']) +"'"+ ")"
        cursor.execute('SELECT * FROM spjain.dbo.student_info')
        cursor.execute('INSERT INTO spjain.dbo.student_info (CampusId,FullName,Batch) Values ' + values)
        cnxn.commit()
        return render_template('dbupdated.html')
    return render_template('insert.html')
@app.route('/sql',methods=['GET','POST'])
def sql():
    if request.method=='POST':
        sql = str(request.form['query'])
        sql_query = pd.read_sql_query(sql,cnxn)
        html = sql_query.to_html()
        text_file = open("C:/Users/91952/Desktop/college work/DATABASES/project db/api flask/templates/sqlout.html", "w")
        text_file.write(html)
        text_file.close()
        return render_template('sqlout.html')
    return render_template('sqlfill.html')
if __name__ == "__main__": 
    app.run()