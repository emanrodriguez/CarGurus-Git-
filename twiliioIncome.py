from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import textMessageMake

account_sid = '###########REPLACE WITH YOUR SID########'
auth_token = '###########REPLACE WITH YOUR AUTHTOKEN########'
client = Client(account_sid, auth_token)
app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)
    number = request.values.get('From')
    resp = MessagingResponse()
    body = body.lower().replace(" ", '')
    classText = textMessageMake.CarMessage(number, body)
    textMessage = classText.mainFunction()
    resp.message(textMessage)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
