from phue import Bridge


class HueService:
    def __init__(self, bridge_ip):
        self.connected = False
        try:
            self.bridge = Bridge(bridge_ip)
            self.connected = True
            self.bridge.connect()
            self.hue_info = self.bridge.get_api()
            self.lights = []
            for light_numb in self.hue_info['lights']:
                light = self.hue_info['lights'][light_numb]
                light_obj = HueLight(self, light_numb, light)
                self.lights.append(light_obj)
        except:
            pass

    def get_lights(self):
        return self.lights

    def refresh_lights(self):
        print('refreshing lights')
        self.hue_info = self.bridge.get_api()
        for light_numb in range(0, len(self.lights)):
            self.lights[light_numb].refresh()



class HueLight:
    def __init__(self, hue, light_id, light):
        self.bridge = hue.bridge
        self.hue_obj = hue
        self.service = 'hue'
        self.id = int(light_id)
        self.reachable = light['state']['reachable']
        self.on = light['state']['on']
        self.label = light['name']
        self.is_light = True
        self.product_name = light['productname']
        self.brightness = light['state']['bri'] / 255
        self.xy = light['state']['xy']
        self.hue = light['state']['hue']
        self.get_color()
        self.red, self.green, self.blue = self.get_color()
        self.type = "rgb_light"

    def __str__(self):
        r, g, b = self.get_color()
        return "[ INTERLOCK DEVICE | "+str(self.id)+" | "+self.product_name+" | " +self.label+ " | Turned "+("OFF", "ON")[self.on]+" | COLOR: #"+self.rgb_to_hex(int(r), int(g), int(b))+" ]"

    def set_xy(self, x, y):
        self.turn_on()
        self.bridge.set_light(self.id, 'xy', [x, y])

    def get_xy(self):
        return self.xy

    def set_state(self, state):
        if state == 1:
            state = True
        elif state == 0:
            state = False
        self.bridge.set_light(self.id, 'on', state)

    def turn_on(self):
        self.set_state(True)

    def turn_off(self):
        self.set_state(False)

    def set_brightness(self, brightness):
        brightness = round(brightness * 255)
        self.turn_on()
        self.bridge.set_light(self.id, 'bri', brightness)

    def refresh(self):
        lights = self.hue_obj.hue_info['lights']
        for light_id in lights:
            if light_id == str(self.id):
                light = lights[light_id]
                self.on = light['state']['on']
                self.reachable = light['state']['reachable']
                self.xy = light['state']['xy']
                self.get_color()
                self.red, self.green, self.blue = self.get_color()
                self.brightness = light['state']['bri'] / 255

    def get_state(self):
        # self.refresh()
        lights = self.hue_obj.hue_info['lights']
        for light_id in lights:
            if light_id == str(self.id):
                return lights[light_id]['state']['on']

    def is_on(self):
        return self.on

    def hex_to_rbg(self, h):
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, r, g ,b):
        return '%02x%02x%02x' % (r, g, b)

    def set_color(self, r, g, b):
        # https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
        # just following this guys method
        if 0 <= r <= 255:
            if 0 <= g <= 255:
                if 0 <= b <= 255:
                    r = r / 255
                    g = g / 255
                    b = b / 255
                    x = r * 0.649926 + g * 0.103455 + b * 0.197109
                    y = r * 0.234327 + g * 0.743075 + b * 0.022598
                    z = g * 0.053077 + b * 1.035763
                    X = x / (x+y+z)
                    X = y / (x+y+z)
                    self.turn_on()
                    self.bridge.set_light(self.id, 'xy', [X,X])
                    return True

    def get_color(self):
        x, y = self.xy
        z = 1.0 - x - y
        Y = self.brightness
        X = (Y / y) * x
        Z = (Y / y) * z
        r = X * 1.612 - Y * 0.203 - Z * 0.302
        g = -X * 0.509 + Y * 1.412 + Z * 0.066
        b = X * 0.026 - Y * 0.072 + Z * 0.962
        r = 12.92 * r if r <= 0.0031308 else (1.0 + 0.055) * pow(r, (1.0 / 2.4)) - 0.055
        g = 12.92 * g if g <= 0.0031308 else (1.0 + 0.055) * pow(g, (1.0 / 2.4)) - 0.055
        b = 12.92 * b if b <= 0.0031308 else (1.0 + 0.055) * pow(b, (1.0 / 2.4)) - 0.055
        maxValue = max(r, g, b)
        r /= maxValue
        g /= maxValue
        b /= maxValue
        r = r * 255
        if r < 0:
            r = 255
        g = g * 255
        if g < 0:
            g = 255
        b = b * 255
        if b < 0:
            b = 255
        return r, g, b
