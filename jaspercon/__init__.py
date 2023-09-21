import rcon

from jaspercon.utils import jlogging

class RCONClient:
    def __init__(self, server_ip: str, server_port: int, password: str, log_main_name: str, debug: bool = False):
        self.server_ip = server_ip
        self.server_port = server_port
        self.password = password
        self.socket = None
        self.request_id_counter = 0
        self.logger = jlogging.get_logger(app_name=log_main_name, module_name="jaspercon", debug=debug)
        
    def _generate_request_id(self):
        self.request_id_counter += 1
        log_line = f"request_id_counter: {self.request_id_counter}"
        self.logger.debug(log_line)
        return self.request_id_counter
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            self.logger.info("Successfully connected to the server")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the server {e}")
        
    def authenticate(self):
        try:
            password_bytes = self.password.encode("utf-8")
            packet_format = "<ii{}s".format(len(password_bytes))
            request_id = self._generate_request_id()
            auth_packet = struct.pack(packet_format, request_id, 3, password_bytes)
            self.logger.debug(auth_packet)
            self.socket.send(auth_packet)
            response_packet = self.socket.recv(4096)
            response_id, response_type, success_flag = struct.unpack("<iii", response_packet[:12])
            response_message = f"Response Details: {response_id} {response_type} {success_flag}"
            self.logger.debug(response_message)
            if success_flag == 1:
                self.logger.info("Authentication successful")
            else:
                self.logger.error("Authentication failed")
        except Exception as e:
            raise Exception(f"Authentication failed: {e}")
        
    def send_command(self, command):
        try:
            request_id = self._generate_request_id()
            command_bytes = command.encode("utf-8")
            packet_format = "<iii{}s".format(len(command_bytes))
            command_packet = struct.pack(packet_format, request_id, 2, command_bytes)
            self.socket.send(command_packet)
        except Exception as e:
            raise Exception(f"Failed to send command: {e}")
        
    def receive_response(self, command):
        try:
            response_packet = self.socket.recv(4096)
            response_id, response_type, response_data = struct.unpack("<iii", response_packet[:12], response_packet)
            response_text = response_data.decode("utf-8")
            return response_text
        except Exception as e:
            raise Exception(f"Failed to receive response: {e}")
        
    def disconnect(self):
        try:
            if self.socket:
                self.socket.close()
        except Exception as e:
            raise Exception(f"Failed to close the connection: {e}")