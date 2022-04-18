import sqlDatabase
import parseWebsite
from twilio.rest import Client

account_sid = '<ReplaceWithYourAcctSID>'
auth_token = '<ReplaceWithYourAuthToken'
client = Client(account_sid, auth_token)


class CarMessage:

    def __init__(self, phoneNumber, string):
        self.phoneNumber = phoneNumber
        self.body = string
        self.distance = ""
        if "http" in string:
            self.stringURL = string
        else:
            self.stringURL = ""
        self.textMessage = ''
        self.menuChoice = sqlDatabase.fetchChoice(self.phoneNumber, 'menuchoice')
        self.subChoice = sqlDatabase.fetchChoice(self.phoneNumber, 'submenuchoice')
        self.emptyUrl = sqlDatabase.fetchChoice(self.phoneNumber, 'starturl')

    def sqlUpdate(self):
        return sqlDatabase.checkValid(self.phoneNumber)

    def sendMessage(self, phonenumber, string):
        message = client.messages.create(
            body=string,
            from_='+17143600976',
            to=phonenumber
        )

    @staticmethod
    def menuOptionTwo():
        tempStr = "Let's go ahead and enter a new link\n" \
                  "Just remember if you're having trouble " \
                  "just reply with 'instructions'."
        return tempStr

    @staticmethod
    def mainMenu():
        tempStr = f"Select an option :\n\n" \
                  f"   1. View options for previous link\n\n" \
                  f"   2. Enter link for a new car"
        return tempStr

    @staticmethod
    def subMenu():
        menu = f"Select one of the following options:\n\n" \
               f"   1. Best Deal\n\n" \
               f"   2. Low Price\n\n" \
               f"   3. Lowest Mileage"
        return menu

    def instructions(self):
        self.textMessage += f"1. For the link please go to cargurus.com " \
                            f"on your mobile/pc device.\n\n" \
                            f"2. Go ahead and input the car, model and zip code that you want.\n\n" \
                            f"3. Check off all the filters for the car that you want.\n\n" \
                            f"4A. For MOBILE click on blue 'Done' button, click 'New Search' then click the blue 'Search' button.\n\n" \
                            f"4B. For COMPUTER click on blue 'Search' button.\n\n" \
                            f"5. Copy and paste that link when asked.\n\n" \
                            f"{self.currentMenu()}"

    def menuOptionThree(self):
        self.textMessage += f"1. Sign up for Daily Notifications at 8AM PST" \
                            f"2. Un-enroll from Daily Notifications" \
                            f"3. Go Back"

    def invalidOption(self):
        print

    def currentMenu(self):
        if self.menuChoice == '':
            curr = self.mainMenu()
        elif self.menuChoice == '1':
            curr = self.subMenu()
        elif self.menuChoice == '2':
            curr = self.menuOptionTwo()
        elif self.menuChoice == '3':
            self.menuOptionThree()
        return curr

    # USED IF USER WANTS TO RESET THE CARLINK
    def resetValues(self):
        self.menuChoice = ""
        sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'starturl', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'endurl', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'distance', self.phoneNumber)
        self.textMessage += f"All values have been reset.\n\n" \
                            f"{self.currentMenu()}"
        return

    # CHECKS IF USER INPUTTED LINK IS VALID
    def validUrl(self):
        if 'showNego' in self.stringURL:
            startUrl, endUrl, distance = parseWebsite.stripUrl(self.stringURL)
            sqlDatabase.replaceChoice(startUrl, 'starturl', self.phoneNumber)
            sqlDatabase.replaceChoice(endUrl, 'endurl', self.phoneNumber)
            sqlDatabase.replaceChoice(distance, 'distance', self.phoneNumber)
            return True
        else:
            return False

    def mainFunction(self):
        lowerBody = self.body.lower()
        # ----------------- CHECKS IF USER IS NEW------------------------#
        phoneValid = sqlDatabase.checkValid(self.phoneNumber)
        if phoneValid is True:
            self.textMessage += 'Welcome to the CarGurus Bot\n\n' \
                                'Type "instructions" to see ' \
                                'how the program works!\n\n'
            self.textMessage += self.mainMenu()
            return self.textMessage
        # ---------------CHECKS IF USER INPUT IS ONE OF THE STATIC STATEMENT OPTIONS--------------------------#
        if lowerBody in ['instructions', 'help', 'reset']:
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
                if self.emptyUrl == "":
                    print("There's no link")
                    print("There's no link")
                    self.textMessage += "Looks like you haven't entered a link yet! " \
                                        "Please enter a link from Cargurus.com : \n\n" \
                                        "If you have trouble please type 'instructions'."
                    sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
                else:
                    self.textMessage += f"Welcome back!\n\n{self.subMenu()}"

            elif self.body in '2':
                sqlDatabase.replaceChoice('2', 'menuchoice', self.phoneNumber)
                self.textMessage += self.menuOptionTwo()
                return self.textMessage
            else:
                if 'https' in sqlDatabase.fetchChoice(self.phoneNumber, 'starturl'):
                    return self.currentMenu()
        # ----------------------THIS IF STATEMENT IS USED FOR OPTION ONE-----------------------------#
        elif self.menuChoice in '1':
            if self.subChoice in "" and sqlDatabase.fetchChoice(self.phoneNumber,
                                                                'starturl') != "" and self.body not in ['1', '2', '3']:
                return self.subMenu()
            elif self.subChoice != '' and self.body not in ['1', '2', '3']:
                if lowerBody in ['yes', 'no']:
                    if lowerBody in 'yes':
                        self.textMessage += f"You have selected to choose another option.\n\n{self.currentMenu()}"
                        sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
                    elif lowerBody in 'no':
                        self.textMessage += f"Going back to the main menu..."
                        self.resetValues()
                else:
                    print("In here")
                    self.textMessage += "Invalid choice, please choose one of the following bitch" + self.currentMenu()
            else:
                if self.body not in ['1', '2', '3'] and not self.validUrl():
                    print("In here")
                    self.textMessage += "Invalid choice, please choose one of the following slot" + self.currentMenu()
                else:
                    if self.emptyUrl != "":
                        sqlDatabase.replaceChoice(self.body, 'submenuchoice', self.phoneNumber)
                        startURL = sqlDatabase.fetchChoice(self.phoneNumber, 'starturl')
                        endURL = sqlDatabase.fetchChoice(self.phoneNumber, 'endurl')
                        distance = sqlDatabase.fetchChoice(self.phoneNumber, 'distance')
                        carInformation, carLink, distance = parseWebsite.runAll(self.body, startURL, endURL, distance)
                        self.sendMessage(self.phoneNumber, carInformation)
                        self.textMessage += f"{carLink}\n\n" \
                                            f"Would you like to select another option?"
                    elif self.validUrl():
                        return self.subMenu()
        elif self.menuChoice in '2':
            if self.validUrl():
                self.textMessage += f"\n You're all set, sending you back to main menu...\n\n"
                sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
                self.textMessage += self.subMenu()
                return self.textMessage
            else:
                self.textMessage += self.currentMenu()
        elif self.menuChoice in '3':
            if lowerBody in '1':
                sqlDatabase.replaceChoice('yes', 'dailynotification', self.phoneNumber)
            elif lowerBody in '2':
                sqlDatabase.replaceChoice('no', 'dailynotification', self.phoneNumber)
            elif lowerBody in '3':
                sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
            else:
                self.textMessage += f"Invalid option. Please choose from one of the following:\n "

        return self.textMessage
