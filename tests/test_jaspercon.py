from unittest.mock import Mock

import pytest

from jaspercon import RCONClient

def test_send_command_and_receive_response_with_mocked_socket():
    mock_socket = Mock()
    mock_socket.recv.return_value = b'\x00\x00\x00\x01\x00\x00\x00\x02ResponseData'
    rcon_client = RCONClient(server_ip="localhost", server_port=12345, password="password")
    rcon_client.socket = mock_socket
    rcon_client.send_command("list_players")
    response = rcon_client.receive_response()
    assert response == "ResponseData"