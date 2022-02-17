def ack_from_server(seq: int):
    """
    This method gets an acknowledgement response from the server
    :return:
    """
    pass


def ack_from_client(seq: int):
    """
    This method gets an acknowledgment response from the client
    :return:
    """
    pass


def nack_from_server(seq: int):
    """
    This method gets an not acknowledgement response from the server
    :return:
    """
    pass


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


def file_to_datagram_seq(file_name: str, seq: int, size: float) -> str:
    """
    This method gets a file and returns a packet of the maximum datagram by size the client can receive, numbered by seq.
    :param file_name:
    :return:
    """
    pass
