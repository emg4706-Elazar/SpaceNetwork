from space_network_lib import (DataCorruptedError,SpaceEntity,
Packet, SpaceNetwork,TemporalInterferenceError,
LinkTerminatedError ,OutOfRangeError )
import time


class BrokenConnectionError(Exception):
    pass

class RelayPacket(Packet):
    def __init__(self,packet_to_relay, sender, proxy):
        super().__init__(packet_to_relay,sender,proxy)

    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver}from {self.sender})"

class SpaceEntityNotSat(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        pass


def attempt_transmission(packet :Packet):
    sent = False
    print(f"from {packet.sender.name}")
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
        if isinstance(packet,RelayPacket):
            inner_packet = packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}" )

my_space = SpaceNetwork(level=3)
earth = SpaceEntityNotSat("Earth",0)
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)

p1 = Packet("Hello, How are you?",sat1,sat2)
p_final = Packet("Hello from Earth",sat1,sat2)
p_earth_to_sat1 = RelayPacket(p_final,earth,sat1)

try:
    attempt_transmission(p_earth_to_sat1)
except:
    print("Transmission failed")

