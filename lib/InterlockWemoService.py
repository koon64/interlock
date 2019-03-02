from ouimeaux.environment import Environment
from xml.etree.ElementTree import fromstring
from time import sleep


class WemoService:
    def __init__(self, discover_time=1):
        self.env = Environment()
        self.env.start()
        self.env.discover(discover_time)
        device_list = self.env.list_switches()
        self.devices = []
        for name in device_list:
            self.devices.append(name)

    def get_devices(self):
        return self.devices

    def device(self, name, attempts=0):
        try:
            return WemoDevice(self.env, name)
        except:
            if attempts < 3:
                print(name + ' was not found, trying in 3 seconds')
                sleep(3)
                attempts += 1
                self.device(name, attempts)
            else:
                raise Exception(name + ' could not be found')


class WemoDevice:
    def __init__(self, env, name):
        self.env = env
        self.service = 'wemo'
        self.device_name = name
        self.id = name
        self.label = name
        self.device = self.env.get_switch(name)
        self.is_light = False
        # print(self.device.explain())
        device_info_xml = self.device.deviceinfo.GetInformation()['Information']
        root = fromstring(device_info_xml)
        for child in root:
            for sub_child in child:
                tag = sub_child.tag
                text = sub_child.text
                if tag == 'productName':
                    if text == 'Insight':
                        self.product_name = 'insight'
                        self.is_light = True
                    else:
                        self.product_name = 'unsupported'
        self.image = self.device.basicevent.GetIconURL()['URL']
        self.state = self.get_state()
        self.on = bool(int(self.get_state()))
        self.type = "switch"

    def __str__(self):
        return "[ INTERLOCK DEVICE | "+self.device_name+" | WEMO "+self.product_name.upper()+" | Turned "+("OFF", "ON")[self.get_state() == 1]+" ]"

    def set_state(self, state):
        if type(state) is bool or type(state) is int and state == 0 or state == 1:
            if state == True:
                state = 1
            # state = 1 if state else ""
            return self.device.basicevent.SetBinaryState(BinaryState=state)

    def turn_off(self):
        self.set_state(0)

    def turn_on(self):
        self.set_state(1)

    def set_brightness(self, bri):
        pass

    def get_state(self):
        state = int(self.device.basicevent.GetBinaryState()['BinaryState'])
        if state > 0:
            state = 1
        return state

    def is_on(self):
        return bool(int(self.get_state()))

    def get_power(self):
        if self.wemo_type == 'insight':
            return self.device.insight.GetPower()
        else:
            raise Exception(self.device_name+' is not an insight switch')

    def get_today_kwh(self):
        if self.wemo_type == 'insight':
            return self.device.insight.GetTodayKWH()['TodayKWH']
        else:
            raise Exception(self.device_name + ' is not an insight switch')

    def get_on_for(self):
        if self.wemo_type == 'insight':
            return self.device.insight.GetONFor()['ONFor']
        else:
            raise Exception(self.device_name + ' is not an insight switch')

    def get_today_on_time(self):
        if self.wemo_type == 'insight':
            return self.device.insight.GetTodayONTime()['TodayONTime']
        else:
            raise Exception(self.device_name + ' is not an insight switch')

