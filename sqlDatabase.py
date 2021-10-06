#THIS FILE IS ONLY IF YOU WANT TO USE YOUR OWN DATABASE
#USES PRE-MADE STATEMENTS TO INSERT OR GET VALUES FROM SQLDATABASE
import mysql.connector
from twilio.rest import Client

account_sid = '###REPLACE WITH YOUR SID###'
auth_token = '###REPLACE WITH YOUR AUTHTOKEN###'
client = Client(account_sid, auth_token)

mydb = mysql.connector.connect(
    host="",
    port="",
    user="",
    password="",
    database="")
cursor = mydb.cursor()


def checkRow():
    rowCheck = f"SELECT * FROM CLIENTS"
    cursor.execute(rowCheck)
    for i in cursor:
        print(i)


def checkValid(phoneNumber):
    doesExist = f"SELECT MENUCHOICE FROM CLIENTS WHERE PHONENUMBER= {phoneNumber}"
    cursor.execute(doesExist)
    rowExists = cursor.fetchone()
    if rowExists is None:
        print(f"Now adding the number {phoneNumber}")
        insertClient(phoneNumber)
        print(f"Successfully added {phoneNumber} to the database")
        return True
    else:
        print(f"{phoneNumber} already exists!\n")
        return False


def insertClient(phoneNumber):
    addQuery = f"insert ignore into CLIENTS (phonenumber) values({phoneNumber})"
    cursor.execute(addQuery)
    mydb.commit()
    return


def fetchChoice(phoneNumber, columnName):
    addQuery = f"select {columnName} from CLIENTS where phonenumber={phoneNumber}"
    cursor.execute(addQuery)
    fetchedValue = ''
    for i in cursor:
        originalValue = str(i)
        fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',', "").replace(
            '"', "").replace("'", '')
    return fetchedValue


def fetchValue(phoneNumber, columnType):
    if columnType == 'MENUCHOICE':
        addQuery = f"select MENUCHOICE from CLIENTS where phonenumber={phoneNumber}"
    elif columnType == 'SUBMENUCHOICE':
        addQuery = f"select SUBMENUCHOICE from CLIENTS where phonenumber={phoneNumber}"
    cursor.execute(addQuery)
    fetchedValue = ''
    for i in cursor:
        originalValue = str(i)
        fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',', "").replace(
            '"', "").replace("'", '')
    return fetchedValue


def replaceValue(phonenumber, value):
    replaceQuery = f"UPDATE clients SET prevalue='{value}' WHERE phonenumber={phonenumber}"
    cursor.execute(replaceQuery)
    mydb.commit()


def dailyTasks():
    addQuery = f"SELECT PHONENUMBER,CARLINK FROM CLIENTS WHERE CARLINK!=''"
    cursor.execute(addQuery)
    test = []
    for i in cursor:
        originalValue = str(i)
        fetchedValue: str = originalValue.replace('(', '').replace('+', '').replace(')', "").replace(',', "").replace(
            '"', "").replace("'", '')
        test.append(fetchedValue)
    return test


def replaceAll(phonenumber):
    replaceQuery = f"UPDATE CLIENTS SET MENUCHOICE='0',SUBMENUCHOICE='0' WHERE phonenumber={phonenumber}"
    cursor.execute(replaceQuery)
    mydb.commit()


def replaceChoice(value, column, number):
    replaceMenuChoice = f"UPDATE CLIENTS SET {column}='{value}' WHERE PHONENUMBER={number}"
    cursor.execute(replaceMenuChoice)
    mydb.commit()


def resetValues(NUMBER):
    replaceMenuChoice = f"UPDATE CLIENTS SET MENUCHOICE='' WHERE PHONENUMBER={NUMBER}"
    cursor.execute(replaceMenuChoice)
    replaceMenuChoice = f"UPDATE CLIENTS SET SUBMENUCHOICE='' WHERE PHONENUMBER={NUMBER}"
    cursor.execute(replaceMenuChoice)
    replaceMenuChoice = f"UPDATE CLIENTS SET STARTURL='' WHERE PHONENUMBER={NUMBER}"
    cursor.execute(replaceMenuChoice)
    replaceMenuChoice = f"UPDATE CLIENTS SET ENDURL='' WHERE PHONENUMBER={NUMBER}"
    cursor.execute(replaceMenuChoice)
    mydb.commit()


def deleteAll():
    checkRow()
    deleteAllQuery = f"TRUNCATE TABLE CLIENTS"
    cursor.execute(deleteAllQuery)
    mydb.commit()

