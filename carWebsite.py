import requests
from bs4 import BeautifulSoup


def filterChoice(numberChoice, url, entity):
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
    if 'showNegotiable' in url:
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
    carResult = f"{filter} \n\nCar Name : {listX[3][0]}\nCar Price: {listX[3][1]}\nMiles: {listX[3][2]}\nDeal Status: {listX[3][3]}\nMarket Ranking: {listX[3][4]}\n"
    return carResult


def addLists(carName, carPrice, carMarketDiff, prices, marketPrices, listCars, carMileage, carDealScore, carLinks):
    for i in range(6):
        s = str(carName[i].text).strip()
        s = s[:s.find('Used')]
        s = s[:s.find("\n")]
        name = s
        s = str(carPrice[i].text).strip()
        s = (s[s.find(''):])
        price = s
        test = int(''.join([n for n in str(carMarketDiff[i].text) if n.isdigit()]))
        prices.append(test)
        priceCompare = price[1:].replace(',', '')
        marketPrices.append(priceCompare)
        listCars.append([name, price, carMileage[i].text, carDealScore[i].text, carMarketDiff[i].text, carLinks[i]])


def addLinks(soup, url):
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
    carName = soup.find_all("div", class_="titleWrap")
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
    return filteredResult(filterString, listCars), listCars[3][5]
