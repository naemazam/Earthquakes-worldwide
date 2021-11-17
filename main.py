import urllib.request
import json
import re
import datetime
import matplotlib.pyplot as plt 
import math


def printResults(data):

    theJSON = json.loads(data)

    if "title" in theJSON["metadata"]:
        print("\n" + re.sub('\, ','\n',theJSON["metadata"]["title"]) + "\n")
 

    count = theJSON["metadata"]["count"]
    print (str(count) + " events recorded\n")

    georejestr = []

    for element in theJSON["features"]:
        print ("Magnitude:", round(float(element["properties"]["mag"]),1), "Event time:", datetime.datetime.fromtimestamp(element["properties"]["time"] / 1000).strftime('%Y-%m-%d %H:%M:%S') , "  Epicenter:", end = '')
        if re.sub ("\D|\.|\s", "", element["properties"]["place"]) != "":
            print(" ", element["properties"]["place"])
        elif re.search ("Near", element["properties"]["place"]) != None:
            print(" ", element["properties"]["place"])
        else:
            print("  Under", element["properties"]["place"])
        print()    
        georejestr.append([element["geometry"]["coordinates"][0:2],element["properties"]["mag"],element["properties"]["time"]])

    clr = ['fuchsia','deeppink','mediumvioletred','darkviolet','indigo','black','red']
    im = plt.imread("https://www.freepngimg.com/thumb/earth/93077-world-area-map-free-png-hq.png")
    implot = plt.imshow(im)
    for coord,m,tran in georejestr:
        plt.scatter(x=(float(coord[0])+180)*2840/360, y=(-(float(coord[1]))+94)*1850/180, c=clr[math.ceil(m-3)], s=(int((m/1.5)**4)),  alpha=(round((datetime.datetime.now().timestamp()/3600-tran /1000/ 3600)/24,1)))
    plt.savefig("plot.png")
    plt.show()


def main(): 
    urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    webUrl = urllib.request.urlopen(urlData)
    print ("Connecting to US Geological Survey API.\n\nChecking connection... Result code: " + str(webUrl.getcode()), end ="")
    if (webUrl.getcode() == 200):
        print (".\nIt's OK! Receiving data...")
        data = webUrl.read()
        printResults(data)
    else:
        print("[EN] Received error, cannot parse results\n[PL] Wystąpił błąd, nie można użyć wyników")


if __name__ == "__main__":
    main()
          