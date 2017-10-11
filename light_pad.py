import mido
import time
import collections
import math
import opc

inport = mido.open_input('SmartPAD')
outport = mido.open_output('SmartPAD')

msgs = collections.defaultdict(int)
note_blocks = [] # tuple consisting of (func, [note_id1, note_id2]), this will only allow one of the group to be lit up and will call the function with the new note id.

def range_convert(old_value, old_min, old_max, new_min, new_max):
    return round(( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)

def range_c_simple(old_value):
    return range_convert(old_value, -1.0, 1.0, 0.0, 256.0)

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

class signal():

    def __init__(self, signal_buttons, knob_ids):
        self.current_signal = 0
        self.period=1.0
        self.amplitude=1.0
        self.shift=0.0
        self.signal_buttons = signal_buttons
        self.knob_ids = knob_ids

    def update(self, time):
        return { 0: self.zero, 1: self.flat, 2: self.sin }[self.current_signal](time)

    def update_button(self, note_id):
        self.current_signal = self.signal_buttons.index(note_id)
        print("new signal is {}".format(self.current_signal))

    def update_knob(self, knob_id, knob_value):
        print("did we get update_knob")
        select_knob = self.knob_ids.index(knob_id)
        knob_to_update = { 0: "period", 1: "amplitude", 2: "shift" }[select_knob]
        print("knob: {} to {}".format(knob_to_update, knob_value))
        setattr(self, knob_to_update, range_convert(knob_value, 0.0, 127.0, -20.0, 20.0))
        print("internal knob was set to", getattr(self, knob_to_update))

    def get_current_signal(self):
        return self.signal_buttons[self.current_signal]

    def get_current_knobs(self):
        results = []
        for knob_id, value in zip(self.knob_ids, [self.period, self.amplitude, self.shift]):
            print(knob_id, value)
            results.append((knob_id, range_convert(value, -20.0, 20.0, 0.0, 127.0)))
        print(results)
        return results

    def sin(self, time):
        if self.period >= 0:
            return self.shift + self.amplitude*math.sin(self.period*time)
        else:
            return self.shift + self.amplitude*math.sin((1/self.period)*time)

    def flat(self, time):
        return 0.0

    def zero(self, time):
        return -1


class wave():
    button_blocks = []
    r = None
    g = None
    b = None
    x = None
    y = None
    z = None

    def __init__(self):
        self.button_blocks = []
        self.knob_blocks = []
        for i, signal_name in enumerate(["r", "g", "b", "x", "y", "z"]):
            buttons = [0+i, 16+i, 32+i, 48+i, 64+i]
            knobs = [0+i, 16+i, 32+i]
            setattr(self, signal_name, signal(buttons, knobs))
            self.knob_blocks.append((getattr(self, signal_name).update_knob, knobs))
            self.button_blocks.append((getattr(self, signal_name).update_button, buttons))

    def update(self, time):
	arr = []
        for i in range(6):
            for k in range(6):
                for j in range(12):
                    scalar_x = range_convert(self.x.update(time+j), -1, 1, 0, 1)
                    scalar_y = range_convert(self.y.update(time+k), -1, 1, 0, 1)
                    scalar_z = range_convert(self.z.update(time+i), -1, 1, 0, 1)
                    scalar = (scalar_x * 0.333) + (scalar_y * 0.333) + (scalar_z * 0.333)
                    # print(self.r.update(time), range_c_simple(self.r.update(time))*scalar)
                    pixel = (range_c_simple(self.r.update(time))*scalar, range_c_simple(self.g.update(time))*scalar, range_c_simple(self.b.update(time))*scalar)
                    arr.append(pixel)
        # print(arr)
        return arr 

def handle_blocks(note_id, note_block=None):
    global note_blocks
    if note_block:
        blocks = note_block
    else:
        blocks = note_blocks

    for block in blocks:
        if (type(note_id) == int and note_id in block[1]) or (type(note_id) == tuple and note_id[0] in block[1]):
            for set_note_id in block[1]:
                msgs[set_note_id] = 0
                visually_update_note(set_note_id)
            msgs[note_id] = 1
            if type(note_id) == int:
                block[0](note_id)
            else:
                block[0](note_id[0], note_id[1])
            visually_update_note(set_note_id)
            break

# TODO
def handle_knob(knob_id, value):
    global current_panel, panels
    print(knob_id, value)
    handle_blocks((knob_id, value), panels[current_panel].knob_blocks)

panel_ids = [6,7,22,23,38,39]
current_panel = panel_ids[0]

def visually_update_note(note_id):
    if msgs[note_id]:
        outport.send(mido.Message('note_on', note=note_id, velocity=127))
    else:
        outport.send(mido.Message('note_off', note=note_id, velocity=0))

def visually_update_knob(knob_id, knob_value):
    print("sending value {} to id {}".format(knob_value, knob_id))
    outport.send(mido.Message('control_change', control=knob_id, value=int(knob_value)))

def handle_selector(note_id):
    global current_panel
    teardown_panel()
    current_panel = note_id
    setup_panel()

def teardown_panel():
    for id in full_panels:
        msgs[id] = 0
        visually_update_note(id)

def setup_panel():
    global current_panel, panels
    for label in ["r", "g", "b", "x", "y", "z"]:
        vid = getattr(panels[current_panel], label).get_current_signal()
        msgs[vid] = 1
        visually_update_note(vid)
        for knob_id, value in getattr(panels[current_panel], label).get_current_knobs():
            visually_update_knob(knob_id, value)
    msgs[current_panel] = 1
    visually_update_note(current_panel)

def handle_panel(note_id):
    global current_panel, panels
    handle_blocks(note_id, panels[current_panel].button_blocks)

panel_ids = [6,7,22,23,38,39]
current_panel = panel_ids[0]

panels = {}
for panel_id in panel_ids:
    panels[panel_id] = wave()

note_blocks.append((handle_selector, panel_ids))

full_panels = []

for i in range(6):
    full_panels = full_panels + [0+i,16+i,32+i,48+i,64+i]
    note_blocks.append((handle_panel, [0+i,16+i,32+i,48+i,64+i]))

teardown_panel()
setup_panel()

# print(panels[current_panel].r.get_current_signal())
# buttons = [0,16,32,48,64]

# s = signal(buttons)



# note_blocks.append((s.update_button, buttons))

# for i in range(6):
    # note_blocks.append((wave_minipulator, [0+i,16+i,32+i,48+i,64+i]))

# note_blocks.append((geo_pattern, [102,118,86,70,54]))
# note_blocks.append((geo_pattern, [103,119,87,71,55]))

print(note_blocks)

client = opc.Client("127.0.0.1:7890")

t = 0

while True: #main loopA
    # deal with incoming messages
    for msg in inport.iter_pending():
        if msg.type == "control_change":
            # control 0,16,32,48
            handle_knob(msg.control, msg.value)
            print(msg)
        if msg.type == "note_on" and msg.channel == 2 and msg.note == 112:
            print("clear board")
            for item in msgs:
                msgs[item] = 0
                visually_update_note(msg.note)
            continue
        if msg.type == "note_on" and msg.channel == 0:
            msgs[msg.note] = (msgs[msg.note] + 1) % 2
            visually_update_note(msg.note)
            handle_blocks(msg.note)
            # print(msgs)
        if msg.type == "note_off" and msg.channel == 0:
            # is this actually supposed to be off?
            if msgs[msg.note]:
                visually_update_note(msg.note)
   
    final_output = []
    final_lights = []
    for panel in panels:
        final_lights.append(panels[panel].update(t))
    for item in zip(*final_lights):
        x = []
        y = []
        z = []
        for light in item:
            if light[0] == 0 and light[1] == 0 and light[2] == 0:
                continue
            x.append(light[0])
            y.append(light[1])
            z.append(light[2])
        if len(x) == 0:
            final_output.append((0,0,0))
        else:
            final_output.append((int(mean(x)), int(mean(y)), int(mean(z))))
        # print(item)
        

    client.put_pixels(final_output)

    # for item in msgs:
        # if msgs[item]:
            # outport.send(mido.Message('note_on', note=msg.note, velocity=127))
    time.sleep(0.02)
    t += -0.1 

while True:
    time.sleep(0.2)
    for j in range(0,15):
        for i in range(0,127):
            outport.send(mido.Message('note_on', note=i, velocity=100, channel=j))
    time.sleep(0.2)
    for i in range(0,127):
        outport.send(mido.Message('note_off', note=i, velocity=100, channel=0))
