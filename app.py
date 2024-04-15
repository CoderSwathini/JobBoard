
from flask_mysqldb import MySQL
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql.cursors import DictCursor

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)
app.secret_key = os.urandom(16)


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DB'] = 'swathini'
mysql = MySQL(app)

def create_table():
    with app.app_context():  
        #mysql.connection.cursor(DictCursor)
        cur = mysql.connection.cursor()
        cre_qry = 'CREATE DATABASE IF NOT EXISTS swathini'
        cre_tb='CREATE TABLE IF NOT EXISTS job_board (jobtitle VARCHAR(50) ,companyname VARCHAR(50),email VARCHAR(50),salary INT NOT NULL,jobid VARCHAR(50) PRIMARY KEY,postdate DATE,city VARCHAR(30),description VARCHAR(1000))'
        cre_tb_spam='CREATE TABLE IF NOT EXISTS spam (jobtitle VARCHAR(50) ,companyname VARCHAR(50),email VARCHAR(50),salary INT NOT NULL,jobid VARCHAR(50) PRIMARY KEY,postdate DATE,city VARCHAR(30),description VARCHAR(1000))'
        cur.execute(cre_qry)
        cur.execute(cre_tb,cre_tb_spam)
        print(cre_qry,cre_qry,cre_tb_spam)
        mysql.connection.commit()
        cur.close()
    
    



@app.route('/',methods=['GET', 'POST'])
def index():
   create_table()

   return render_template('home.html')


@app.route('/listjob',methods=['GET', 'POST'])
def viewjob():
    mysql.connection.cursor(DictCursor)
    cur = mysql.connection.cursor()
    #cur = mysql.connection.cursor(dictionary = True)
    sql_list = 'SELECT * FROM job_board'
    cur.execute(sql_list)
    jobs_tuple = cur.fetchall()
    cur.close()
    # jobtitle,companyname,email,salary,jobid,postdate,city,description
    job_dict= [{'jobtitle': jobs[0], 'companyname': jobs[1], 'email': jobs[2], 'salary': jobs[3],'jobid': jobs[4], 'postdate': jobs[5],'city': jobs[6], 'description': jobs[7] } for jobs in jobs_tuple]
    return render_template('listjob.html',jobs=job_dict)
    
@app.route('/smartsearch',methods=['GET'])
def smartsearch():
    if request.method =='GET':
        jobtitle=request.args.get('jobtitle')
        city=request.args.get('city')
        mysql.connection.cursor(DictCursor)
        cur = mysql.connection.cursor()
        ss_query = ''' SELECT * FROM job_board
                    WHERE city = '%s' AND jobtitle = '%s' '''
        cur.execute(ss_query %(city,jobtitle))
        jobs_tuple = cur.fetchall()
        cur.close()
        job_dict = [{'jobtitle': jobs[0], 'companyname': jobs[1], 'email': jobs[2], 'salary': jobs[3],'jobid': jobs[4], 'postdate': jobs[5],'city': jobs[6], 'description': jobs[7] } for jobs in jobs_tuple]
        return render_template('listjob.html',jobs=job_dict)
    else:
        flash('No Jobs Available', 'error')
        return redirect(url_for('viewjob'))

@app.route('/jobdetails/<string:jobid>',methods=['GET'])
def jobdetails(jobid):
    if request.method =='GET':
        mysql.connection.cursor(DictCursor)
        cur = mysql.connection.cursor()
        jd_query='SELECT * FROM job_board WHERE jobid= %s'
        cur.execute(jd_query, (jobid,))
        job_tuple=cur.fetchone()
        cur.close()
        print(job_tuple)  
        if job_tuple:
            job_details = {
                'jobtitle': job_tuple[0],
                'companyname': job_tuple[1],
                'email': job_tuple[2],
                'salary': job_tuple[3],
                'jobid': job_tuple[4],
                'postdate': job_tuple[5],
                'city': job_tuple[6],
                'description': job_tuple[7]
            }
        return render_template('jobdetails.html',job=job_details) 
    else:
            flash('No Job Decription', 'error')
            return redirect(url_for('listjob'))
            
@app.route('/postjob',methods=['GET', 'POST'])
def postjob():
    if request.method =='POST':
        jobtitle=request.form['job_title']
        companyname=request.form['companyName']
        email=request.form['recruiter_email']
        salary=request.form['salary']
        jobid=request.form['jobid']
        postdate=request.form['postdate']
        city=request.form['city']
        description=request.form['message']
       # jobtitle,companyname,email,salary,jobid,postdate,city,description
        mysql.connection.cursor(DictCursor)
        cur= mysql.connection.cursor()
        sql = 'INSERT INTO job_board (jobtitle,companyname,email,salary,jobid,postdate,city,description) VALUES (%s, %s, %s,%s, %s, %s,%s, %s)'
        
        data = (jobtitle,companyname,email,salary,jobid,postdate,city,description)
        cur.execute(sql,data)
        mysql.connection.commit()  # runs query in the database
        flash( ' Added successfully', 'success')
        return redirect(url_for('viewjob'))
    else:
        return render_template('postjob.html')

@app.route('/editjob/<string:jobid>',methods=['GET','POST'])
def editjob(jobid):
    if request.method =='POST':
        jobtitle=request.form['job_title']
        companyname=request.form['companyName']
        email=request.form['recruiter_email']
        salary=request.form['salary']
        jobid=request.form['jobid']
        postdate=request.form['postdate']
        city=request.form['city']
        description=request.form['message']
       # jobtitle,companyname,email,salary,jobid,postdate,city,description
        mysql.connection.cursor(DictCursor)
        
        cur= mysql.connection.cursor()
        update_sql = '''  UPDATE swathini.job_board SET jobtitle= %s,
            companyname=%s,email=%s,salary=%s,postdate=%s,
            city=%s,description=%s WHERE jobid=%s '''
       
     
        data = (jobtitle,companyname,email,salary,postdate,city,description,jobid)
        cur.execute(update_sql,data)
        mysql.connection.commit()  
        flash( ' Updates successfully', 'success')
        return redirect(url_for('viewjob'))
    
    print(jobid)
    mysql.connection.cursor(DictCursor)
    
    cur= mysql.connection.cursor()
    updt_qry='SELECT * FROM job_board WHERE jobid =%s'
    cur.execute(updt_qry,[jobid])
    job_details=cur.fetchone()
    print(job_details)
    return render_template('editjob.html',job=job_details) 

@app.route('/delete/<string:jobid>')
def deletejob(jobid):
    mysql.connection.cursor(DictCursor)
    cur= mysql.connection.cursor()
    del_qury='DELETE FROM job_board WHERE jobid=%s'
    cur.execute(del_qury,(jobid,))
    mysql.connection.commit()  # runs query in the database
    flash( ' Deleted successfully', 'success')
    return redirect(url_for('viewjob'))
    
if __name__  == '__main__':
    app.run(port=5005, debug=True)

