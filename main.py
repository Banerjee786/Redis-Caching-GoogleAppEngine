
import logging
import os

from flask import Flask
import redis
from flask import Flask, render_template, request, url_for
import sqlite3 as sql
import hashlib
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
        d.to_sql(name="minnow", con=cnx, if_exists="replace", index=False)
        return render_template('home.html')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/hello_redis', methods=['GET','POST'])
def hello_redis():
    """Example Hello Redis Program"""
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    redis_password = os.environ.get('REDIS_PASSWORD', None)
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password)
    for i in range(0, 100):
        query = "select * from Minnow"
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

@app.route('/nonredis',methods=['GET','POST'])
def nonredis():
	before_time = time.time()
	for i in range(100):
		cnx = sql.connect("minnowdatabase.db")
    	cnx.row_factory = sql.Row
    	cr = cnx.cursor()
    	cr.execute("select * from minnow")
    	rows = cr.fetchall();
	after_time = time.time()
	response_time = after_time - before_time
	return render_template("response.html",response_time=str(response_time),str="Non-Redis (Normal)")
@app.route('/barchart', methods=['GET','POST'])
def list():
    cnx = sql.connect("minnowdatabase.db")
    cnx.row_factory = sql.Row
    cr = cnx.cursor()
    cr.execute("select * from minnow where Fare=100")
    rows = cr.fetchall();
    fare100=len(rows)
    cr.execute("select * from minnow where Fare=200")
    rows = cr.fetchall();
    fare200=len(rows)
    cr.execute("select * from minnow where Fare=500")
    rows = cr.fetchall();
    fare500=len(rows)
    cr.execute("select * from minnow where Fare=800")
    rows = cr.fetchall();
    fare800=len(rows)
    total = 0.0
    total = fare100 + fare200 + fare500 + fare800
    p1 = (fare100*100.0)/total
    p2 = (fare200*100.0)/total
    p3 = (fare500*100.0)/total
    p4 = (fare800*100.0)/total
    print("fetch success")
    return render_template('barchart.html',p1=p1,p2=p2,p3=p3,p4=p4)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
	app.run(debug=True)
