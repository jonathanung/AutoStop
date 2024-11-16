import carla

"""
This class is a wrapper for the CARLA client.
"""
class ClientManager:
    """
    This method initializes the ClientManager class.
    """
    def __init__(self, host: str = 'localhost', port: int = 2000, map_name: str = 'Town01'):
        self.host = host
        self.port = port
        self.map_name = map_name
        self.client = self.create_client(host, port)
        self.world = self.client.get_world()
        self.vehicle_manager = None

    """
    This method creates a client and connects to the CARLA server.
    """
    def create_client(self):
        client = carla.Client(self.host, self.port)
        client.set_timeout(20.0)
        client.load_world(self.map_name)
        print(f"Connected to CARLA server: {client.get_world().get_map().name}")
        return client

    """
    This method returns the client.
    """
    def get_client_instance(self):
        if self.client is None:
            self.client = self.create_client()
            self.world = self.client.get_world()
        return self.client

    """
    This method returns the world.
    """
    def get_world(self):
        if self.world is None:
            if self.client is None:
                self.client = self.create_client()
            self.world = self.client.get_world()
        return self.world
    
    """
    This method returns the vehicle manager.
    """
    def get_vehicle_manager(self):
        return self.vehicle_manager
    
    """
    This method sets the vehicle manager.
    """
    def set_vehicle_manager(self, vehicle_manager):
        self.vehicle_manager = vehicle_manager

    """
    This method cleans up the client and the vehicle manager.
    """
    def cleanup(self):
        self.client = None
        self.world = None
        if self.vehicle_manager is not None:
            self.vehicle_manager.cleanup()
            self.vehicle_manager = None
