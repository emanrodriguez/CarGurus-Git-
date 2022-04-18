import datetime
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
        tempEntity = endEntity[:8]
        for i in endEntity[8:]:
            if i.isnumeric():
                tempEntity += i
            else:
                break
    return splitUrl, tempEntity, distance


def filteredResult(choice, carName, carPrice, miles, dealScore, firstLine):
    # RETURNS THE RESULT FORMATTED NEATLY
    carResult = f"{choice} \n\n" \
                f"Car Name : \n{carName}\n\n" \
                f"Car Price: \n{carPrice}\n\n" \
                f"Miles: \n{miles}\n\n" \
                f"Deal Status: \n{dealScore}\n\n" \
                f"Market Ranking: \n{firstLine}\n\n" \
                f"{datetime.datetime.now()}"
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
    return (listArray[:listArray.index("Description")]).strip()


def getCarPrice(listarray):
    variableforMiles = listarray[listarray.index("$"):listarray.index(" miles")].strip()
    price = variableforMiles[:variableforMiles.index(" - ")]
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

    # GETS CAR NAME
    name = getCarName(unfilteredString)

    # GETS PRICE
    price_miles, price = getCarPrice(unfilteredString)

    # GETS  MILES
    miles = getMiles(price_miles)

    # Check Deal Score
    dealScore = getDealScoreString(unfilteredString)

    # Get Market Rating
    marketDealPrice = getMarketRatingQuant(unfilteredString)

    carLinks = addLinks(soup, filteredUrl)
    # RETURNS THE THIRD ELEMENT BECAUSE THE THIRD ELEMENT IS THE FIRST NOT SPONSORED POSTING.
    return filteredResult(filterString, name, price, miles, dealScore, marketDealPrice), carLinks[3], distance