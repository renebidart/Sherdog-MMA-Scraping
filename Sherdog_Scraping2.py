import os
import collections
import datetime
import urllib
from urllib2 import urlopen
from bs4 import BeautifulSoup
from lxml import html
import requests
import urllib2
import re
import csv
import time
from random import randint




#Get Event List
r = requests.get("http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2")
data = r.text
soup = BeautifulSoup(data)

#chart has a table tag with class event
eventTable = soup.find("table", attrs={"class" : "event"})

#Removes some unnecessary stuff?
eventRows = eventTable.find_all("tr")

events = []
fightList=[]

#extract event name, id number and date from the unformatted list
for row in eventRows[1:]:
    cells = row.find_all("td")
    id = cells[1].a['href'].rpartition("-")[2]
    month = row.find("span", {"class" : "month"}).string
    day = row.find("span", {"class" : "day"}).string
    year = row.find("span", {"class" : "year"}).string
    tempDate = "%s %s, %s" % (month, day, year)
    eventDate = datetime.datetime.strptime(tempDate, '%b %d, %Y')
    name = str(cells[1].find("span").getText())
    location = str(cells[2].find_all(text=True)[0].string)
    link=cells[1].a['href']
    events.append({'ID' : id, 'date' : eventDate, 'name': name, 'location': location, 'Link' : link})



#Get event fights
fullFighterList = []
fighterList = []
a=0
for row in events[0:]:
    url="http://www.sherdog.com" +row["Link"]
    print(row["Link"])
    succeeded = False
    while not succeeded:
        try:
            r = requests.get(url)
            succeeded = True
        except Exception:
            continue
    data = r.text
    soup = BeautifulSoup(data)
    fighterRaw=soup.find_all('a',
    attrs={'href': re.compile("^/fighter/")})
    for row in fighterRaw[3:]:
        cells = row.find_all("span")
        if len(cells)>0:       
            id = row['href'].rpartition("-")[2]
            name=str(row.getText())
            link=row['href']
            fighterList.append({'ID' : id, 'name': name, 'Link' : link})
            print(a)
            a=a+1
    fullFighterList.extend(fighterList)
#full list of all fighters in the UFC
fullFighterListND=[dict(t) for t in set([tuple(d.items()) for d in fullFighterList])]
    



#Get fighter info (loop, function is below)
a=0
fighterDetail=[]
for row in fullFighterListND[0:]:
    url="http://www.sherdog.com" +row['Link']
    succeeded = False
    while not succeeded:
        try:
            r = requests.get(url)
            succeeded = True
        except Exception:
            continue
    data = r.text
    soup = BeautifulSoup(data)
    bio = soup.find("div", {"class" : "module bio_fighter vcard"})
    try:
        name = str(bio.h1.find(text=True))
    except Exception:
        name = ""    
    try:
        age= bio.find("span", {"class" : "item birthday"})
        age=str(age.find("strong").string)
    except Exception:
        age = ""
    try:
        association = bio.h5.find("span", {"itemprop": "name"})
        association = str(association.find(text=True))
    except Exception:
        association = ""
    try:           
        height= bio.find("span", {"class" : "item height"})
        height=str(height.findAll(text=True)[3]).replace('\n', '').lstrip().rstrip()
    except Exception:
        height = ""    
    try:   
        weight= bio.find("span", {"class" : "item weight"})
        weight=str(weight.findAll(text=True)[3]).replace('\n', '').lstrip().rstrip()
    except Exception:
        weight = ""
    try:
        location = bio.find("span", {"class" : "item birthplace"})
    except Exception:
        location = ""
    try:
        city= str(location.findAll(text=True)[2].strip())
    except Exception:
        city = ""  
    try: 
        country= str(location.strong.string)
    except Exception:
        country= "" 
    try: 
        wclass= str(bio.h6.strong.string)
    except Exception:
        wclass= ""
    print(a) 
    a=a+1
    fighterDetail.append({'''name''': name, '''Link''' : url, '''age''' : age, '''association''': association,
        '''height''' : height, '''weight''' : weight, ''''city''':city, '''weight''':weight,
         '''wclass''':wclass})



#function for getting fighter details:
a=0
def getFighterDetails(url):
    details=[]
    url="http://www.sherdog.com" +url
    succeeded = False
    while not succeeded:
        try:
            r = requests.get(url)
            succeeded = True
        except Exception:
            continue
    data = r.text
    soup = BeautifulSoup(data)
    bio = soup.find("div", {"class" : "module bio_fighter vcard"})
    try:
        name = str(bio.h1.find(text=True))
    except Exception:
        name = ""    
    try:
        age= bio.find("span", {"class" : "item birthday"})
        age=str(age.find("strong").string)
    except Exception:
        age = ""
    try:
        association = bio.h5.find("span", {"itemprop": "name"})
        association = str(association.find(text=True))
    except Exception:
        association = ""
    try:           
        height= bio.find("span", {"class" : "item height"})
        height=str(height.findAll(text=True)[3]).replace('\n', '').lstrip().rstrip()
    except Exception:
        height = ""    
    try:   
        weight= bio.find("span", {"class" : "item weight"})
        weight=str(weight.findAll(text=True)[3]).replace('\n', '').lstrip().rstrip()
    except Exception:
        weight = ""
    try:
        location = bio.find("span", {"class" : "item birthplace"})
    except Exception:
        location = ""
    try:
        city= str(location.findAll(text=True)[2].strip())
    except Exception:
        city = ""  
    try: 
        country= str(location.strong.string)
    except Exception:
        country= "" 
    try: 
        wclass= str(bio.h6.strong.string)
    except Exception:
        wclass= ""
    try: 
        birthday= bio.find("span", {"class" : "item birthday"})
        birthday= str(birthday.findAll(text=True)[1])
        birthday= datetime.datetime.strptime(birthday, '%Y-%m-%d')

    except Exception:
        birthday= ""

    print(a) 
    details=({'''name''': name, '''Link''' : url, '''age''' : age, '''association''': association,
        '''height''' : height, '''weight''' : weight, '''city''':city, '''country''':country,
        '''weight''':weight,'''wclass''':wclass, '''birthday''':birthday})
    return details


a=0

#Full Fight List-list for prediction:
for row in fullFighterListND[0:]:
    url="http://www.sherdog.com" +row['Link']
    succeeded = False
    while not succeeded:
        try:
            r = requests.get(url)
            succeeded = True
        except Exception:
            continue
    data = r.text
    soup = BeautifulSoup(data)

    fightEven = soup.find_all("tr", {"class" : "even"})
    fightOdd = soup.find_all("tr", {"class" : "odd"})

    rawFights=[]
    rawFights = fightEven+fightOdd
    print(a)
    a=a+1
    #Loop through fights in fighter profile
    import time
    time.sleep(randint(4,17))
    for fight in rawFights[0:]:
        date=str(fight.find('span', {'class':'sub_line'}).string)
        DATE=datetime.datetime.strptime(date, '%b / %d / %Y')
        fighterA=row['name']
        fighterB=str(fight.find_all(text=True)[3])
        outcomeWRTA=str(fight.find_all(text=True)[1])
        outcomeDetail=str(fight.find_all(text=True)[8])
        round=str(fight.find_all(text=True)[11])
        time=str(fight.find_all(text=True)[13])
        ref=str(fight.find_all(text=True)[9])
        fighterAUrl=row['Link']
        fighterAheight=getFighterDetails(fighterAUrl)['height']
        fighterACurClass=getFighterDetails(fighterAUrl)['wclass']
        fighterAassociation=getFighterDetails(fighterAUrl)['association']
        fighterAcity=getFighterDetails(fighterAUrl)['city']
        fighterAcountry=getFighterDetails(fighterAUrl)['country']
        try: 
            fighterAAge=(DATE-getFighterDetails(fighterAUrl)['birthday']).days
        except Exception:
            fighterAAge= ""
        fighterBUrl=str(fight.find('a')['href'])
        fighterBheight=getFighterDetails(fighterBUrl)['height']
        fighterBCurClass=getFighterDetails(fighterBUrl)['wclass']
        fighterBassociation=getFighterDetails(fighterBUrl)['association']
        fighterBcity=getFighterDetails(fighterBUrl)['city']
        fighterBcountry=getFighterDetails(fighterBUrl)['country']
        try: 
            fighterBAge=(DATE-getFighterDetails(fighterBUrl)['birthday']).days
        except Exception:
            fighterBAge= ""
        fightList.append({'''date''' : date, '''fighterA''':fighterA, '''fighterB''': fighterB, 
        '''outcomeWRTA''' : outcomeWRTA, '''outcomeDetail''':outcomeDetail,  
        '''round''':round, '''time''':time, '''ref''':ref,
        '''fighterAheight''':fighterAheight, '''fighterACurClass''':fighterACurClass, 
        '''fighterAassociation''':fighterAassociation, '''fighterAcity''':fighterAcity, 
        '''fighterAcountry''':fighterAcountry, '''fighterAAge''':fighterAAge,
        '''fighterBheight''':fighterBheight, '''fighterBCurClass''':fighterBCurClass, 
        '''fighterBassociation''':fighterBassociation, '''fighterBcity''':fighterBcity, 
        '''fighterBcountry''':fighterBcountry, '''fighterBAge''':fighterBAge})

#Save fightList as a csv:

fightListTest=fightList

import csv



with open('/Users/user/documents/Honors Project/UFC data/fightList.csv', 'a') as outcsv:   
    #configure writer to write standard csv file
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['''date''' , '''fighterA''', '''fighterB''', '''outcomeWRTA''' , 
        '''outcomeDetail''',  '''round''', '''time''', '''ref''','''fighterAheight''',
        '''fighterACurClass''', '''fighterAassociation''', '''fighterAcity''', 
        '''fighterAcountry''', '''fighterAAge''','''fighterBheight''', '''fighterBCurClass''', 
        '''fighterBassociation''', '''fighterBcity''', 
        '''fighterBcountry''', '''fighterBAge'''])
    for item in fightListTest:
        #Write item to outcsv
        writer.writerow([item['date'], item['fighterA'], item['fighterB'],item['outcomeWRTA'],
         item['outcomeDetail'],item['round'],item['time'], item['ref'], item['fighterAheight'],
         item['fighterACurClass'], item['fighterAassociation'], item['fighterAcity'],
         item['fighterAcountry'], item['fighterAAge'], item['fighterBheight'],item['fighterBCurClass'], 
         item['fighterBassociation'],item['fighterBcity'], item['fighterBcountry'],
         item['fighterBAge']])









