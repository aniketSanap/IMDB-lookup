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
    index = 0
    for i in range(1, len(sys.argv)):
        query = query + sys.argv[i] + "+"
        actualQuery = actualQuery + sys.argv[i] + " "
    query = query[:-1]      #Remove the last '+'
    actualQuery = actualQuery[:-1]      #Removes the last space
    searchURL = baseURL + forSearching + query
    soup = openUrl(searchURL)
    table = soup.find('table', class_='findList' )
    print("Finding...")
    flag = 1
    urls = []
    years = []
    tds = table.find_all('td', class_='result_text')
    for td in tds:
        if td.text != "":
            years.append(td.text)

    for url in table.find_all('a'):
        if "title" in str(url.get('href')) and url.text != "":
            urls.append(url)
            index += 1
            if str(url.text.lower()) == actualQuery.lower():
                flag = 0
                print("Found: " + years[index-1])
                newURL = baseURL + url.get('href')
                print("url: " + newURL)
                soup = openUrl(newURL)
                findRating(soup)
                break    
        
    if flag:
        print("Not found")
        print ("Did you mean:")
        for i in range(0, len(urls)):
            print(i+1,". " + years[i])
        try:
            index = int(input())
            if index-1 > len(urls):
                print("Invalid input, exiting")
                sys.exit()
        except ValueError:
            print("Invalid input, exiting")
            sys.exit()
        print("Finding the rating of: " + years[index-1])
        print("url: " + str(urls[index-1].get('href')))
        newUrl = baseURL + urls[index-1].get('href')
        soup = openUrl(newUrl)
        findRating(soup)    

else:
    print("Enter the name of the movie/show")
