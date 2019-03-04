import json
from lib.InterlockRoom import Room
from lib.InterlockScene import Scene, Instruction
from lib.InterlockPhone import Phone
from lib.InterlockHueService import HueService
from lib.InterlockWemoService import WemoService
from lib.InterlockSonosService import SonosService
from lib.InterlockPlayMusicService import PlayMusicService
from lib.InterlockChromecastService import ChromecastService




class Interlock:
    def __init__(self, config_file=None, debug=False):
        # sets the version numbers
        self.version = 2.0
        self.last_supported_version = 2.0
        print("")
        print("                  ___           ___           ___           ___           ___       ___           ___           ___     ")
        print("      ___        /\\__\\         /\\  \\         /\\  \\         /\\  \\         /\\__\\     /\\  \\         /\\  \\         /\\__\\    ")
        print("     /\\  \\      /::|  |        \\:\\  \\       /::\\  \\       /::\\  \\       /:/  /    /::\\  \\       /::\\  \\       /:/  /    ")
        print("     \\:\\  \\    /:|:|  |         \\:\\  \\     /:/\\:\\  \\     /:/\\:\\  \\     /:/  /    /:/\\:\\  \\     /:/\\:\\  \\     /:/__/     ")
        print("     /::\\__\\  /:/|:|  |__       /::\\  \\   /::\\~\\:\\  \\   /::\\~\\:\\  \\   /:/  /    /:/  \\:\\  \\   /:/  \\:\\  \\   /::\\__\\____ ")
        print("  __/:/\\/__/ /:/ |:| /\\__\\     /:/\\:\\__\\ /:/\\:\\ \\:\\__\\ /:/\\:\\ \\:\\__\\ /:/__/    /:/__/ \\:\\__\\ /:/__/ \\:\\__\\ /:/\\:::::\\__\\")
        print(" /\\/:/  /    \\/__|:|/:/  /    /:/  \\/__/ \\:\\~\\:\\ \\/__/ \\/_|::\\/:/  / \\:\\  \\    \\:\\  \\ /:/  / \\:\\  \\  \\/__/ \\/_|:|~~|~   ")
        print(" \\::/__/         |:/:/  /    /:/  /       \\:\\ \\:\\__\\      |:|::/  /   \\:\\  \\    \\:\\  /:/  /   \\:\\  \\          |:|  |    ")
        print("  \\:\\__\\         |::/  /     \\/__/         \\:\\ \\/__/      |:|\\/__/     \\:\\  \\    \\:\\/:/  /     \\:\\  \\         |:|  |    ")
        print("   \\/__/         /:/  /                     \\:\\__\\        |:|  |        \\:\\__\\    \\::/  /       \\:\\__\\        |:|  |    ")
        print("                 \\/__/                       \\/__/         \\|__|         \\/__/     \\/__/         \\/__/         \\|__|    ")
        print("")
        print("Initializing Interlock " + str(self.version))
        print("By Max Koon")
        print("")
        # debug
        self.debug = debug
        # lets the services
        self.phone = Phone
        self.wemo = WemoService
        self.sonos = SonosService
        self.hue = HueService
        self.chromecast = ChromecastService

        # idk
        self.hue_instance = None

        # object variables
        self.rooms = []
        self.scenes = []
        self.media_services = []
        # if config file is passed
        if config_file is not None:
            with open(config_file, 'r') as file:  # opens the json file
                try:
                    # sets it into a dict
                    config = json.load(file)
                    self.config = config
                    # for over-righting
                    self.config_file_path = config_file
                    # checks if supported
                    if self.last_supported_version <= config['interlock_information']['version'] <= self.version:
                        # server info
                        self.server_ip = config['server']['ip_address']
                        self.server_port = config['server']['port']
                        # makes sure duplicate services does not occur
                        wemo_started = False
                        chromecast_started = False
                        sonos_started = False
                        # creates all the rooms
                        rooms_to_create = config['rooms']
                        for room in rooms_to_create:
                            created_room = self.create_room(room['name'], room['label'], room['image'], room['svg'])
                            if room['main']:
                                created_room.set_main()  # if main room
                        # creates all the devices
                        devices_to_create = config['devices']
                        if devices_to_create is not None:
                            for device in devices_to_create:
                                created_device = None
                                if device['service'] == 'wemo':
                                    # wemo device
                                    if not wemo_started:  # makes sure the wemo service is not running
                                        wemo = self.wemo()
                                        wemo_started = True
                                    created_device = wemo.device(device['id'])
                                elif device['service'] == 'chromecast':
                                    # chromecast
                                    if not chromecast_started:
                                        chromecast = self.chromecast()
                                        chromecast_started = True
                                    created_device = chromecast.device(device['id'])
                                elif device['service'] == 'sonos':
                                    # sonos
                                    if not sonos_started:
                                        sonos = self.sonos()
                                        sonos_started = True
                                    created_device = sonos.device(device['id'])
                                if created_device is None:
                                    raise Exception('unsupported device')
                                if self.verify_room(device['room']):
                                    room = self.room(device['room'])
                                    room.add_device(created_device)

                        # creates all the devices for the services
                        services_to_create = config['services']
                        for service in services_to_create:
                            if service['service_name'] == 'hue':
                                self.hue_instance = self.hue(service['bridge_ip'])
                                lights_to_assign_to_rooms = service['rooms']
                                for light in self.hue_instance.lights:
                                    for room_name in lights_to_assign_to_rooms:
                                        room_lights = lights_to_assign_to_rooms[room_name]
                                        if light.id in room_lights:
                                            room = self.room(room_name)
                                            room.add_device(light)
                            elif service['service_name'] == 'play_music':
                                try:
                                    self.play_music = PlayMusicService(service['oauth'])
                                    self.media_services.append(self.play_music)
                                except:
                                    print("could not connect to play music")
                                    # creates all the scenes for the rooms
                        if "scenes" in config:
                            scenes_to_create = config['scenes']
                            for scene in scenes_to_create:
                                room_name = scene['room']
                                if self.verify_room(room_name):
                                    scene_instructions = self.create_scene_instructions(room, scene['instructions'])
                                    created_scene = self.create_scene(scene['id'], scene['label'],
                                                                      scene_instructions)
                                    room = self.room(room_name)
                                    room.add_scene(created_scene)
                except json.JSONDecodeError as exc:
                    self.print(exc)

    def create_room(self, room_name, room_label, room_image=None, room_svg=None):
        room = Room(self, room_name, room_label, room_image, room_svg)
        self.rooms.append(room)
        return room

    def create_scene(self, scene_id, label, ins):
        scene = Scene(scene_id, label, ins)
        self.scenes.append(scene)
        return scene

    def create_scene_instructions(self, room, instructions):
        instruction_objs = []
        for instruction in instructions:
            device = room.get_device(instruction['device'])
            if device is not None:
                ins = Instruction(device, instruction['command'], instruction['state'])
                instruction_objs.append(ins)
            else:
                raise Exception(str(instruction['device']) + " is not a valid device in the " + room.room_label)
        return instruction_objs

    def verify_room(self, room_name):
        return self.room(room_name)

    def get_rooms(self):
        return self.rooms

    def room(self, room_name):
        for room in self.rooms:
            if room_name == room.room_name:
                return room
        return False

    def get_devices(self):
        devices = []
        for room in self.rooms:
            room_devices = room.get_devices()
            devices = devices + room_devices
        return devices

    def device(self, device_name):
        for device in self.get_devices():
            if str(device.id) == str(device_name):
                return device

    def print(self, text):
        if self.debug:
            print("INTERLOCK OUTPUT:", text)

    def edit_config(self, config):
        with open(self.config_file_path, 'w') as file:
            json.dump(config, file)
            print("file changed")

    def get_media_services(self):
        return self.media_services

    def refresh_hue(self):
        self.hue_instance.refresh_lights()

