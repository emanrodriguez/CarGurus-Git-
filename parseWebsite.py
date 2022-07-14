import requests
from bs4 import BeautifulSoup


def filterChoice(numberChoice, url, entity, distance):
    # THE 'ENDURL' IS ADDED TO CORRECTLY FILTER THE RESULTS
    if int(numberChoice) == 1:
        choice = 'BEST DEAL'
        endUrl = url + f'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance={distance}&sortType=DEAL_SCORE&entitySelectingHelper.selected'
    elif int(numberChoice) == 2:
        choice = "LOWEST PRICE"
        endUrl = url + f'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance={distance}&sortType=PRICE&entitySelectingHelper.selected'
    elif int(numberChoice) == 3:
        choice = "LOWEST MILEAGE"
        endUrl = url + f'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance={distance}&sortType=MILEAGE&entitySelectingHelper.selected'
    endUrl = endUrl + entity
    return choice, endUrl


def stripUrl(url):
    # STRIPS URL TO ONLY THE MAIN LINK NEEDED
    if 'showNegotiable' in url:
        # SHOWNEGOTIABLE IS THE KEYWORD TO REMOVING THE UNNECESSARY PART OF LINK
        splitUrl = url[:url.index("show")]
        endEntity = url[url.index("Entity="):]
        distance = url[url.index("distance=") + 9:url.index("&sortType")]

    return splitUrl, endEntity, distance


def filteredResult(choice, carName, carPrice, miles, dealScore, firstLine):
    # RETURNS THE RESULT FORMATTED NEATLY
    carResult = f"{choice} \n\n" \
                f"Car Name : \n{carName}\n\n" \
                f"Car Price: \n{carPrice}\n\n" \
                f"Miles: \n{miles}\n\n" \
                f"Deal Status: \n{dealScore}\n\n" \
                f"Market Ranking: \n{firstLine}\n\n"
    return carResult


def addLinks(soup, url):  # Returns all the links to the corresponding cars.
    carLink = soup.findAll("div", class_='bladeMediaWrapper')
    linkList = []
    for i in carLink:
        yes = (i.find("a", href=True))
        newString = url + (str(yes['href']))
        linkList.append(newString)
    return linkList


def getCarName(listArray):
    print(listArray)
    temp = (listArray[:listArray.index("$")]).strip()
    string = ""
    if len(temp) > 15:
        if temp[15] != " ":
            for i in range(len(temp[15:])):
                if temp[i + 15] == " ":
                    string += f"{temp[:i + 15]}\n{temp[i + 15:].strip()}"
                    break
    else:
        string = temp
    return string


def getCarPrice(listarray):
    variableforMiles = listarray[listarray.index("$"):listarray.index(" mi")+4].strip()
    splitArray = variableforMiles.split()
    price = splitArray[0]
    variableforMiles = splitArray[1]+" "+splitArray[2]
    return variableforMiles, price


def getMiles(listArray):
    return listArray[listArray.index("- ") + 2:] + " mi"


def getDealScoreString(listArray):
    if 'GOOD' in listArray.upper():
        dealScore = 'GOOD DEAL'
    elif 'GREAT' in listArray.upper():
        dealScore = 'GREAT DEAL'
    elif 'FAIR' in listArray.upper():
        dealScore = 'FAIR DEAL'
    elif 'BAD' in listArray.upper():
        dealScore = 'BAD DEAL'
    else:
        dealScore = "DEAL RATING N/A"
    return dealScore


def getMarketRatingQuant(listArray):
    if "market" in listArray:
        marketDealPrice = listArray[listArray.index("market") - 20:].strip()
    else:
        marketDealPrice = "PRICE ANALYSIS N/A"
    return marketDealPrice


def checkIfCPO(stringInput):
    cpoIndex = stringInput.index("Certified Pre-Owned: ")
    cpoCheck = stringInput[cpoIndex + 21:stringInput.index("Transmission")].strip()
    return cpoCheck


def filterArray(a: str):
    filteredArray = []
    a = a.strip("[").strip("]")
    return filteredArray


def runAll(option, starturl, endurl, distance):
    filterString, filteredUrl = filterChoice(int(option), starturl, endurl, distance)
    try:
        page = requests.get(filteredUrl)
    except:
        return "Something went wrong here"
    soup = BeautifulSoup(page.content, 'html.parser')
    checkInfo = soup.find_all('div', class_="cardBodyPadding cardBody")
    thirdElement = []
    for i in checkInfo[3]:
        if i.text.strip() == "":
            pass
        else:
            thirdElement.append(i.text.strip().replace('\n', ' ').replace("\xa0", ' '))
    unfilteredString = thirdElement[0]
    filteredArray = filterArray(unfilteredString)

    # GETS CAR NAME
    name = getCarName(unfilteredString)

    # GETS PRICE & MILES
    miles, price = getCarPrice(unfilteredString)

    # Check Deal Score
    dealScore = getDealScoreString(unfilteredString)

    # Get Market Rating
    marketDealPrice = getMarketRatingQuant(unfilteredString)

    carLinks = addLinks(soup, filteredUrl)
    # RETURNS THE THIRD ELEMENT BECAUSE THE THIRD ELEMENT IS THE FIRST NOT SPONSORED POSTING.
    returnString = filteredResult(filterString, name, price, miles, dealScore, marketDealPrice)

    return returnString, carLinks[3], distance

