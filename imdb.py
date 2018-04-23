#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bs4 as bs
import sys
import urllib.request

baseURL = "http://www.imdb.com"
forSearching = "/find?q="
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

def openUrl(url):
    print("Opening url...")
    req = urllib.request.Request(url, headers=headers)
    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    return soup

def findRating(soup):
    print("Fetching rating...")
    for eachItem in soup.find_all('span'):
        if str(eachItem.get("itemprop")) == "ratingValue":
            print("Rating: " + eachItem.text)

if len(sys.argv) > 1:
    actualQuery = ""
    query = ""
    for i in range(1, len(sys.argv)):
        query = query + sys.argv[i] + "+"
        actualQuery = actualQuery + sys.argv[i] + " "
    query = query[:-1]      #Remove the last '+'
    actualQuery = actualQuery[:-1]      #Removes the last space
    searchURL = baseURL + forSearching + query
    soup = openUrl(searchURL)
    table = soup.table
    print("Finding...")
    flag = 1
    firstResult = 0
    firstUrl = ""
    firstTitle = ""
    for url in table.find_all('a'):
        if firstResult < 2:
            firstUrl = url.get('href')
            firstResult = firstResult + 1
            firstTitle = url.text
        if str(url.text.lower()) == actualQuery.lower():
            flag = 0
            print("Found")
            newURL = baseURL + url.get('href')
            print(newURL)
            soup = openUrl(newURL)
            findRating(soup)
            break
    if flag:
        print("Not found")
        if "title" in firstUrl:
            print("Using best result: " + firstTitle)
            newURL = baseURL + firstUrl
            soup = openUrl(newURL)
            findRating(soup)  

else:
    print("Enter the name of the movie/show")
