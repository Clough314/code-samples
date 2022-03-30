"""
    The purpose of this class is to provide
    a convenient collection of functions to harvest
    rendered (includes dynamic JS changes on webpage creation)
    HTML and write it to a local file for data ex
"""

import requests
from time import sleep
from sys import argv, exit

def main():

    if len(argv) == 1:
        _printOptionsBanner()
        exit()

    if argv[1] == "-s":
        writeHTMLFromURL(argv[2])
    elif argv[1] == "-m":
        writeHTMLFromURLs(argv[2])
    else:
        print("ERROR: Invalid option selected")
        _printOptionsBanner()

    return

def _printOptionsBanner():
    """
        Prints available user options to stdout
    """
    print("Options:"
        + "\n-s URL"
        + "\n-m Filepath containing URLs")
    return

def writeHTMLFromURL(url):
    """
        Takes a URL
        Harvests the unrendered HTML from the URL
        Writes the content to a file in the current directory
    """
    page = requests.get(url)
    _writeStringToFile(page.text, "output.html")
    return

def writeHTMLFromURLs(filepath):
    """
        Takes a file containing a list of URLs
        Harvests the unrendered HTML from each URL
        Writes the content to files in the current directory
    """
    urls = _loadFile(filepath)

    for i in range(len(urls)):
        page = requests.get(urls[i])
        _writeStringToFile(page.text, "output" + str(i) + ".html")
        sleep(1)

    return

def _writeStringToFile(string, filepath):
    """
        Provided string will be written to provided filepath
    """
    f = open(filepath, "w")
    f.write(string)
    f.close()
    return

def _loadFile(filepath):
    """
        Loads file, returns list of lines
    """
    f = open(filepath, 'r')

    lines = list(f)
    for line in list(f):
        if(line.strip() != ""):
            lines.append(line.strip())

    return lines

if __name__ == '__main__':
    main()
