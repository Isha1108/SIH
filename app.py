from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask
from flask_mail import Mail, Message
import smtplib
import speech_recognition as sr
from pydub import AudioSegment
import wave
import keyboard
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import PyAudio

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dys'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'as1303879@gmail.com'
app.config['MAIL_PASSWORD'] = 'lincolnab'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        print("gg")
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        # Check if account exists using MySQL
        print(email)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM p_creds WHERE password = %s ', [password])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            #account exists and test taken, so redirect to profile page
            return render_template('student_profile.html')
            #account exists and test NOT taken, so redirect to exam page page   
  
    
    return render_template('signin.html')


def sendmail(s_name, password, p_name, school, p_email, p_phone):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = "kashyapahana20@gmail.com"
    toaddr = str(p_email)

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = " Your child's registration details "
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s_id FROM p_creds WHERE p_email = %s ', [p_email])
    s_id = cursor.fetchone()

    body = "Name: "+  str(s_name)+'\n' +"Password: "+  str(password)+'\n' +"Registered Parent's Name: "+  str(p_name)+'\n' +"School: "+  str(school)+'\n' +"Parent's registered email: "+  str(p_email)+'\n' +"Mobile Number: "+  str(p_phone)+'\n' +"Student's ID: "+  str(s_id)+'\n'
    msg.attach(MIMEText(body,'plain'))

    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.starttls()
    server.login(fromaddr, "Kash@1108")

    text = msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    print("hjsgcjydg")
    server.quit()

    

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    s_id = 0000000
    if request.method == 'POST' :
        s_name = request.form['s_name']
        age = request.form['age']
        password = request.form['password']
        p_name = request.form['p_name']
        school = request.form['school']
        p_email = request.form['p_email']
        p_phone = request.form['p_phone']
        
        print(s_name,age,password,p_name, school, p_email, p_phone)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('INSERT INTO p_creds(s_name, age, p_name, school, p_email, p_phone, password, s_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', [s_name,age,p_name,school,p_email,p_phone,password, s_id])
        mysql.connection.commit()
        sendmail(s_name, password, p_name, school, p_email, p_phone)
        

        msg = 'Successfully registered! Please Sign-In'
        print('done')
        #student will be redirected for a test immediately
        return redirect(url_for('student_test'))
    
    return render_template('signup.html') 

@app.route('/d_signup', methods=['GET', 'POST'])
def d_signup():
    if request.method == 'POST':
        d_name = request.form['d_name']
        d_password = request.form['d_password']
        d_email = request.form['mail']
        desi = request.form['Designation']
        d_no = request.form['num']
        d_id=0

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)        
        cursor.execute('INSERT INTO d_creds(d_id, d_password, d_name, d_no, d_email) VALUES(%s,%s,%s,%s,%s)', [d_id,d_password,d_name,d_no,d_email])
        mysql.connection.commit()
        return redirect(url_for('dr-profile')) 
    return render_template('d_signup.html')   

@app.route('/d_login', methods=['GET', 'POST'])
def d_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM d_creds WHERE d_password = %s ', [password])   
        account = cursor.fetchone()

        if account:      
            return render_template('dr-profile.html')     
    
    return render_template('d_login.html')


@app.route('/dr_landing')
def dr_landing():
    return render_template('dr_landing.html')   

@app.route('/doctor-patient-profile')
def dpp():
    return render_template('doctor-patient-profile.html')

@app.route('/doctor-profile')
def dp():
    return render_template('doctor-profile.html')

@app.route('/student_profile')
def student_profile():
    return render_template('student_profile.html')

@app.route('/student_profile1')
def student_profile1():
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('18sXYVa_hqEAcZAuuzXplbqKcKsLj0dPZ80V5ZuNw9uI')
    Worksheet= sh.worksheet('Sheet1')
    list_of_lists = Worksheet.get_all_values()
    questions_list = []
    responses_of_parent = []


    student_name = 'Ronit Bhamere'
    q1 = list_of_lists[0][1]
    q2 = list_of_lists[0][2]
    q3 = list_of_lists[0][3]
    q4 = list_of_lists[0][4]
    q5 = list_of_lists[0][5]
    q6 = list_of_lists[0][6]
    q7 = list_of_lists[0][7]
    q8 = list_of_lists[0][8]
    q9 = list_of_lists[0][9]
    q10 = list_of_lists[0][10]
    q11 = list_of_lists[0][11]
    q12 = list_of_lists[0][12]
    q13 = list_of_lists[0][13]
    q14 = list_of_lists[0][14]
    q15 = list_of_lists[0][15]
    dic = {}

    questions_list = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15]

    for x in list_of_lists:
        if student_name in x[16]:
            a1 = x[1]
            a2 = x[2]
            a3 = x[3]
            a4 = x[4]
            a5 = x[5]
            a6 = x[6]
            a7 = x[7]
            a8 = x[8]
            a9 = x[9]
            a10 = x[10]
            a11 = x[11]
            a12 = x[12]
            a13 = x[13]
            a14 = x[14]
            a15 = x[15]
            student_id = x[18]

    responses_of_parent = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15]     
    dic = dict(zip(questions_list, responses_of_parent))

    print(dic)
    return render_template('student_profile1.html', dic=dic)

@app.route('/student_list')
def student_list():
    return render_template('student_list.html')

# def speechr():
#     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute('SELECT * FROM dys_identification')
#     para = cursor.fetchall()
    
    
#     para_list = []
#     for i in range (len(para)):
#         x = para[i]
#         list_h = []
#         for key in x.values():
#             list_h.append(key)
#         para_list.append(list_h)

#     paragraph_string = para_list[0][1]
    


@app.route('/student_test')
def student_test():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM dys_identification')
    para = cursor.fetchall()
    
    
    para_list = []
    for i in range (len(para)):
        x = para[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        para_list.append(list_h)

    paragraph_string = str(para_list[0][1])

    r = sr.Recognizer()  
    paragraph = paragraph_string.lower()
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for ele in paragraph:
        if ele in punc:
            paragraph = paragraph.replace(ele, "")

    
    text = 'No text found'
    while True:
        with sr.Microphone() as source:
                # read the audio data from the default microphone
            audio_data = r.record(source)
            print("Recognizing...")
            # convert speech to text
            try :
                text_og= str(r.recognize_google(audio_data, language= "en-IN"))
                text = text_og.lower()
                text = list(text.split(" ")) 
                if keyboard.press('q'):
                    break
            except :
                pass    
    count = 0
    for i in range(len(paragraph)):
        for j in range(len(text)):
            if paragraph[i] == text[j]:
                count = count + 1

    wrong_words_spoken_list = [] 
    right_words_spoken_list = []           
    for i in range(len(text)):
        if text[i] in paragraph:
            right_words_spoken_list.append(text[i])
        elif text[i] not in paragraph:
            wrong_words_spoken_list.append(text[i])
            

    accuracy = 100* (count/len(paragraph))
    print ('Analysis :')
    print('Text given to student to read: ', paragraph_string)
    print('Text spoken by the Student : ', text_og)
    print('The list of right words spoken by the student is: ', right_words_spoken_list) 
    print('The list of wrong words spoken by the student is: ', wrong_words_spoken_list) 
    print('Accuracy Percentage of right words: ', accuracy)
    print('Number of right words spoken: {right} and number of wrong words spoken: {wrong}'.format(right = len(right_words_spoken_list), wrong = len(wrong_words_spoken_list))) 
    

    return render_template('student_test.html', para_list=para_list)

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

if __name__ == "__main__":
    app.run(debug=True)