import math
import time
import opc

r = 0.0

def sin(time, period=1.0, amplitude=1.0, shift=0.0):
    result = shift + amplitude*math.sin(period*time)
    # print(result)
    return result

def range_convert(old_value, old_min, old_max, new_min, new_max):
        return round(( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min)

def range_c_simple(old_value):
    return range_convert(old_value, -1.0, 1.0, 0.0, 256.0)

client = opc.Client("127.0.0.1:7890")

while True:
    arr = []
    for k in range(8):
        for j in range(8):
            for i in range(8):
                scalar = (sin(j+r, period=1.0/3.0)*0.333) + (sin(i+r, period=1.0)* 0.333) + (sin(r+k) * 0.333)
                # print(sin(j), sin(i), scalar)
                pixel = (range_c_simple(scalar), range_c_simple(scalar), range_c_simple(scalar))
                arr.append(pixel)
                # print(pixel)
    client.put_pixels(arr)
    r = r + 1
    time.sleep(0.1)

