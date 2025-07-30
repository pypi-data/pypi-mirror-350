import binascii
import itertools
import math
import statistics
import struct

class ninjalib:
    def __init__(self,data,a=0,b=0,c=0):
        self.data = data
        self.a = a
        self.b = b
        self.c = c

    def anomaly(self):
        hits = []
        distances = []
        self.data.sort()
        for key,value in enumerate(self.data):
            if key < len(self.data) - 1:
                distances.append(abs(self.data[key]-self.data[key+1]))
        average = sum(distances) / len(distances)
        for key,value in enumerate(self.data):
            if key < len(self.data) - 1:
                if average < abs(self.data[key+1] - self.data[key]) and average < abs(self.data[key] - self.data[key-1]):
                    hits.append(self.data[key])
        return hits

    def flatten_list(self):
        new_data = self.data
        if self.a == 0:
            while True:
                if isinstance(new_data[0],list) or isinstance(new_data[0],tuple):
                    new_data = list(itertools.chain(*new_data))
                else:
                    break
        else:
            for i in range(self.a):
                if isinstance(new_data[0],list) or isinstance(new_data[0],tuple):
                    new_data = list(itertools.chain(*new_data))
        return new_data

    def flatten_tuple(self):
        new_data = self.data
        if self.a == 0:
            while True:
                if isinstance(new_data[0],list) or isinstance(new_data[0],tuple):
                    new_data = tuple(itertools.chain(*new_data))
                else:
                    break
        else:
            for i in range(self.aF):
                if isinstance(new_data[0],list) or isinstance(new_data[0],tuple):
                    new_data = tuple(itertools.chain(*new_data))
        return new_data

    def project(self):
        try:
            screen_x = math.floor(self.data * (self.a / self.c))
        except ZeroDivisionError:
            screen_x = self.data + self.a
        try:
            screen_y = math.floor(self.data * (self.b / self.c))
        except ZeroDivisionError:
            screen_y = self.data + self.b
        return [screen_x,screen_y]

    def rotate_camera(self):
        hits = []
        theta = math.radians(self.b)
        center_x = []
        center_y = []
        center_z = []
        for i in range(len(self.data)):
            center_x.append(self.data[i][0])
            center_y.append(self.data[i][1])
            center_z.append(self.data[i][2])
        cx = statistics.mean(center_x)
        cy = statistics.mean(center_y)
        cz = statistics.mean(center_z)
        for i in range(len(self.data)):
            x = self.data[i][0] - cx
            y = self.data[i][1] - cy
            z = self.data[i][2] - cz
            if self.a == "x":
                hits.append([round(cx+x,3),round(cy+math.cos(theta)*y-math.sin(theta)*z,3),round(cz+math.sin(theta)*y+math.cos(theta)*z,3)])
            if self.a == "y":
                hits.append([round(cx+math.cos(theta)*x+math.sin(theta)*z,3),round(cy+y,3),round(cz+-math.sin(theta)*x+math.cos(theta)*z,3)])
            if self.a == "z":
                hits.append([round(cx+math.cos(theta)*x-math.sin(theta)*y,3),round(cy+math.sin(theta)*x+math.cos(theta)*y,3),round(cz+z,3)])
        return hits

    def mean(self):
        return sum(self.data) / len(self.data)

    def odds(self):
        return str(round(sum(self.data) / (sum(self.data) + sum(self.a)) * 100,3)) + "%"

    def status(self):
        if self.a == 0:
            self.a = -1
        handshake = binascii.unhexlify("00") + b"".join([bytes([(b := (self.a >> 7 * i) & 0x7F) | (0x80 if self.a >> 7 * (i + 1) else 0)]) for i in range(5) if (self.a >> 7 * i)]) + struct.pack(">b",len(self.data[0])) + self.data[0].encode() + struct.pack(">H", self.data[1]) + b"\x01"
        return [struct.pack(">b",len(handshake)) + handshake, binascii.unhexlify("0100")]

    def varint(self):
        return b"".join([bytes([(b := (self.data >> 7 * i) & 0x7F) | (0x80 if self.data >> 7 * (i + 1) else 0)]) for i in range(5) if (self.data >> 7 * i)])
