
import logging
import os
import redis
from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import hashlib
import pandas as pd
import time
import json

app = Flask(__name__)

#This function is used to load the csv file into the database
@app.route('/ctb', methods=['GET','POST'])
def ctb():
    if request.method == 'POST':
        f = request.files['myf']
        d = pd.read_csv(f)
        cnx = sql.connect('minnowdatabase.db')
        d.to_sql(name="quake", con=cnx, if_exists="replace", index=False)
        return render_template('home.html')

@app.route('/')
def home():
	return render_template('home.html')
	
@app.route('/nonredis',methods=['GET','POST'])
def nonredis():
	#val1 = str(request.form['mag1'])
	#val2 = str(request.form['mag2'])
	before_time = time.time()
	val1 = str(3)
	val2 = str(5)
	cnx = sql.connect("minnowdatabase.db")
	cnx.row_factory = sql.Row
	cr = cnx.cursor()
	for i in range(40):
		cr.execute("select * from quake where mag between "+val1+" and "+val2)
		rows = cr.fetchall();
		length = len(rows)
	cr.execute("select place from quake")
	row = cr.fetchone()
	print row
	after_time = time.time()
	response_time = after_time - before_time
	return render_template("response.html",response_time=str(response_time),str="Non-Redis (Normal)",length=length,before_time=before_time)

@app.route('/hello_redis', methods=['GET','POST'])    
def hello_redis():
    """Example Hello Redis Program"""
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    redis_password = os.environ.get('REDIS_PASSWORD', None)
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
    for i in range(0, 40):
        query = "select * from quake"
        hash_value = hashlib.sha224(query).hexdigest()
        key = "sql_cache:" + hash_value
        print("Created Key\t : ",key)
        before = time.time()
        cnx = sql.connect("minnowdatabase.db")
    	cnx.row_factory = sql.Row
    	cr = cnx.cursor()
    	rows = cr.fetchall();
        if r.get(hash_value):
            after = time.time()
        else:
            cr.execute(query)
            data = cr.fetchall()
            after = time.time()

        response_time = after - before
    return render_template("response.html",response_time=str(response_time),str="Redis")	
	
if __name__ == '__main__':
	app.run(debug=True)
