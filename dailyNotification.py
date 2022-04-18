import time
from twilio.rest import Client
import sqlDatabase
import parseWebsite
import createMessage


def sendMessage(phonenumber, string):
    message = client.messages.create(
        body=string,
        from_='',
        to=phonenumber
    )


account_sid = 'ACc9fd4c22cd5a9edad5deaf14ae4d6086'
auth_token = '910df4d587249ae2d5be6ea1cfb58e76'
client = Client(account_sid, auth_token)
# tempList = sqlDatabase.customQuery("SELECT * FROM USERS WHERE STARTURL IS NOT NULL AND TRIM(STARTURL) <> '' ")
tempList = sqlDatabase.customQuery("SELECT * FROM USERS WHERE DAILYNOTIFICATION IS NOT NULL AND TRIM(STARTURL) <> '' ")
newList = []

for i in tempList:
    try:
        temp = i.split(",")
        message, link, distance = parseWebsite.runAll('1', temp[3], temp[4], temp[5])
        print(message)
        print(link.replace(" ", ''))
        # sendMessage(f"+{temp[0]}", message)
        # sendMessage(f"+{temp[0]}", link.replace(" ",''))
        time.sleep(5)
    except:
        print("Error")
