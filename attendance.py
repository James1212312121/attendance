import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
from RPLCD.i2c import CharLCD
from gpiozero import Button
from datetime import datetime

now = datetime.now()

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574',0x27)
button = Button(4)

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd = "password",
    database = "school"
)

mycursor = mydb.cursor()
total = 0
id = 0

try:
    def pageBreak():
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()

    def createTable():
        mycursor.execute("create table productTB2 (id varchar(40) not null primary key,name varchar(255) not null, price float not null)")
            
    def showClass(table):
        mycursor.execute('select * from ' + table)
        
        print("|\tID\t|\tClass Name\t|\tTeacher\t|")
        print("________________________________________________________________")
        myresult = mycursor.fetchall()
        for x in myresult:
            print("|\t" + str(x[0]) + "\t|\t" + x[1] + "\t|\t" + x[2] + "\t|")
        
    def insertVerifyClass(table ,name, teacher):
        mycursor.execute('select * from ' + table + ' where name = "' + name + '"')
        
        myresult = mycursor.fetchall()
        
        if len(myresult) == 0:
            mycursor.execute('insert into ' + table + ' (name, teacher) values ("' + name + '", "' + teacher + '")')
            mydb.commit()
            print("class inserted")
        else:
            print("class already exist")
            
    def checkForClassId(table, id):
        mycursor.execute('select * from ' + table + ' where id = ' + str(id))
        
        myresult = mycursor.fetchall()
        
        if len(myresult) != 0:
            return True
    
    def showStudent(table):
        mycursor.execute('select * from ' + table)
        
        print("|\tID\t|\tFirst Name\t|\tLast Name\t|\tNick Name\t|")
        print("________________________________________________________________")
        myresult = mycursor.fetchall()
        for x in myresult:
            print("|\t" + str(x[0]) + "\t|\t" + x[1] + "\t|\t" + x[2] + "\t|\t" + x[3] + "\t|")
        
    def insertVerifyStudent(table ,id, firstname, lastname, nickname):
        mycursor.execute('select * from ' + table + ' where id = "' + str(id) + '"') 
        
        myresult = mycursor.fetchall()
        
        if len(myresult) == 0:
            mycursor.execute('insert into ' + table + ' (id, first_name, last_name, nick_name) values ("' + str(id) + '", "' + firstname + '", "' + lastname + '", "' + nickname + '")')
            mydb.commit()
            print("student inserted")
        else:
            print("student already exist")
            
    def checkForStudentId(table, id):       
        mycursor.execute('select * from ' + table + ' where id = ' + str(id))
        
        myresult = mycursor.fetchall()
        
        if len(myresult) != 0:
            return True
        
    def deleteStudent(table, id):
        mycursor.execute('delete from ' + table + ' where id = ' + str(id))
        mydb.commit()
        print("Student is deleted from Student database")
    
    def deleteAttendance(table, id):
        mycursor.execute('delete from ' + table + ' where studentid = ' + str(id))
        mydb.commit()
        print("Student is deleted from Attendance database")
        
    def showAttendance(table):
        mycursor.execute('select * from ' + table)
        
        print("|\tStudent ID\t|\tClass ID\t|\tDate Time\t|")
        print("________________________________________________________________")
        myresult = mycursor.fetchall()
        for x in myresult:
            print("|\t" + str(x[0]) + "\t|\t" + x[1] + "\t|\t" + x[2] + "\t|")
        
    def insertVerifyAttendance(table ,studentid, classid, datetime): #hererererererererererererererere
        mycursor.execute('select * from ' + table + ' where studentid = "' + str(studentid) + '" and classid = "' + str(classid) + '" and datetime = "' + str(datetime) + '"')
        
        myresult = mycursor.fetchall()
        
        if len(myresult) == 0:
            mycursor.execute('insert into ' + table + ' (studentid, classid, datetime) values ("' + str(studentid) + '", "' + str(classid) + '", "' + str(datetime) + '")')
            mydb.commit()
            print("attendance checked")
            return True
        else:
            print("you already checked in today!!!!!!!")
            return False
    
    #student = id, first_name last_name nick_name
    #class = id name teacher
    #attendance = studentid classid date
    
    

    menu = 0
    conWorking = 1
    table = None
    while conWorking == 1:
        if menu == 0:
            print("|||||||||||||||||||||||||||||||||||||||||")
            print("Please select the function")
            print("[1] to add class")
            print("[2] to show class")
            print("[3] to add students")
            print("[4] to show students")
            print("[5] to add attendance")
            print("[6] to show attendance")
            print("[7] to add continuous attendance")
            datetime = str(now.day) + '-' + str(now.month) + '-' + str(now.year)
            
            userInput = input()
            if userInput == "1":
                print("------------------------------------------------")
                table = "classes"
                print("class name?")
                name = input()
                print("class teacher?")
                teacher = input()
                insertVerifyClass(table, name, teacher)
            elif userInput == "2":
                print("------------------------------------------------")
                table = "classes"
                showClass(table)
            elif userInput == "3":
                print("------------------------------------------------")
                table = "students"
                print("please scan the tag")
                id,name = reader.read()
                print("firstname?")
                firstname = input()
                print("lastname?")
                lastname = input()
                print("nickname?")
                nickname = input()
                insertVerifyStudent(table, id, firstname, lastname, nickname)
            elif userInput == "4":
                print("------------------------------------------------")
                table = "students"
                showStudent(table)
                print("Do you want to delete student and their attendance?")
                print("[1] : Yes")
                print("[2] : No")
                userInput = input()
                if userInput == "1":
                    print("student id?")
                    print("please scan your tag")
                    #herererererere
                    id, name = reader.read()
                    if checkForStudentId("students", id):
                        deleteStudent("students", id)
                        deleteAttendance("attendance", id)
                        print("student delete success")
                    else:
                        print("student does not exist!!!")
            elif userInput == "5":
                print("------------------------------------------------")
                table = "attendance"
                print("please tag your id card")
                studentid,name = reader.read()
                if checkForStudentId("students", studentid):
                    print("\n")
                    showClass("classes")
                    print("what is the ID of your class?")
                    classid = input()
                    if checkForClassId("classes", classid):
                        print("\n\n")
                        insertVerifyAttendance(table ,studentid, classid, datetime)
                        print("[Enter]")
                        input()
                        print("\n\n\n")
                    else:
                        print("\n\n")
                        print("Class does not exist!!!")
                        print("[Enter]")
                        input()
                        print("\n\n\n")
                else:
                    print("\n\n")
                    print("You have not signed up as a student!!!")
                    print("[Enter]")
                    input()
                    print("\n\n\n")
            elif userInput == "6":
                print("------------------------------------------------")
                table = "attendance"
                showAttendance(table)
            elif userInput == "7":
                print("------------------------------------------------")
                table = "attendance"
                print("Continuous Check in Selected")
                print("please select class")
                print("\n")
                showClass("classes")
                print("what is the ID of your class?")
                lcd.write_string("please insert")
                lcd.cursor_pos = (1,0)
                lcd.write_string("class id")
                classid = input()
                lcd.clear()
                if checkForClassId("classes", classid):
                    while True:
                        lcd.clear()
                        print("\n\n")
                        print("please tag your id card or press the button to exit")
                        lcd.write_string("Attendance for")
                        lcd.cursor_pos = (1,0)
                        mycursor.execute('select * from classes where id = ' + str(classid))
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            classname = str(x[1])
                        lcd.write_string(classname)
                        lcd.cursor_pos = (2,0)
                        lcd.write_string("place your tag")
                        while not (reader.read_id_no_block() or button.is_pressed):
                            sleep(0.01)
                        if button.is_pressed:
                            break
                        else:
                            studentid,name = reader.read()
                            if checkForStudentId("students", studentid):
                                if insertVerifyAttendance(table ,studentid, classid, datetime):
                                    lcd.clear()
                                    lcd.write_string("check-in success")
                                else:
                                    lcd.clear()
                                    lcd.write_string("You already Checked-in")
                                print("\n")
                            sleep(1)
                else:
                    print("\n\n")
                    print("Class does not exist!!!")
                    print("[Enter]")
                    input()
                    print("\n\n\n")
                
finally:
    GPIO.cleanup;




        


