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


class Scene:
    def __init__(self, scene_id, label, scene_instructions):
        self.id = scene_id
        self.label = label
        self.room = None
        self.instructions = scene_instructions

    def run(self):
        for ins in self.instructions:
            ins.run()
