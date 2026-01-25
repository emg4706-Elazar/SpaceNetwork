from space_network_lib import (DataCorruptedError,SpaceEntity,
Packet, SpaceNetwork,TemporalInterferenceError,
LinkTerminatedError ,OutOfRangeError )
import time


class BrokenConnectionError(Exception):
    pass


def attempt_transmission(packet :Packet):
    sent = False
    while not sent:
        try:
            my_space.send(packet)
            sent = True
        except TemporalInterferenceError:
            print("Interference, waiting...")
            time.sleep(2)
        except DataCorruptedError:
            print("Data corrupted, retrying...")
        except LinkTerminatedError:
            raise BrokenConnectionError("Link lost!")
        except OutOfRangeError:
            raise BrokenConnectionError("Target out of range")


class Satellite(SpaceEntity):
    def __init__(self,name,distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"Satellite : {self.name}\nReceived {packet}")

my_space = SpaceNetwork(level=3)
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)

p1 = Packet("Hello, How are you?",sat1,sat2)

try:
    attempt_transmission(p1)
except:
    print("Transmission failed")
