# THIS FILE IS ONLY IF YOU WANT TO USE YOUR OWN DATABASE
# USES PRE-MADE STATEMENTS TO INSERT OR GET VALUES FROM SQLDATABASE
import mysql.connector
from twilio.rest import Client

account_sid = '###REPLACE WITH YOUR TWILIO SID TOKEN###'
auth_token = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
client = Client(account_sid, auth_token)


class sqlEdit:
    def __init__(self):
        self.mydb, self.cursor = self.startConnection()
    #Closes upon return to prevent SQL timeouts
    def startConnection(self):
        self.mydb = mysql.connector.connect(
            host="######",
            port="######",
            user="######",
            password="######",
            database="######")
        cursor = self.mydb.cursor()
        return self.mydb, cursor

    def endConnection(self):
        self.mydb.close()
        self.cursor.close()

    def checkRow(self):
        rowCheck = f"SELECT * FROM USERS"
        self.cursor.execute(rowCheck)
        fetchedValue = ''
        rowList = []
        for i in self.cursor:
            originalValue = str(i)
            fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace('',
                                                                                                         "").replace(
                '"', "").replace("'", '')
            rowList.append(fetchedValue)
        return rowList

    def checkValid(self, phoneNumber):
        doesExist = f"SELECT MENUCHOICE FROM USERS WHERE PHONENUMBER= {phoneNumber}"
        self.cursor.execute(doesExist)
        rowExists = self.cursor.fetchone()
        if rowExists is None:
            print(f"Now adding the number {phoneNumber}")
            self.insertClient(phoneNumber)
            print(f"Successfully added {phoneNumber} to the database")
            return True
        else:
            print(f"{phoneNumber} already exists!\n")
            return False

    def insertClient(self, phoneNumber):
        print(f"Value being added it {phoneNumber}")
        addQuery = f"insert ignore into USERS (phonenumber) values({phoneNumber})"
        self.cursor.execute(addQuery)
        self.mydb.commit()
        return

    def fetchChoice(self, phoneNumber, columnName):
        addQuery = f"select {columnName} from USERS where phonenumber={phoneNumber}"
        self.cursor.execute(addQuery)
        fetchedValue = ''
        for i in self.cursor:
            originalValue = str(i)
            fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',',
                                                                                                         "").replace(
                '"', "").replace("'", '')
        return fetchedValue

    def fetchValue(self, phoneNumber, columnType):
        if columnType == 'MENUCHOICE':
            addQuery = f"select MENUCHOICE from USERS where phonenumber={phoneNumber}"
        elif columnType == 'SUBMENUCHOICE':
            addQuery = f"select SUBMENUCHOICE from USERS where phonenumber={phoneNumber}"
        self.cursor.execute(addQuery)
        fetchedValue = ''
        for i in self.cursor:
            originalValue = str(i)
            fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',',
                                                                                                         "").replace(
                '"', "").replace("'", '')
        return fetchedValue

    def replaceValue(self, phonenumber, value):
        replaceQuery = f"UPDATE clients SET prevalue='{value}' WHERE phonenumber={phonenumber}"
        self.cursor.execute(replaceQuery)
        self.mydb.commit()

    def dailyTasks(self):
        addQuery = f"SELECT PHONENUMBER,CARLINK FROM USERS WHERE CARLINK!=''"
        self.cursor.execute(addQuery)
        test = []
        for i in self.cursor:
            originalValue = str(i)
            fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',',
                                                                                                         "").replace(
                '"', "").replace("'", '')
            test.append(fetchedValue)
        return test

    def replaceAll(self, phonenumber):
        replaceQuery = f"UPDATE USERS SET MENUCHOICE='0',SUBMENUCHOICE='0' WHERE phonenumber={phonenumber}"
        self.cursor.execute(replaceQuery)
        self.mydb.commit()

    def replaceChoice(self, value, column, number):
        replaceMenuChoice = f"UPDATE USERS SET {column}='{value}' WHERE PHONENUMBER={number}"
        self.cursor.execute(replaceMenuChoice)
        self.mydb.commit()

    def customQuery(self, query):
        self.cursor.execute(query)
        fetchedValue = ''
        rowList = []
        for i in self.cursor:
            originalValue = str(i)
            fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace('',
                                                                                                         "").replace(
                '"', "").replace("'", '')
            rowList.append(fetchedValue)
        return rowList

    def resetValues(self, NUMBER):
        replaceMenuChoice = f"UPDATE USERS SET MENUCHOICE='' WHERE PHONENUMBER={NUMBER}"
        self.cursor.execute(replaceMenuChoice)
        replaceMenuChoice = f"UPDATE USERS SET SUBMENUCHOICE='' WHERE PHONENUMBER={NUMBER}"
        self.cursor.execute(replaceMenuChoice)
        replaceMenuChoice = f"UPDATE USERS SET STARTURL='' WHERE PHONENUMBER={NUMBER}"
        self.cursor.execute(replaceMenuChoice)
        replaceMenuChoice = f"UPDATE USERS SET ENDURL='' WHERE PHONENUMBER={NUMBER}"
        self.cursor.execute(replaceMenuChoice)
        self.mydb.commit()

    def deleteAll(self):
        self.checkRow()
        deleteAllQuery = f"TRUNCATE TABLE USERS"
        self.cursor.execute(deleteAllQuery)
        self.mydb.commit()


