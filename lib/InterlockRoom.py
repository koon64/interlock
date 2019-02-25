class Room:
    def __init__(self, interlock, room_name, room_label, room_image=None, room_svg=None):
        self.interlock = interlock
        self.room_name = room_name
        self.room_label = room_label
        self.room_image = room_image
        self.svg = room_svg
        self.main = False
        self.lights = []
        self.devices = []
        self.scenes = []

    def __str__(self):
        return "[ INTERLOCK ROOM | "+self.room_name+" | "+str(len(self.devices))+" DEVICE"+("s", "")[len(self.devices) == 1]+" | Lights "+("OFF", "ON")[self.lights_on()]+" ]"

    def add_device(self, device):
        if str(type(device)) == "<class 'lib.InterlockWemoService.WemoDevice'>":
            if device.is_light:
                self.lights.append(device)
            self.devices.append(device)
        elif str(type(device)) == "<class 'lib.InterlockHueService.HueLight'>":
            self.lights.append(device)
            self.devices.append(device)
        elif str(type(device)) == "<class 'lib.InterlockChromecastService.ChromecastDevice'>":
            self.devices.append(device)
        elif str(type(device)) == "<class 'lib.InterlockSonosService.SonosSpeaker'>":
            self.devices.append(device)
        else:
            print(str(type(device))+'unsupported device')

    def add_scene(self, scene):
        self.scenes.append(scene)
        scene.room = self

    def create_scene(self, name):
        if name not in self.scenes:
            instructions = []
            for device in self.devices:
                command = None
                state = None
                if device.type == 'rgb_light':
                    command = "set_xy"
                    state = device.xy
                elif device.type == "switch":
                    command = "set_state"
                    state = device.on
                instruction = {
                    "device": device.id,
                    "command": command,
                    "state": state
                }
                instructions.append(instruction)
            config = self.interlock.config
            scene = {
                "id": name,
                "label": name.title(),
                "room": self.room_name,
                "instructions": instructions
            }
            config['scenes'].append(scene)
            self.interlock.edit_config(config)

    def get_devices(self):
        return self.devices

    def get_device(self, device_id):
        for device in self.devices:
            if device.id == device_id:
                return device
        return None

    def get_lights(self):
        return self.lights

    def lights_on(self):
        on = False
        for light in self.lights:
            if light.is_on():
                on = True
        return on

    def turn_off(self):
        for device in self.devices:
            if device.type == "rgb_light" or device.type == "switch":
                device.turn_off()
            elif device.type == "display" or device.type == "speakers":
                device.stop()

    def turn_on(self):
        for device in self.devices:
            device.turn_on()

    def turn_off_lights(self):
        for light in self.lights:
            light.turn_off()

    def turn_on_lights(self):
        for light in self.lights:
            light.turn_on()

    def set_brightness(self, brightness):
        for light in self.lights:
            light.set_brightness(brightness)

    def set_main(self):
        self.main = True
        for room in self.interlock.get_rooms():
            if room.room_name != self.room_name:
                room.main = False

    def get_scene(self, scene_id):
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None