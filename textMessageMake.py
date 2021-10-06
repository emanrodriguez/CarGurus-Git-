import sqlDatabase
import carWebsite


class CarMessage:

    def __init__(self, phoneNumber, string):
        self.phoneNumber = phoneNumber
        self.body = string
        self.textMessage = ''
        self.menuChoice = sqlDatabase.fetchChoice(self.phoneNumber, 'menuchoice')
        self.subChoice = sqlDatabase.fetchChoice(self.phoneNumber, 'submenuchoice')
        self.emptyUrl = sqlDatabase.fetchChoice(self.phoneNumber, 'starturl')

    def sqlUpdate(self):
        return sqlDatabase.checkValid(self.phoneNumber)

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

    def invalidOption(self):
        self.textMessage += f"You have entered an invalid option.\n\n{self.currentMenu()}"
        return self.textMessage

    def currentMenu(self):
        if self.menuChoice == '':
            curr = self.mainMenu()
        elif self.menuChoice == '1':
            curr = self.subMenu()
        elif self.menuChoice == '2':
            curr = self.menuOptionTwo()
        return curr

    # USED IF USER WANTS TO RESET THE CARLINK
    def resetValues(self):
        self.menuChoice = ""
        sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'starturl', self.phoneNumber)
        sqlDatabase.replaceChoice('', 'endurl', self.phoneNumber)
        self.textMessage += f"All values have been reset.\n\n" \
                            f"{self.currentMenu()}"
        return

    # CHECKS IF USER INPUTTED LINK IS VALID
    def validUrl(self):
        if 'https' and 'showNego' in self.body:
            startUrl, endUrl = carWebsite.stripUrl(self.body)
            sqlDatabase.replaceChoice(startUrl, 'starturl', self.phoneNumber)
            sqlDatabase.replaceChoice(endUrl, 'endurl', self.phoneNumber)
            return True
        else:
            self.textMessage += "The link you entered was invalid, try again..\n\n"
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
        if self.menuChoice == "":
            if self.body not in ['1', '2']:
                return self.invalidOption()
            elif self.body in '1':
                if self.emptyUrl == "":
                    self.textMessage += "Looks like you haven't entered a link yet! " \
                                        "Please enter a link from Cargurus.com : \n\n" \
                                        "If you have trouble please type 'instructions'."
                else:
                    self.textMessage += f"Welcome back!\n\n{self.subMenu()}"
                sqlDatabase.replaceChoice('1', 'menuchoice', self.phoneNumber)
            else:
                sqlDatabase.replaceChoice('2', 'menuchoice', self.phoneNumber)
                self.textMessage += "Let's go ahead and enter a new link\n" \
                                    "Just remember if you're having trouble " \
                                    "just reply with 'instructions'."
                return self.textMessage
        # ----------------------THIS IF STATEMENT IS USED FOR OPTION ONE-----------------------------#
        if self.menuChoice == '1':
            if self.emptyUrl == '':
                if self.validUrl():
                    self.textMessage += self.subMenu()
            elif self.subChoice != '' and self.body not in ['1', '2', '3']:
                if lowerBody in ['yes', 'no']:
                    if lowerBody in 'yes':
                        self.textMessage += f"You have selected to choose another option.\n\n{self.currentMenu()}"
                        sqlDatabase.replaceChoice('', 'submenuchoice', self.phoneNumber)
                    elif lowerBody in 'no':
                        self.textMessage += f"Going back to the main menu..."
                        self.resetValues()
                else:
                    self.textMessage += self.invalidOption()
            else:
                if self.body not in ['1', '2', '3']:
                    self.textMessage += self.invalidOption()
                else:
                    sqlDatabase.replaceChoice(self.body, 'submenuchoice', self.phoneNumber)
                    startURL = sqlDatabase.fetchChoice(self.phoneNumber, 'starturl')
                    endURL = sqlDatabase.fetchChoice(self.phoneNumber, 'endurl')
                    self.textMessage += f"{carWebsite.runAll(self.body, startURL, endURL)}\n\n" \
                                        f"Would you like to select another option?"
        # ----------------------------IF STATEMENT IS USED FOR OPTION TWO---------------------------------------#
        elif self.menuChoice == '2':
            if self.validUrl():
                self.textMessage += f"\n You're all set, sending you back to main menu...\n\n"
                sqlDatabase.replaceChoice('', 'menuchoice', self.phoneNumber)
                self.textMessage += self.mainMenu()
        return self.textMessage
