from pythonosc import udp_client, tcp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from ipaddress import IPv4Address
from typing import Literal, Any
import types
from enum import Enum
import logging
import threading
import re

from chimp_osc.commands import COMMANDS, TYPES, Action, LED

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Chimp:
    def __init__(
        self,
        ip: IPv4Address,
        port_out: int = 8000,
        port_in: int = 9000,
        mode: Literal["TCP", "UDP"] = "UDP",
    ):
        self._ip = ip
        self._port_in = port_in
        self._port_out = port_out
        self._mode = mode
        if self._mode == "TCP":
            self.client = tcp_client.SimpleTCPClient(
                self._ip.compressed, self._port_out
            )
        elif self._mode == "UDP":
            self.client = udp_client.SimpleUDPClient(
                self._ip.compressed, self._port_out
            )
        logging.debug("Registering dynamic methods")
        self.register_dynamic_methods()
        self.dispatcher = Dispatcher()
        self.server = ThreadingOSCUDPServer(
            (self._ip.compressed, self._port_in), self.dispatcher
        )
        self.thread = None
        self.start_osc_server()

    def start_osc_server(self):
        self.thread = threading.Thread(target=self.server.serve_forever)
        logging.debug("Starting Server")
        self.thread.start()

    def shutdown_osc_server(self):
        if self.server and self.thread.is_alive():
            logging.debug("Shutting down OSC server...")
            self.server.shutdown()
            self.thread.join()
            logging.debug("OSC Server Shut Down")

    def add_handler(self, address: str, handler: Any):
        self.dispatcher.map(address=address, handler=handler)

    def send_message(self, path: str, value):
        if not path.startswith("/"):
            path = "/" + path
        self.client.send_message(path, value)
        logging.debug(f"Send {value} to {path}")

    def register_dynamic_methods(self):
        def build_methods(
            tree: dict,
            path_parts: list = [],
            method_parts: list = [],
            parameters: dict = {},
        ):
            for key, val in tree.items():
                method_parts_new = method_parts.copy()
                parameters_new = parameters.copy()
                if isinstance(val, dict):
                    match = re.match(r"\{(\w+)\}", key)
                    if match:
                        parameters_new[match.group(1)] = TYPES[match.group(1)]
                    else:
                        method_parts_new.append(key)
                    build_methods(
                        val, path_parts + [key], method_parts_new, parameters_new
                    )
                else:
                    path_str = "/".join(path_parts + [key])
                    method_name = "c_"+"_".join(method_parts + [key])
                    # logging.debug(method_name)
                    # logging.debug(path_str)
                    parameters["data"] = val
                    method = f"""def {method_name}(self, {', '.join([f'{key}: {value.__name__}' for key, value in parameters.items()])}):
                        path = "/chimp/" + "{path_str}".format({', '.join([f'{key}={key}'for key in parameters])})
                        if isinstance(data, Enum):
                            data = data.value
                        self.send_message(path, data)
                    """
                    namespace = {}
                    exec(method, None, namespace)
                    func = namespace[method_name]
                    func.__name__ = method_name
                    setattr(self, method_name, types.MethodType(func, self))

        build_methods(COMMANDS)
