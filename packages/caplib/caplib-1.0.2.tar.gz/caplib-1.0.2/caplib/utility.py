import struct

def num_to_bytes(data: list):
    _data = [i.to_bytes(1, byteorder='little', signed=True) for i in data]
    res = _data[0]
    for i in range(1, len(_data)):
        res += _data[i]
    return res
