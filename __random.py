import mysql.connector as sql
conn=sql.connect(host='localhost',user='root',password='root',database='racetrack')
mycursor=conn.cursor()

def start():
    f = open("racetrack.txt", "r")
    print(f.read())
    choicee=int(input("      ENTER THE CHOICE(1 or 2):        "))
    if choicee==1:
            login()
    elif choicee==2:
            create()
    else :
        print("PLEASE ENTER (1 or 2)!")
        print()
        start()
   

def create():
    import csv
    print('+++++++++++++++++++++++++++++++++++++++++++++           WELCOME TO YAS MARINA ACCOUNT CREATION SYSTEM           +++++++++++++++++++++++++++++++++++++++++++++')
    import datetime as dt
    print(dt.datetime.now())
    with open("accounts.csv",mode='a',newline='') as f:
        writer=csv.writer(f,delimiter=',')
        invalidpass="!@#$%^&*() +=~`/*-.,?><:;}]{["
        name=input('ENTER A USERNAME=')
        if (name == ''):
            print("CAN'T LEAVE FIELD EMPTY-PLEASE TRY AGAIN")
            create()
        else:
            print()
            password=input('ENTER A PASSWORD(must not contain special characters!)=')
            if (password==''):
                print("CAN'T LEAVE FIELD EMPTY-PLEASE TRY AGAIN")
                create()
            else:
                print()
                for i in password:
                    if (i in invalidpass):
                        print("PASSWORD MUST NOT CONTAIN SPECIAL CHARACTERS-PLEASE TRY AGAIN")
                        create()
                    else:
                        repassword=input('RE-ENTER YOUR PASSWORD=')
                        if password==repassword:
                            writer.writerow([name,password])
                            print()
                            print('USER CREATED SUCCESSFULLY')
                            login()
                        else:
                            print('PASSWORD DOES NOT MATCH-PLEASE TRY AGAIN')
                            create()
   
def login():
    import csv
    print("*************************************************                    YAS MARINA RACETRACK LOGIN            *************************************************")
    print()
    c=input("DO YOU WANT TO CONTINUE OR NOT(yes or no):")
    if(c=='yes'):
        name=input('ENTER YOUR USERNAME=')
        print()
        password=input('ENTER YOUR PASSWORD=')
        print()
        with open("accounts.csv",mode='r') as f:
            reader=csv.reader(f,delimiter=",")
            for row in reader:
                if row == [name,password]:
                    print("YOU HAVE SUCCESSFULY LOGGED IN")
                    ch=input("IS THIS YOUR FIRST LOGIN?(yes or no):")
                    if(ch=='yes'):
                        register()
                    elif(ch=='no'):
                        print('LOADING...')
                        menu()
                    else:
                        print("PLEASE ENTER (yes or no)")
                        login_error()
    elif(c=='no'):
        print('EXITING...')
        exitt()
    else:
        print("PLEASE CHOOSE(yes or no)!")
        login()

def login_error():
    c=input("IS THIS YOUR FIRST LOGIN?(yes or no):")
    if(c=='yes'):
        register()
    elif(c=='no'):
        menu()
    else:
        login_error()