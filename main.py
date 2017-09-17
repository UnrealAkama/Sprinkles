#!/usr/bin/env python

import opc
import glob, os
import importlib
import random
from sample_pattern import SamplePattern

IP_PORT = '127.0.0.1:7890'

if __name__ == "__main__":
    client = opc.Client(IP_PORT)
    if client.can_connect():
        print('    connected to %s' % IP_PORT)
    else:
        # can't connect, but keep running in case the server appears later
        print('    WARNING: could not connect to %s' % IP_PORT)
    print('')

    modules = []

    os.chdir("patterns")
    for file in glob.glob("*.py"):
        if 'Pattern' in file:
            new_module = importlib.import_module('patterns.{}'.format(file[:-3]))
            pattern = getattr(new_module, file[:-3])
            if issubclass(pattern, SamplePattern):
                modules.append(pattern())

    # setup all the modules XXX: probably need x,y,z spacing
    for module in modules:
        module.setup()

    while True:
        active_module = random.choice(modules)

        for i in range(500):
            output = active_module.tick()
            client.put_pixels(output)



    # call tock
    # pixels = []

    # update actual LEDs
    # client.put_pixels(pixels)
