import sys
from pickle import loads, dumps
from typing import BinaryIO


def server_handshake(syn_or_ack: str):
    return 'SYN-SERVER' if syn_or_ack == 'syn' else 'ACK-SERVER'


def client_handshake():
    return 'SYN_ACK-CLIENT'


def ack_from_client(seq: int, final: bool = False):
    """
    This method gets an acknowledgment response pkt from the client
    :return:
    """
    if final:
        return '-FINAL-ACK-FILE-RECEIVED-'.encode()
    return f'ACK-DATA-SEQ-{seq}'.encode()


def seq_from_client_ack(ack: bytes):
    return int(ack.decode()[13:])


def nack_from_client(seq: int):
    """
    This method gets an not acknowledgement response from the client
    :return:
    """
    pass


def file_to_pkt(file: BinaryIO, seq: int):
    """
    This method gets a file and returns a packet of the maximum datagram by size the client can receive, numbered by seq.
    :param frame_id:
    :param size:
    :param seq:
    :param file:
    :return:
    """
    data = None
    try:
        data = file.read(1024)
    except Exception as e:
        print(e)
    seq = seq + sys.getsizeof(data)
    return seq, dumps([seq, data])


def pkt_to_file(pkt: bytes) -> tuple:
    """
    This method gets a pkt and returns a tuple of the data file and his sequence .
    :param pkt:
    :return:
    """
    pkt = loads(pkt)
    return pkt[0], pkt[1]


if __name__ == '__main__':
    print(seq_from_client_ack(ack_from_client(50)))
