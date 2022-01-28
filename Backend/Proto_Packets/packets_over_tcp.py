from typing import List

from scapy.layers.inet import IP, TCP
from scapy.packet import Raw


def create_active_clients_packet():
    """
    This method returns a single packet.
    The client can send it to the server to get the active clients on the server
    :return:
    """

    pass


def active_clients_packet(client_names: List[str]):
    """
    This method gets the client name list.
    it imports the imgs to a packet which the server will send to the client the request came from.
    :param client_names:
    :return:
    """
    l1 = IP(dst='127.0.0.1')  # dest ip, where we want to send the pkt
    l2 = TCP()  # on which protocol to invoke it
    l3 = Raw(load=client_names)  # what imgs to send [ shaked , guy, elad, nerya ]
    pkt = l1 / l2 / l3
    return pkt


def create_server_files_packet():
    """
    This method returns a single packet.
    The client can send it to the server to get the file list available to download on the server.
    :return:
    """
    pass


def server_files_packet(files: List[str]):
    """
    This methods gets the server files list.
    it imports the imgs to a packet which the server will send to the client.
    :param files:
    :return:
    """
    l1 = IP(dst='')  # dest ip, where we want to send the pkt
    l2 = TCP()  # on which protocol to invoke it
    l3 = Raw(load=files)  # what imgs to send
    pkt = l1 / l2 / l3
    return pkt


def create_msg_packet(reciever_name: str, sender_name: str, msg: str):
    """
    This method creates a packet contains:
    a text message and a name to send it to.
    :param reciever_name:
    :return:
    """
    pass


def msg_packet(sender_name: str, msg: str):
    """
    This method gets the sender name.
    it imports the imgs to a packet which will be sent to the receiver ( other client )
    :param sender_name:
    :param msg:
    :return:
    """
    l1 = IP(dst='')  # dest ip, where we want to send the pkt
    l2 = TCP()  # on which protocol to invoke it
    l3 = Raw(load=msg)  # what imgs to send
    pkt = l1 / l2 / l3
    return pkt


def encrypt_packet(dekan_pkt):
    """
    This method encrypts our packet and sends it to the client as an encrypted,
    he will be able to decrypt it using the decrypt message in the server.
    :return:
    """
    pass


def decrypt_packet(encrypted_pkt):
    """
    This method decrypts our packet using the algorithm we provided.
    :param encrypted_pkt:
    :return:
    """
    pass


if __name__ == '__main__':
    clients = ["Josh", "Mike", "Ron"]
    print(active_clients_packet(clients).show())
    print(clients)
