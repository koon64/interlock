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

    # turns all the lights off in a room
    def turn_off_lights(self):
        for light in self.lights:
            light.turn_off()

    # turns all the lights on in a room
    def turn_on_lights(self):
        for light in self.lights:
            light.turn_on()

    # sets the brightness of a room
    def set_brightness(self, brightness):
        # loops through each light from the room
        for light in self.lights:
            light.set_brightness(brightness)  # sets the brightness to the night

    # sets the room to be main
    def set_main(self):
        self.main = True  # sets this room to main
        # loops through all the other rooms in the interlock class
        for room in self.interlock.get_rooms():
            if room.room_name != self.room_name:  # if it is not the current room
                room.main = False  # sets main to false

    # returns a scene object from a room
    def get_scene(self, scene_id):
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None

    # returns a string of the status of the room
    def get_status_string(self):
        # defines some starting variables
        string_parts = []
        status_string = ""
        lights_on = 0
        lights_off = 0

        playing_media = []
        # collects all the status information and changes the vars
        # lights
        # todo: tidy this up a bit
        b = False
        for light in self.lights:
            if light.service == 'hue' and not b:
                light.get_state()
                b = True
            if light.on or light.on == 1:
                lights_on += 1
            else:
                lights_off += 1
        # speakers and displays
        for device in self.devices:
            if device.type == "display" or device.type == "speaker":
                media = device.get_media()
                if media is not None:
                    playing_media.append({
                        "device": device,
                        "media": media
                    })
        # puts the vars into a string
        # lights
        if lights_on == 0:
            string_parts.append("all the lights are off")
        elif lights_off == 0:
            string_parts.append("all the lights are on")
        # speakers and displays
        if len(playing_media) == 0:
            string_parts.append("nothing is currently playing")
        else:
            for instance in playing_media:
                device_label = instance['device'].label
                media = instance['media']
                title = media.title
                artist = media.artist
                string_parts.append(device_label + " is playing " + title + " by " + artist)
        # join all the string parts together
        string_count = 0
        for string in string_parts:
            string_count += 1
            status_string += string
            if string_count != len(string_parts):
                if string_count + 1 == len(string_parts):
                    status_string += ", and "
                else:
                    status_string += ", "
        status_string = status_string.capitalize()
        status_string += "."
        return status_string

