"""
This class is a listener class that each client has, and it keeps the client on listening to the server.
it updates constantly the client imgs send - recv.
we use it by implementing the observable design pattern.
"""

from template_client import Client


class client_obs():

    def __init__(self):
        self.clients = []

    def register_client_observer(self, client):
        self.clients.append(client)

    def notify_clients(self, *args, **kwargs):
        for cli in self.clients:
            cli.notify(self, *args, **kwargs)


class Listener():

    def __init__(self, client: client_obs):
        client.register_client_observer(client)

    def notify(self, client, *args, **kwargs):
        """
        This method updates the imgs to all clients.
        :param client:
        :param args:
        :param kwargs:
        :return:
        """
        pass
