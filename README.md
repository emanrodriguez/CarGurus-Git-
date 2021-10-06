# CarGurus-Git-
I created this CarGurus tool to make car buying just a little easier.
I was looking for a car from the beginning of this year and was honestly 
tired of always having to manually check the CarGurus websites for any new updates.
Let alone having the website to load. I instead decided to look for ways to avoid
having to open the website and save all the different links. I wanted
to create a program where you only have to enter the link of the type of car
you want once and never have to enter it again.

# How was it built?
One of the first problems I was facing was making the program fast enough
to get the responses from the website, and I was deciding between
Selenium and BeautifulSoup4. Ultimately BS4 was faster as it did not
have to load the javascript from the website. Making runtime a little faster.

Now that that was done I needed to implement a way to be able to get user input
in order to filter the links as the user wanted (Lowest Priced, Newest Listing, etc.).
This was solved by using a database using the MariaDB software.

Next was tracking user options and the database was able to solve this problem
by creating an instance of a class by using the users phonenumber. It was able to
track the previous menu option and current option.

Now I needed a way to have the user communicate with the system. For this
I used Twilio's API because it is a low-cost solution with amazing
capacity. By trial and error I could find the the users phone number and
body text and using it for the instance of the class.

Last thing needed was a way to run the program 24/7 and my solution was a
Raspberry Pi, its cost-effective and performs great. I utilized ngrok tunnels
to allow listenting to the Twilio server and allow back and forth communication
with the program.
