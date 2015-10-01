import urllib2
import json

def get_data_from_usgs():
    url = "http://waterservices.usgs.gov/nwis/iv/?site=01408205&startDT=2015-09-30&format=json&modifiedSince=P2D&parameterCd=00065"
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

def gauge_info(data):
    gauge_info = {}
    gauge_info["name"] = data["value"]["timeSeries"][0]["sourceInfo"]["siteName"]
    gauge_info ["site_code"] = data["value"]["timeSeries"][0]["sourceInfo"]["siteCode"][0]["value"]
    gauge_info["lat"] = data["value"]["timeSeries"][0]["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
    gauge_info["lng"] = data["value"]["timeSeries"][0]["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
    gauge_info["h_datum"] = data["value"]["timeSeries"][0]["sourceInfo"]["geoLocation"]["geogLocation"]["srs"]
    return gauge_info

def max_gauge_reading(data):
    readings = {}
    
    for reading in data["value"]["timeSeries"][0]["values"][0]["value"]:
        date_time = reading["dateTime"]
        gauge_height = reading["value"]
        readings[gauge_height] = date_time
        
    max_gauge_height = max(readings)
    max_gauge_time = readings[max_gauge_height]
    return {"peak_gauge_height": max_gauge_height, "peak_time": max_gauge_time}



data = get_data_from_usgs()
gauge_data = gauge_info(data)
max_reading = max_gauge_reading(data)
gauge_data.update(max_reading)
print gauge_data
