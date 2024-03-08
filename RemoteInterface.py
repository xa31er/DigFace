import socket


class RemoteException(Exception):
    """Exception raised for remote communication errors."""
    pass


class RemoteInterface:
    """Class for interacting with a remote simulator over TCP/IP."""

    def __init__(self):
        """Initialize the RemoteInterface object."""
        self.local_host = socket.gethostbyname(socket.gethostname())

    def start(self, file_path):
        """Start the simulation with the specified hex file.

        Args:
            file_path (str): The path to the hex file to load to program memory.
        """
        self.send_request("start", file_path)

    def debug(self, file_path):
        """Debug the simulation with the specified hex file.

        Args:
            file_path (str): The path to the hex file to load to program memory.
        """
        self.send_request("debug", file_path)

    def run(self):
        """Run the simulation until a breakpoint is encountered.

        Returns:
            int: The actual code address.
        """
        response = self.send_request("run")
        return self.get_addr(response)

    def stop(self):
        """Stop the simulation."""
        self.send_request("stop")

    def step(self):
        """Execute a single step in the simulation.

        Returns:
            int: The actual code address.
        """
        response = self.send_request("step")
        return self.get_addr(response)

    @staticmethod
    def get_addr(addr_string):
        """Parse the address string from the simulator response.

        Args:
            addr_string (str): The address string received from the simulator.

        Returns:
            int: The parsed code address.
        """
        if len(addr_string) <= 3:
            return -1
        try:
            return int(addr_string[3:], 16)
        except ValueError:
            return -1

    def send_request(self, command, args=None):
        """Send a request to the simulator and receive the response.

        Args:
            command (str): The command to send to the simulator.
            args (str, optional): Additional arguments for the command. Defaults to None.

        Returns:
            str: The response received from the simulator.

        Raises:
            RemoteException: If an error occurs during communication with the simulator.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.local_host, 56556))
                if args:
                    command = f"{command}:{args}"
                s.sendall(command.encode())
                response = s.recv(1024).decode()
                if not (response == "ok" or response.startswith("ok:")):
                    raise RemoteException(f"Error received from simulator:\n{response}")
                return response
        except (socket.error, OSError) as e:
            raise RemoteException("Error communicating with simulator!") from e
