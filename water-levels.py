import urllib2
import urllib
import json

"""
TITLE: USGS Gauge peak levels

CREATED: 10/1/2015 by Tom Lee
UPDATED: 3/14/2016 by Tom Lee

DESCRIPTION: Gets the peak USGS guage levels for a State.
             Returned data is the peak height for every gauge in the state.
             Before running, modify the query_args in get_data_from_usgs
             Output format is on-screen display, one row per gauge, "|" limited

STATUS: Works great.
        Future improvements could improve writing data to an output file,
        prompting for the date query_arg,
        or taking multiple States instead of one at a time.
"""

def get_data_from_usgs(state_code):
    query_args = {"stateCd": state_code,
                  "startDT":"2016-03-11",
                  "format": "json",
                  "modifiedSince": "P5D",
                  "parameterCd": "00065"}

    encoded_args = urllib.urlencode(query_args)
    url = "http://waterservices.usgs.gov/nwis/iv/?" + encoded_args
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

def gauge_info(data):
    gauge_info = {}
    gauge_info["name"] = data["siteName"]
    gauge_info ["site_code"] = data["siteCode"][0]["value"]
    gauge_info["lat"] = data["geoLocation"]["geogLocation"]["latitude"]
    gauge_info["lng"] = data["geoLocation"]["geogLocation"]["longitude"]
    gauge_info["h_datum"] = data["geoLocation"]["geogLocation"]["srs"]
    gauge_info["site_type"] = data["siteProperty"][0]["value"]
    return gauge_info

def max_gauge_reading(data):
    readings = {}

    for reading in data[0]["value"]:
        date_time = reading["dateTime"]
        gauge_height = float(reading["value"])
        readings[gauge_height] = date_time

    try :
        max_gauge_height = max(readings)
        max_gauge_time = readings[max_gauge_height]
    except :
        max_gauge_height = -999999
        max_gauge_time = 0

    return {"peak_gauge_height": max_gauge_height, "peak_time": max_gauge_time}

def summarize_gauge(gauge_data):
    gauge_info_data = gauge_data["sourceInfo"]
    gauge_reading_data = gauge_data["values"]

    gauge_summary_data = gauge_info(gauge_info_data)
    max_reading = max_gauge_reading(gauge_reading_data)
    gauge_summary_data.update(max_reading)
    return gauge_summary_data

def gauge_summary_output_line(gauge):
    gauge_data = [str(gauge["site_code"]),
                  str(gauge["name"]),
                  str(gauge["lat"]),
                  str(gauge["lng"]),
                  str(gauge["h_datum"]),
                  str(gauge["site_type"]),
                  str(gauge["peak_gauge_height"]),
                  str(gauge["peak_time"])]
    return "|".join(gauge_data)


state_code = raw_input("Enter state (eg: NJ): ")
data = get_data_from_usgs(state_code)

count = 0

for gauge in data["value"]["timeSeries"]:
    count += 1
    gauge_summary = summarize_gauge(gauge)
    print gauge_summary_output_line(gauge_summary)

print count, " gauges"
