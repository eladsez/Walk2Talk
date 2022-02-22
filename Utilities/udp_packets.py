import sys
from pickle import loads, dumps
from typing import BinaryIO

"""
---------------------------seq ack packet template--------------------------
 1 ack/nack | server/client | seq
----------------------------------------------------------------------------

---------------------------handshake packet template------------------------
 1 syn/syn ack/ack | server/client
----------------------------------------------------------------------------

"""


def server_handshake(syn_or_ack: str):
    return 'SYN-SERVER' if syn_or_ack == 'syn' else 'ACK-SERVER'


def client_handshake():
    return 'SYN_ACK-CLIENT'


def ack_from_client(seq: int):
    """
    This method gets an acknowledgment response pkt from the client
    :return:
    """
    return f'ACK-DATA-SEQ-{seq}'.encode()


def nack_from_client(seq: int):
    """
    This method gets an not acknowledgement response from the client
    :return:
    """
    pass


def get_window_size(which_window: int):
    """
    This method gets the size of the client maximum data per packet
    :param which_window: integer representing a size of data
    :return:
    """
    pass


def file_to_pkt(file: BinaryIO, seq: int, cwnd: int):
    """
    This method gets a file and returns a packet of the maximum datagram by size the client can receive, numbered by seq.
    :param cwnd:
    :param seq:
    :param file:
    :return:
    """
    data = None
    try:
        data = file.read(cwnd)
    except Exception as e:
        print(e)
    seq = seq + sys.getsizeof(data)
    return seq, dumps([seq, data])


def pkt_to_file(pkt: bytes):
    """
    This method gets a pkt and returns a tuple of the data file and his sequence .
    :param pkt:
    :return:
    """
    pkt = loads(pkt)
    return pkt[0], pkt[1]


if __name__ == '__main__':
    print(server_handshake(False))
