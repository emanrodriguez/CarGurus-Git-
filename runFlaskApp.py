from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import createMessage
account_sid = '###REPLACE WITH YOUR TWILIO SID TOKEN###'
auth_token = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
client = Client(account_sid, auth_token)
app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def twilioFlask():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)
    # EXTRACTS THE USERS PHONE NUMBER AND BODY TO RETURN TO SAME
    # PHONE AND TO CHECK THE CONDITIONAL STATEMENTS
    # IN THE CREATEMESSAGE.PY FILE
    number = request.values.get('From')
    resp = MessagingResponse()
    body = body.replace(" ", '')
    try:
        classText = createMessage.CarMessage(number, body)
        textMessage = classText.mainFunction()
    except BaseException as e:
        textMessage = """An error occurred. Please try again in about 10 seconds...\n\nError:""" + str(e)
    resp.message(textMessage)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True,threaded=False)
