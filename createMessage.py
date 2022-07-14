import datetime

import sqlDatabase as sqlFile
import parseWebsite
from twilio.rest import Client
import traceback

account_sid = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
auth_token = '###REPLACE WITH YOUR TWILIO AUTH TOKEN###'
client = Client(account_sid, auth_token)


class CarMessage:

    def __init__(self, phoneNumber, string):
        self.sqlDatabase = sqlFile.sqlEdit()
        self.phoneNumber = phoneNumber
        self.body = string
        self.distance = self.sqlDatabase.fetchChoice(self.phoneNumber, 'distance')
        if "http" in string:
            self.stringURL = string
        else:
            self.stringURL = ""
        self.textMessage = ''
        self.menuChoice = self.sqlDatabase.fetchChoice(self.phoneNumber, 'menuchoice')
        self.subChoice = self.sqlDatabase.fetchChoice(self.phoneNumber, 'submenuchoice')
        self.databaseUrl = self.sqlDatabase.fetchChoice(self.phoneNumber, 'starturl')

    def sqlUpdate(self):
        return self.sqlDatabase.checkValid(self.phoneNumber)

    def sendMessage(self, string):
        message = client.messages.create(
            body=string,
            from_='+######',
            to=self.phoneNumber
        )

    def menuOptionTwo(self):
        self.textMessage += "Enter a new CarGurus link\n" \
                            "Reply with 'instructions'.\n" \
                            "If you require assistance\n\n "

    def mainMenu(self):
        self.textMessage += f"Select an option :\n\n" \
                            f"   1. View options for previous link\n\n" \
                            f"   2. Enter link for a new car\n\n" \
                            f"   3. Edit Daily Notifications"

    def subMenu(self):
        self.textMessage += f"Select one of the following options:\n\n" \
                            f"   1. Best Deal\n\n" \
                            f"   2. Low Price\n\n" \
                            f"   3. Lowest Mileage"

    def instructions(self):
        self.textMessage += f"1. For the link please go to cargurus.com " \
                            f"on your mobile/pc device.\n\n" \
                            f"2. Go ahead and input the car, model and zip code that you want.\n\n" \
                            f"3. Check off all the filters for the car that you want.\n\n" \
                            f"4A. For MOBILE click on blue 'Done' button, click 'New Search' then click the blue 'Search' button.\n\n" \
                            f"4B. For COMPUTER click on blue 'Search' button.\n\n" \
                            f"5. Copy and paste that link when asked.\n\n"
        self.currentMenu()

    def menuOptionThree(self):
        self.textMessage += f"Daily Notification Settings\n\n\n" \
                            f"1. Sign up for Daily Notifications at 8AM PST\n\n" \
                            f"2. Un-enroll from Daily Notifications\n\n" \
                            f"3. Go Back"

    def currentMenu(self):
        if self.menuChoice == '':
            self.mainMenu()
        elif self.menuChoice == '1':
            self.subMenu()
        elif self.menuChoice == '2':
            self.menuOptionTwo()
        elif self.menuChoice == '3':
            self.menuOptionThree()
        else:
            pass

    def goMainMenu(self):
        self.sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
        self.sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
        self.mainMenu()

    # USED IF USER WANTS TO RESET THE CARLINK
    def resetValues(self):
        self.menuChoice = ""
        self.sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
        self.sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
        self.sqlDatabase.replaceChoice('', 'starturl', self.phoneNumber)
        self.sqlDatabase.replaceChoice('', 'endurl', self.phoneNumber)
        self.sqlDatabase.replaceChoice('', 'distance', self.phoneNumber)
        self.textMessage += f"All values have been reset.\n\n"
        self.currentMenu()
        return

    # CHECKS IF USER INPUTTED LINK IS VALID
    def validUrl(self):
        if 'showNego' in self.stringURL:
            startUrl, endUrl, distance = parseWebsite.stripUrl(self.stringURL)
            self.sqlDatabase.replaceChoice(startUrl, 'starturl', self.phoneNumber)
            self.sqlDatabase.replaceChoice(endUrl, 'endurl', self.phoneNumber)
            self.sqlDatabase.replaceChoice(distance, 'distance', self.phoneNumber)
            return True
        else:
            return False

    def mainFunction(self):
        lowerBody = self.body.lower()
        self.textMessage += "CARGURUS BOT\n-----------------\n\n"
        # ----------------- CHECKS IF USER IS NEW------------------------#
        phoneValid = self.sqlDatabase.checkValid(self.phoneNumber)
        if phoneValid is True:
            self.textMessage += 'Welcome to the CarGurus Bot\n' \
                                'Created by Emmanuel Rodriguez\n\n' \
                                'Type "instructions" to see ' \
                                'how the program works!\n\n'
            self.mainMenu()
            return self.textMessage
        # ---------------CHECKS IF USER INPUT IS ONE OF THE STATIC STATEMENT OPTIONS--------------------------#
        if lowerBody in 'main menu':
            self.goMainMenu()
            return self.textMessage
        elif lowerBody in ['instructions', 'help', 'reset']:
            if lowerBody in 'instructions':
                self.instructions()
                return self.textMessage
            elif lowerBody in 'help':
                self.textMessage += "Looks like you need help!\n\n"
                self.currentMenu()
                return self.textMessage
            elif lowerBody in 'reset':
                self.resetValues()
                return self.textMessage

        # ------------------------------------------------------------------#
        if self.menuChoice in "":
            if self.body in '1':
                self.sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
                if self.databaseUrl == "":
                    self.textMessage += "Looks like you haven't entered a link yet! " \
                                        "Enter a link from Cargurus.com : \n\n" \
                                        "If you have trouble type 'instructions'."
                else:
                    self.textMessage += f"Welcome back!\n\n"
                    self.subMenu()


            elif self.body in '2':
                self.sqlDatabase.replaceChoice('2', 'menuchoice', self.phoneNumber)
                self.menuOptionTwo()
                return self.textMessage

            elif self.body in '3':
                self.sqlDatabase.replaceChoice('3', 'menuchoice', self.phoneNumber)
                self.menuOptionThree()
                return self.textMessage
            else:
                self.textMessage += "Input is invalid\n"
                self.mainMenu()
        # ----------------------THIS IF STATEMENT IS USED FOR OPTION ONE-----------------------------#
        elif self.menuChoice in '1':
            if self.databaseUrl == "":
                if not self.validUrl():
                    self.textMessage += """You entered an incorrect URL. Type'instructions' if you need help getting the correct link"""
                else:
                    self.textMessage += "URL is Valid\n\n"
                    self.subMenu()
            elif self.databaseUrl != "":
                if self.subChoice == "":
                    if self.body in ['1', '2', '3']:
                        self.sqlDatabase.replaceChoice(self.body, 'submenuchoice', self.phoneNumber)
                        parsedResult, link, distance = parseWebsite.runAll(self.body, self.databaseUrl,
                                                                           self.sqlDatabase.fetchChoice(
                                                                               self.phoneNumber,
                                                                               'endurl'),
                                                                           self.sqlDatabase.fetchChoice(
                                                                               self.phoneNumber,
                                                                               'distance'))
                        parsedResult += f"\nWould you like to select another option? Reply with 'yes' or 'no'\n\n{datetime.datetime.now()}"
                        self.sendMessage(parsedResult)
                        return link
                    else:
                        self.textMessage += "You have chosen an invalid option\n\n"
                        self.currentMenu()
                        return self.textMessage

                elif self.subChoice != "":
                    if lowerBody in ['yes', 'no']:
                        if lowerBody in 'yes':
                            self.sqlDatabase.replaceChoice('', "submenuchoice", self.phoneNumber)
                            self.subMenu()
                        else:
                            self.goMainMenu()
                    else:
                        self.textMessage += """You have chosen an invalid option.\n\nReply with "yes" or "no" to """ \
                                            "choose another option. """
                        return self.textMessage


        elif self.menuChoice in '2':
            if self.validUrl():
                self.textMessage += f"You're all set, sending you back to main menu...\n\n"
                self.sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
                self.subMenu()
                return self.textMessage
            else:
                self.textMessage += "Invalid URL has been entered\n\n"
                self.currentMenu()



        elif self.menuChoice in '3':
            if lowerBody in '1':
                self.sqlDatabase.replaceChoice('yes', 'dailynotification', self.phoneNumber)
                self.textMessage += "You are now enrolled for daily notifications!\n\n"
                self.sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
            elif lowerBody in '2':
                self.sqlDatabase.replaceChoice('no', 'dailynotification', self.phoneNumber)
                self.textMessage += "You are now un-enrolled if not already for daily notifications.\nNow going " \
                                    "back to main menu.\n"
                self.sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
                self.sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
            elif lowerBody in '3':
                self.sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
            else:
                self.textMessage += f"Invalid option.\nChoose from one of the following\n"
                self.currentMenu()
                return self.textMessage
            self.mainMenu()
        self.sqlDatabase.endConnection()
        return self.textMessage