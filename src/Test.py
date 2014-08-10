__author__ = 'vince_000'

import urllib2
from bs4 import BeautifulSoup
import csv
import pickle

def resultSetToText(resultSet):
    # removing <> tags, changing the encoding to ASCII
    intermediateSet=[result.getText().encode('ascii', 'ignore') for result in resultSet]
    return [" ".join(result.split()) for result in intermediateSet]

# on the jamrock entertainment website, 2008 and 2009 are formatted slightly differently.
years=range(1950, 2011)
years.remove(2008)
years.remove(2009)


def downloadBillboardTop100(year):
    top100text=urllib2.urlopen("http://www.jamrockentertainment.com/billboard-music-top-100-songs-listed-by-year/top-100-songs-"+str(year)+".html").read()
    rawTable=BeautifulSoup(top100text).find(id="BODYTEXT")
    tableAsRows=rawTable.find_all("tr")
    tableAsCells=map(lambda x: x.find_all("td"), tableAsRows)
    processedTable=map(resultSetToText, tableAsCells)
    return processedTable

def exportBillboardTop100(year):
    with open("top100_"+str(year)+".csv", "wb") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for x in billboardTop100Dict[year]:
            writer.writerow(x)

# the code below

##top100byYear=dict()
##for year in years:
##    billboardTop100Dict[year]=downloadBillboardTop100(year)
##    exportBillboardTop100(year)
##
##pickle.dump(billboardTop100Dict, open("top100dict.pickle", "wb"))

top100byYear=pickle.load(open("top100dict.pickle", "rb"))

##top100_1950=[]
##with open('top100_1950.csv', 'rb') as csvfile:
##    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
##    for row in reader:
##        top100_1950.append(row)

class rankedSong:
    def __init__(self, title, artist, year, position):
        self.title=title
        self.artist=artist
        metroEndString=(title+"-lyrics-"+artist).replace(" ", "-").lower()
        self.metroURL = "http://www.metrolyrics.com/"+metroEndString+".html"
        self.year=year
        self.position=position
        try:
            self.lyric=metroDownloader(self.metroURL)
            self.hasLyric=True
        except urllib2.HTTPError:
            self.lyric=""
            self.hasLyric=False

def metroLyricsProcessor(text):
    startString='<div id="lyrics-body-text">'
    endString='</div>'
    startPos=text.find(startString)+len(startString)
    endPos=text.find(endString, startPos)
    rawSong=text[startPos:endPos]
    processedSong=rawSong.replace('<br/>', '').replace('</p>', '').replace("<p class='verse'>", '\n').strip()
    return processedSong

def metroDownloader(url):
    text=urllib2.urlopen(url).read()
    return metroLyricsProcessor(text)

##asRankedSong=dict()
##for year in years:
##    for position in range(len(top100byYear[year])):
##        print (year, position)
##        asRankedSong[(year,int(top100byYear[year][position][0]))]=rankedSong(
##            top100byYear[year][position][1],
##            top100byYear[year][position][2],
##            year,
##            int(top100byYear[year][position][0])
##            )
##
##pickle.dump(asRankedSong, open("songdict.pickle", "wb"))

asRankedSong=pickle.load(open("songdict.pickle", "rb"))

for song in asRankedSong.itervalues():
    if not song.hasLyric:
        print (song.title, song.artist)
        
##xList=[]
##yList=[]
##cList=[]

##for song in asRankedSong.itervalues():
##    xList.append(song.year)
##    yList.append(song.position)
##    if song.hasLyric:
##        cList.append([0, 1, 0]) # color green
##    else:
##        cList.append([1, 0, 0])
##
##import matplotlib.pyplot as plt
##plt.scatter(xList, yList, c=cList, alpha=0.5)
##plt.show()

##xList=[]
##yList=[]
##cList=[]

##for song in asRankedSong.itervalues():
##    xList.append(song.year)
##    yList.append(song.position)
##    if song.hasLyric:
##        cList.append([0, 1, 0]) # color green
##    else:
##        cList.append([1, 0, 0])
##
##import matplotlib.pyplot as plt
##plt.scatter(xList, yList, c=cList, alpha=0.5)
##plt.show()
