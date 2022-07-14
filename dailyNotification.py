import datetime
from twilio.rest import Client
import sqlDatabase
import parseWebsite

account_sid = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
auth_token = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
client = Client(account_sid, auth_token)


def sendMessage(phoneNumber, string):
    client.messages.create(
        body=string,
        from_='######',
        to=phoneNumber
    )


sqlObject = sqlDatabase.sqlEdit()
messageList = sqlObject.customQuery("SELECT * FROM USERS WHERE DAILYNOTIFICATION = 'yes' AND DISTANCE <> '' ")
newList = []

for i in messageList:
    try:
        temp = i.split(",")
        message, link, distance = parseWebsite.runAll('1', temp[3], temp[4], temp[5])
        message += f"\n{datetime.datetime.now()}"
        sendMessage(f"+{temp[0]}", message)
        sendMessage(f"+{temp[0]}", link.replace(" ", ''))
    except:
        print("Error")

sqlObject.endConnection()
