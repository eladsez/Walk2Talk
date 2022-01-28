from typing import List

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'

"""
----------------------------massage packet template----------------------------
 1 (massage type) | sender name | receiver name (could be 'broadcast')| massage
-------------------------------------------------------------------------------

-------------------------list/names request packet template--------------------
 2 (request type) | files/names
-------------------------------------------------------------------------------

--------------------------list response packet template------------------------
 3 (list type) | files/names | the list in str format separate with ','
-------------------------------------------------------------------------------

"""


def get_active_clients_packet():
    """
    This method returns a single packet.
    The client can send it to the server to get the active clients on the server
    :return:
    """
    return REQ_TYPE + '|names'


def active_clients_packet(client_names: List[str]):
    """
    This method gets the client name list.
    it imports the imgs to a packet which the server will send to the client the request came from.
    :param client_names:
    :return:
    """
    pkt = LIST_TYPE + '|names|' + client_names[0]
    for name in client_names:
        if client_names[0] == name:
            continue
        pkt += ',' + name
    return pkt


def get_server_files_packet():
    """
    This method returns a single packet.
    The client can send it to the server to get the file list available to download on the server.
    :return:
    """
    return REQ_TYPE + '|flies'


def server_files_packet(files: List[str]):
    """
    This methods gets the server files list.
    it imports the images to a packet which the server will send to the client.
    :param files:
    :return:
    """
    pkt = LIST_TYPE + '|files|' + files[0]
    for name in files:
        if files[0] == name:
            continue
        pkt += ',' + name
    return pkt


# def get_msg_packet(receiver_name: str, sender_name: str, msg: str):
#     """
#     This method creates a packet contains:
#     a text message and a name to send it to.
#     :param receiver_name:
#     :return:
#     """
#     pass


def msg_packet(sender_name: str, receiver_name: str, msg: str):
    """
    This method gets the sender name.
    it imports the images to a packet which will be sent to the receiver ( other client )
    :param receiver_name:
    :param sender_name:
    :param msg:
    :return:
    """
    pkt = MSG_TYPE + "|" + sender_name
    if receiver_name == "":
        pkt += '|broadcast'
    else:
        pkt += '|' + receiver_name
    pkt += '|' + msg
    return pkt

def encrypt_packet(pkt):
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
    print('bla')
