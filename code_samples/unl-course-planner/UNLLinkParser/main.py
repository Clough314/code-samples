from bs4 import BeautifulSoup

def main():
    html = loadFileAsString('output.html')
    soup = getSoupFromHTML(html)
    # print(soup.prettify())

    relevantTagContainers = soup.find_all('div', {"id" : "items"})

    extractLinks(str(relevantTagContainers[0]))

    return

def extractLinks(HTML):
    sectionSoup = getSoupFromHTML(HTML)

    links = sectionSoup.find_all('a')
    majorOnly = list()
    minorOnly = list()
    # both = list()

    for link in links:
        children = list(link.children)
        if len(children) == 1:
            majorOnly.append(children[0].text + ", https://catalog.unl.edu/" + link.get('href'))
            continue

        if children[1].text.lower() == "Minor Only":
            minorOnly.append(children[0].text + ", https://catalog.unl.edu/" + link.get('href'))
            continue

        majorOnly.append(children[0].text + ", https://catalog.unl.edu/" + link.get('href'))
        minorOnly.append(children[0].text + ", https://catalog.unl.edu/" + link.get('href'))
        # print(link.get('href'))

    print("MAJOR LINKS")
    printCollection(majorOnly)

    print()

    print("MINOR LINKS")
    printCollection(minorOnly)

    return

def printCollection(collection):
    for item in collection:
        print(item)

    return

def loadFileAsString(filepath):
    """
        Returns entire file's
        text as a single string
    """
    f = open(filepath, 'r')
    return f.read()

def getSoupFromHTML(HTML):
    """
        IMPORT REQUIREMENTS:
        from bs4 import BeautifulSoup

        Returns soup object which can be used
        to traverse the HTML from the given URL
    """

    #Parser choices: html.parser, html5lib, lxml or none
    soupObj = BeautifulSoup(HTML, 'html.parser')
    return soupObj

if __name__ == '__main__':
    main()
