class Instruction:
    def __init__(self, device, command, state):
        self.device = device
        self.command = command
        self.state = state

    def run(self):
        if self.command == "set_state":
            if self.device.type == "switch" or self.device.type == "rgb_light":
                self.device.set_state(self.state)
        elif self.command == "set_xy":
            if self.device.type == "rgb_light":
                x, y = self.state
                self.device.set_xy(x, y)

    # returns true if a device matches the instruction
    def match(self, device, accuracy=.3):
        # looks for the types of instructions
        # 1) set_state (binary)
        # 2) set_xy

        if self.command == "set_state":
            # makes sure that the device is the right type
            if device.type == "switch" or device.type == "rgb_light":
                # gets the device state value
                device_state = device.get_state()
                # if it is an it, change it to bool
                if device_state == 1:
                    device_state = True
                # makes sure they are the same value
                if device_state == self.state:
                    return True
        elif self.command == "set_xy":
            # makes sure that the device is the right type
            if device.type == "rgb_light":
                # gets the absolute value of the difference between the x and y values
                # these numbers are then compared to the accuracy float and if it is lower, ret True
                device_x, device_y = device.get_xy()
                state_x, state_y = self.state
                difference_x, difference_y = device_x - state_x, device_y - state_y
                absolute_x, absolute_y = abs(difference_x), abs(difference_y)
                if absolute_x <= accuracy and absolute_y <= accuracy:
                    return True
        return False


class Scene:
    def __init__(self, scene_id, label, scene_instructions):
        self.id = scene_id
        self.label = label
        self.room = None
        self.instructions = scene_instructions

    def run(self):
        for ins in self.instructions:
            ins.run()
