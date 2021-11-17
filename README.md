# Earthquakes-worldwide (24 Hours)

An earthquake is what happens when two blocks of the earth suddenly slip past one another. The surface where they slip is called the fault or fault plane. ... Scientists can't tell that an earthquake is a foreshock until the larger earthquake happens. The largest, main earthquake is called the mainshock.

Earthquakes are the result of sudden movement along faults within the Earth. The movement releases stored-up 'elastic strain' energy in the form of seismic waves, which propagate through the Earth and cause the ground surface to shake.

The primary effects of earthquakes are ground shaking, ground rupture, landslides, tsunamis, and liquefaction. Fires are probably the single most important secondary effect of earthquakes.

Some of the common impacts of earthquakes include structural damage to buildings, fires, damage to bridges and highways, initiation of slope failures, liquefaction, and tsunami.

# Live View
![Live View](https://earthquake.usgs.gov/earthquakes/map/?extent=-78.69911,-319.92188&extent=84.9901,130.07813&settings=true)

# Python code



```python
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
          
```



# Note:
If no earthquakes have been recorded in the last hour, these sample programs will of course throw an error. You could change the URL to “…all_day.geojson” instead of “…all_hour.geojson” in that case to get it to run, but you will probably get a lot more data.
