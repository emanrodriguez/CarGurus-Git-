![alt text](https://i.imgur.com/1MgZ54L.png)

# CarGurus-Git-
CarGurus-Git is a car listing bot powered by python. It
stores a CarGurus link which is readily accessible to
be filtered and gives end-user a real time listing via SMS
using the Twilio API.

# Test it yourself by texting "CarGurus" +1(714)360-0976


# FUTURE PLANS:

1.Allow user to opt in for daily text messages of the best deal that day according to their link.
    1. Will be done by adding another column to database for user optIn.
    1. Will use Cron for scheduling the text messages.

# Usage
## Installation Option for required packages
  1. Run the pipInstall.py file for required python packages
  1. Pip install the following
     1. BeautifulSoup
     2. requests
     3. mysql.connector
     4. twilio.rest
     5. flask
     6. twilio.twiml.messaging_response
     7. twilio.rest


## How to use :
1. Send any text to the Twilio number
    1. ![alt text](https://i.imgur.com/JqN5Z46.gif)
1. Type 'instructions' for a list of what to do
    1. <img src="https://i.imgur.com/hD0D97g.png" width="30%" height="30%">
1. After following the instructions, respond with '2'.
1. Go ahead and follow these steps:
    1. ![image](https://i.imgur.com/GhZD8qE.png)
1. Select whatever option you want!:
    1. ![image](https://i.imgur.com/A9QYrfv.png)
1. These are examples of the options:
    1. ![image](https://i.imgur.com/rZOk6pY.png)








# --------EXTRAS---------
## Why was it built?
I created this CarGurus tool to make car buying just a little easier.
I was looking for a car from the beginning of this year and was honestly 
tired of always having to manually check the CarGurus websites for any new updates.
Let alone having the website to load. I instead decided to look for ways to avoid
having to open the website and save all the different links. I wanted
to create a program where you only have to enter the link of the type of car
you want once and never have to enter it again.

## How was it built?
One of the first problems I was facing was making the program fast enough
to get the responses from the website, and I was deciding between
using a Selenium or a Requests based approach.
I ended up using requests as Javascript did not affect the results
from the website. Making runtime faster.

Now that that was done I needed to implement a way to be able to get user input
in order to filter the links as the user wanted (Lowest Priced, Newest Listing, etc.).
This was solved by using a database using a MySQL database.

Next was tracking user options and the more obvious approach was using a database.
When a user sends a text it will use a phone number the text was sent from as the
key, checking and retrieving values.

Now I needed a way to have the user communicate with the system. For this
I used Twilio's API because it is a low-cost(.02 cents/text). solution with amazing
capacity. By trial and error I could find the the users phone number and
body text and using it for the instance of the class.

Last thing needed was a way to run the program 24/7 and my solution was a
remote server, its low-cost($25/m) and is located in Ashburn, VA for the fastest connection. 
I utilized ngrok tunnels to allow listenting to the Twilio server and allow back and forth communication
with the program.


