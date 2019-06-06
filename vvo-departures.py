from urllib import request
import json
import re
import time

# --> For use behind proxy (proxy.xyz.de:port), set protocol below
proxy_host = ''
# --> For legal reasons, the publication of the API is not permitted. Please ask the Verkehrsbund Oberelbe (vvo-online.de).
webAPI = ''

class VVO_Departures():
    list_station = []

    def urlrequest(stop_id):
        stop_url_request = request.Request(webAPI+stop_id)
        # --> For use behind proxy (set proxy url above)
        #stop_url_request.set_proxy(proxy_host, 'http')
        return stop_url_request

    def urlopen(stop_id):
        stop_url_request = VVO_Departures.urlrequest(stop_id)
        stop_url_open = request.urlopen(stop_url_request)
        return stop_url_open

    def urlread(stop_id):
        stop_url_open = VVO_Departures.urlopen(stop_id)
        stop_url_read = stop_url_open.read().decode('utf-8')
        return stop_url_read

    def urljson(stop_id):
        stop_url_read = VVO_Departures.urlread(stop_id)
        stop_url_data = json.loads(stop_url_read)
        return stop_url_data

    def loop_departures(stop_id):
        stop_url_json = VVO_Departures.urljson(stop_id)
        i = 0
        while i < 10:
            stop_tupel = ()
            linename = stop_url_json['Departures'][i]['LineName']
            direction = stop_url_json['Departures'][i]['Direction']
            try:
                timestamp_vvo = stop_url_json['Departures'][i]['RealTime']
            except:
                timestamp_vvo = stop_url_json['Departures'][i]['ScheduledTime']
            timestamp_vvo = re.findall("\/Date\(([0-9]*)-[0-9]*\)\/", timestamp_vvo)[0]
            timestamp_vvo = int(timestamp_vvo) / 1000.0
            timestamp_now = int(time.time())
            waittime = int((timestamp_vvo - timestamp_now) / 60)
            stop_tupel = (linename, direction, waittime)
            if(stop_id == ""): #insert stopID
                VVO_Departures.list_station.append(stop_tupel)
            else:
                print("Wrong stop_id or WebAPI down!")
            i += 1
        return

    def get_departures():
        VVO_Departures.loop_departures("") #insert stopID
        return VVO_Departures.list_station


if __name__ == '__main__':
    station_one = VVO_Departures.get_departures()
    print(station_one)