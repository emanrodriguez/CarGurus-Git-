import requests
from bs4 import BeautifulSoup


def filterChoice(numberChoice, url, entity):
    # THE 'ENDURL' IS ADDED TO CORRECTLY FILTER THE RESULTS
    if int(numberChoice) == 1:
        choice = 'BEST DEAL'
        endUrl = url + 'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=DEAL_SCORE&entitySelectingHelper.selected'
    elif int(numberChoice) == 2:
        choice = "LOWEST PRICE"
        endUrl = url + 'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=PRICE&entitySelectingHelper.selected'
    elif int(numberChoice) == 3:
        choice = "LOWEST MILEAGE"
        endUrl = url + 'showNegotiable=true&sortDir=ASC&sourceContext=carGurusHomePageModel&distance=50&sortType=MILEAGE&entitySelectingHelper.selected'
    endUrl = endUrl + entity
    return choice, endUrl


def stripUrl(url):
    # STRIPS URL TO ONLY THE MAIN LINK NEEDED
    if 'showNegotiable' in url:
        # SHOWNEGOTIABLE IS THE KEYWORD TO REMOVING THE UNNECESSARY PART OF LINK
        splitUrl = url[:url.index("show")]
        endEntity = url[url.index("Entity="):]
        tempEntity = endEntity[:8]
        for i in endEntity[8:]:
            if i.isnumeric():
                tempEntity += i
            else:
                break
    return splitUrl, tempEntity


def filteredResult(filter, listX):
    # RETURNS THE RESULT FORMATTED NEATLY
    carResult = f"{filter} \n\nCar Name : {listX[3][0]}\nCar Price: {listX[3][1]}\nMiles: {listX[3][2]}\nDeal Status: {listX[3][3]}\nMarket Ranking: {listX[3][4]}\n"
    return carResult


def addLists(carName, carPrice, carMarketDiff, prices, marketPrices, listCars, carMileage, carDealScore, carLinks):
    # Get the first 6 elements found to narrow down the results.
    for i in range(6):
        # Find the full name of current car
        nameCar = str(carName[i].text).strip()
        nameCar = nameCar[:nameCar.find('Used')]
        nameCar = nameCar[:nameCar.find("\n")]

        # Find the price of the car
        priceCar = str(carPrice[i].text).strip()
        priceCar = (priceCar[priceCar.find(''):])

        #This checks the type of deal(Good, Bad, Great) that the car price is.
        marketDeal = int(''.join([n for n in str(carMarketDiff[i].text) if n.isdigit()]))
        prices.append(marketDeal)
        priceCompare = priceCar[1:].replace(',', '')
        marketPrices.append(priceCompare)
        listCars.append(
            [nameCar, priceCar, carMileage[i].text, carDealScore[i].text, carMarketDiff[i].text, carLinks[i]])


def addLinks(soup, url):  # Returns all the links to the corresponding cars.
    carLink = soup.findAll("div", class_='bladeMediaWrapper')
    linkList = []
    for i in carLink:
        yes = (i.find("a", href=True))
        newString = url + (str(yes['href']))
        linkList.append(newString)
    return linkList


def runAll(option, starturl, endurl):
    filterString, filteredUrl = filterChoice(int(option), starturl, endurl)
    page = requests.get(filteredUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    carName = soup.find_all("div", class_="titleWrap")  # Find
    fullDeal = soup.find_all("h4", class_="listingPrice")
    carPrice = soup.find_all("span", class_="price")
    carMileage = soup.find_all("p", class_="mileage")
    carDealScore = soup.find_all("span", class_="dealLabel")
    carMarketDiff = soup.find_all("span", class_="dealDifferential")
    carLinks = addLinks(soup, filteredUrl)
    listCars = []
    prices = []
    marketPrices = []
    addLists(carName, carPrice, carMarketDiff, prices, marketPrices, listCars, carMileage, carDealScore, carLinks)
    #RETURNS THE THIRD ELEMENT BECAUSE THE THIRD ELEMENT IS THE FIRST NOT SPONSORED POSTING.
    return filteredResult(filterString, listCars), listCars[3][5]
