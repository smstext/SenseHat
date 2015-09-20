from sense_hat import SenseHat
import urllib2
import json
import time

sense = SenseHat()
sense.set_rotation(180)


global lastID
lastID = 0
refresh = 10    #refresh time in secs
urlRoot = "http://api.thingspeak.com/channels/1417/"
pixels=[]
maxPixels = 64


namesToRGB = {'red': [0xFF, 0, 0],
                'green': [0, 0x80, 0],
                'blue': [0, 0, 0xFF],
                'cyan': [0, 0xFF, 0xFF],
                'white': [0xFF, 0xFF, 0xFF],
                'warmwhite': [0xFD, 0xF5, 0xE6],
                'purple': [0x80, 0, 0x80],
                'magenta': [0xFF, 0, 0xFF],
                'yellow': [0xFF, 0xFF, 0],
                'orange': [0xFF, 0xA5, 0],
                'pink': [0xFF, 0xC0, 0xCB],
                'oldlace': [0xFD, 0xF5, 0xE6]}

#retrieve and load the JSON data into a JSON object
def getJSON(url):
    jsonFeed = urllib2.urlopen(urlRoot + url)
    feedData = jsonFeed.read()
    #print feedData
    jsonFeed.close()

    data = json.loads(feedData)
    return data

#use the JSON object to identify the colour in use,
#update the last entry_id processed
def parseColour(feed):
    global lastID
    print feed["field1"]
    for name in namesToRGB.keys():
        if feedItem["field1"] == name:
            pixels.insert(0, namesToRGB[name])    #add the colour to the head
    lastID = getEntryID(feed)
    
#read the last entry_id
def getEntryID(feed):
    return int(feed["entry_id"])

#main program

#process the currently available list of colours
data = getJSON("feed.json")
for feed in data["feeds"]:
    parseColour(feed)

#check for new colour requests
while True:
    data = getJSON("field/1/last.json")
    
    if getEntryID(data) > lastID:   #Have processed this entry_id before?
        parseColour(data)
    time.sleep(refresh)

#show T as cheerlight colour
def showColour(c):
    for pixel in pixels:
        sensehat.set_pixelcolour (index, c[0], c[1], c[2])
    sensehat.show()

L = (255, 255, 0)
T = name

B = (0, 0, 0)

tree = [
B, B, B, L, L, B, B, B,
B, B, T, T, T, T, B, B,
B, L, T, T, T, T, L, B,
B, T, T, T, T, T, T, B,
L, T, T, T, T, T, T, L,
T, T, T, T, T, T, T, T,
B, B, B, T, T, B, B, B,
B, B, B, T, T, B, B, B
]
sense.set_pixels(tree)

