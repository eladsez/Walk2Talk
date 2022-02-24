from typing import List

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'

"""
-----------------------------massage packet template---------------------------
 1 (massage type) | sender name | receiver name (could be 'broadcast')| massage
-------------------------------------------------------------------------------

---------------------------list request packet template------------------------
 2 (request type) | files/names
-------------------------------------------------------------------------------

---------------------------list response packet template-----------------------
 3 (list type) | files/names | the list in str format separate with ','
-------------------------------------------------------------------------------
"""


def get_active_clients_packet():
    """
    This method returns a single packet.
    The Client can send it to the Server to get the active clients on the Server
    :return:
    """
    return REQ_TYPE + '|names'


def active_clients_packet(client_names: List[str]):
    """
    This method gets the Client name list.
    it imports the imgs to a packet which the Server will send to the Client the request came from.
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
    The Client can send it to the Server to get the file list available to download on the Server.
    :return:
    """
    return REQ_TYPE + '|files'


def server_files_packet(files: List[str]):
    """
    This methods gets the Server files list.
    it imports the images to a packet which the Server will send to the Client.
    :param files:
    :return:
    """
    pkt = LIST_TYPE + '|files|' + files[0]
    for name in files:
        if files[0] == name:
            continue
        pkt += ',' + name
    return pkt


def msg_packet(sender_name: str, receiver_name: str, msg: str):
    """
    This method gets the sender name.
    it imports the images to a packet which will be sent to the receiver ( other Client )
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


def display_list(to_display: List[str]):
    dis = ''
    for i, val in enumerate(to_display):
        # dis += '   ' + str(i + 1) + '.' + val + '\n'
        dis += ' ' + val

    return dis


def download_request(file_name: str):
    """
    This method creates a download request packet
    :param file_name: file name.
    :return:
    """
    pass


def download_details():
    """
    This method will be sent by the server to the client, and will contain all the details about the file.
    i.e - size,which file...
    :return:
    """
    pass


def encrypt_packet(pkt):
    """
    This method encrypts our packet and sends it to the Client as an encrypted,
    he will be able to decrypt it using the decrypt message in the Server.
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



