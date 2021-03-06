from typing import List

MSG_TYPE = '1'
REQ_TYPE = '2'
LIST_TYPE = '3'
DOWNLOAD_REQ = '4'

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

---------------------------download request packet template--------------------
 4 (download request type) | file name
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
    for i in range(1, len(client_names)):
        pkt += ',' + client_names[i]
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
    for i in range(1, len(files)):
        pkt += ',' + files[i]
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
        dis += ' ' + val

    return dis


def download_request(file_name: str):
    """
    This method creates a download request packet
    :param file_name: file name.
    :return:
    """
    return DOWNLOAD_REQ + "|" + file_name


def resume_pkt():
    return (DOWNLOAD_REQ + "|" + 'RESUME-DOWNLOAD').encode()


def pause_pkt():
    return (DOWNLOAD_REQ + "|" + 'PAUSE-DOWNLOAD').encode()
