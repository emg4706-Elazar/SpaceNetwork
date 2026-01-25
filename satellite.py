from space_network_lib import SpaceEntity, Packet, SpaceNetwork


class Satellite(SpaceEntity):
    def __init__(self,name,distance_from_earth):
        super().__init__(name, distance_from_earth)

    def receive_signal(self, packet: Packet):
        print(f"Satellite : {self.name}\nReceived {packet}")

my_space = SpaceNetwork()
sat1 = Satellite("Sat1",100)
sat2 = Satellite("Sat2",200)

p1 = Packet("Hello, How are you?",sat1,sat2)
my_space.send(p1)