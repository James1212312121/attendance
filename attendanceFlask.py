import mysql.connector
import RPi.GPIO as GPIO
from time import sleep
from flask import Flask
app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd = "password",
    database = "school"
)

mycursor = mydb.cursor()

text ='''
<t1>
Attendance
<t1>

<br>

<table style="width:100%; border: 2px solid black;">
    <tr>
        <th> ID </th>
        <th> Student Name </th>
        <th> Class Name </th>
        <th> Class Teacher </th>
        <th> Attendance </th>
    </tr>
'''

@app.route('/')
def hello_world():
    return text + "</table>"


mycursor.execute('select * from attendance')
myresult = mycursor.fetchall()
for x in myresult:
    mycursor.execute('select nick_name from students where id = ' + str(x[0]))
    myresult2 = mycursor.fetchall()
    for y in myresult2:
        name = str(y[0])
        
    mycursor.execute('select * from classes where id = ' + str(x[1]))
    myresult3 = mycursor.fetchall()
    for z in myresult3:
        classname = str(z[1])
        classteacher = str(z[2])
        
    text += '''
    <tr>
        <td style="border: 2px solid black"> ''' + str(x[0]) + '''</td>
        <td style="border: 2px solid black"> ''' + name + '''</td>
        <td style="border: 2px solid black"> ''' + classname + '''</td>
        <td style="border: 2px solid black"> ''' + classteacher + '''</td>
        <td style="border: 2px solid black"> ''' + str(x[2]) + '''</td>
    </tr>

    '''

if __name__ == '__main__':
    app.run()





