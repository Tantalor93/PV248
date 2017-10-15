import requests
import xml.etree.ElementTree as ET
r = requests.get("https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=LKTB&hoursBeforeNow=1")
print(r.content)
root = ET.fromstring(r.content)
for metar in root.find('data').findall('METAR'):
    temp = metar.find('temp_c').text
    time = metar.find('observation_time').text
    print(time, temp)