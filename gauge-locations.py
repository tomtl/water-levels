import urllib

"""
TITLE: USGS Gauge locations

CREATED: 3/14/2016 by Tom Lee
UPDATED:

DESCRIPTION: Gets the USGS guage coordinates and vertical datums for a State.
             Returned data is the station attributes including location coords
             and vertical datum.
             Output format is on-screen display, one row per gauge, "|" limited

STATUS: Works great.
        Future improvements could improve writing data to an output file,
        or taking multiple States instead of one at a time.
"""

# set up service url
service_url = "http://waterservices.usgs.gov/nwis/site/?"
state_code = raw_input("Enter state code (eg: MA): ")
url = service_url + urllib.urlencode({
    "format": "rdb",
    "stateCd": state_code,
    "period": "P30D"
})

# retrieve data
print "Retrieving %s" % url
raw_data = urllib.urlopen(url).read()
print "Retrieved", len(raw_data), "characters"

# display data
gauges = raw_data.split("\n")
for raw_gauge in gauges :
    gauge = raw_gauge.split("\t")
    print "|".join(gauge)
