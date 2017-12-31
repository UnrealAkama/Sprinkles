#!/usr/bin/env python

import opc
import glob, os
import importlib
import random
from sample_pattern import SamplePattern
import sys
import time

FPS = 60
IP_PORT = '127.0.0.1:7890'


# stolen from SO
def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses

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



    names = []

    for pattern in get_all_subclasses(SamplePattern):
        if len(sys.argv) > 1 and sys.argv[1] == pattern.__name__:
            # this is ugly
            print("only loading one module: {}".format(pattern.__name__))
            pat = pattern()
            pat.setup()
            while True:
                output = pat.tick()
                client.put_pixels(output)

        modules.append(pattern())

    while True:
        active_module = random.choice(modules)

        print(active_module.__class__.__name__)
        active_module.setup()

        for i in range(3000):
            output = active_module.tick()
            client.put_pixels(output)



    # call tock
    # pixels = []

    # update actual LEDs
    # client.put_pixels(pixels)
