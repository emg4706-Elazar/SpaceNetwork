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
earth = SpaceEntityNotSat("Earth", 0)
sat1 = Satellite("Sat1", 100)
sat2 = Satellite("Sat2", 400)
sat3 = Satellite("Sat3", 300)
sat4 = Satellite("Sat4", 150)
sat5 = Satellite("Sat5", 450)
sat6 = Satellite("Sat6", 250)

sates = [ sat1, sat2, sat3, sat4,sat5,sat6]


def smart_send_packet(packet: Packet, satellites: list):
    max_range = 150
    packet = packet
    satellites = satellites
    sat_source = packet.sender
    dist_source = packet.sender.distance_from_earth
    trip = [packet.receiver]
    ## selecting satellites for trip
    while trip[-1].distance_from_earth - dist_source > max_range:
        target = trip[-1].distance_from_earth
        difference_range = target - max_range
        sates_in_range = []
        for sati in satellites:
            if target > sati.distance_from_earth >= difference_range:
                sates_in_range.append(sati)
        sates_in_range.sort(key=lambda sat: sat.distance_from_earth)
        hope = sates_in_range[0]
        trip.append(hope)
    trip.append(sat_source)

    # ## creating packets
    packets = []
    for i in range(len(trip)-1):
        if i == 0:
            packet.sender = trip[1]
            packets.append(packet)
        else:
            re_packet = RelayPacket(packets[-1],trip[i+1],trip[i])
            packets.append(re_packet)
    print(packets[-1])

    ## sending packet:
    try:
         attempt_transmission(packets[-1])
    except:
        print("Transmission failed")


p1 = Packet("Hello, How are you?",earth,sat5)
smart_send_packet(p1,sates)







# earth = SpaceEntityNotSat("Earth",0)
# sat1 = Satellite("Sat1",100)
# sat2 = Satellite("Sat2",200)
# sat3 = Satellite("Sat3",300)
# sat4 = Satellite("Sat4",400)
# sates = [earth,sat1,sat2,sat3,sat4]
#
# # p1 = Packet("Hello, How are you?",sat1,sat2)
# p_final = Packet("Hello from Earth",sat3,sat4)
# p_earth_to_sat3 = RelayPacket(p_final,sat2,sat3)
# p_earth_to_sat2 = RelayPacket(p_earth_to_sat3,sat1,sat2)
# p_earth_to_sat1 = RelayPacket(p_earth_to_sat2,earth,sat1)
# print(p_earth_to_sat1)

#
# def smart_send_packet(packet :Packet,satellites : list):
#     satellites = satellites
#     max_range = 150
#     final_target = packet.receiver
#     source = packet.sender
#     if final_target.distance_from_earth - source.distance_from_earth <= max_range:
#         try:
#             attempt_transmission(packet)
#         except:
#             print("Transmission failed")
#     else:
#         current_range = source.distance_from_earth + max_range
#         sates_in_range = []
#         for sati in satellites:
#             if source.distance_from_earth < sati.distance_from_earth <= current_range:
#                 sates_in_range.append(sati)
#         sates_in_range.sort(key=lambda sat: sat.distance_from_earth)
#         sates_in_range[-1]











        # relay_p = RelayPacket(packet,source,sates_in_range[-1])
        # try:
        #     attempt_transmission(relay_p)
        # except:
        #     print("Transmission failed")








