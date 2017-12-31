# input must be an array of same sized slices
def assemble_vertical_slices(slices):
    result = []
    for i in range(len(slices[0])):
        for a_slice in slices:
            result.append(a_slice[i])

    return result

def calculate(x, y, z):
    return 1*x + 12*y + 72*z
