"""
This class is a listener class that each client has, and it keeps the client on listening to the server.
it updates constantly the client data send - recv.
we use it by implementing the observable design pattern.
"""

from template_client import Client


class Listener():

    def __init__(self, client: Client):
        self.Client = client
