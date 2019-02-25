import requests
from lib.InterlockAPIKeys import APIKeys as k
import json


class Phone:
    def __init__(self, phone_id, refresh=False):
        keys = k()
        key = keys.get("zoos")
        if key is not False:
            url = "https://www.zoos-tech.com/api/interlock_device?key="+key+"&device_name="+phone_id
            url += "&refresh" if refresh else ""
            response = requests.get(url).content
            data = json.loads(response)
            self.phone_label = data['device_information']['name_long']
            self.phone_name = phone_id
            self.battery = data['device_information']['battery']
            self.last_online = data['device_information']['last_online']
            self.location = PhoneLocation(data['location'])

    def __str__(self):
        return "[ INTERLOCK PHONE | "+self.phone_name+" | "+self.phone_label+" | BAT: "+self.battery+"% | LAST ONLINE: "+self.last_online+" ]"

    def refresh(self):
        self.__init__(self.phone_name, True)


class PhoneLocation:
    def __init__(self, location_array):
        self.lat = location_array['lat']
        self.lng = location_array['lng']
        self.formatted_address = location_array['formatted_address']
        self.city = location_array['city']
        self.state = location_array['state']
        self.sid = location_array['sid']
        self.country = location_array['country']
        self.cid = location_array['cid']

