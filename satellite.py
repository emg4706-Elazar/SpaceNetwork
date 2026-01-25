from space_network_lib import (DataCorruptedError,SpaceEntity,
Packet, SpaceNetwork,TemporalInterferenceError)
import time

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

class Satellite(SpaceEntity):
    def __init__(self,name,distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"Satellite : {self.name}\nReceived {packet}")

my_space = SpaceNetwork(level=2)
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)

p1 = Packet("Hello, How are you?",sat1,sat2)

attempt_transmission(p1)