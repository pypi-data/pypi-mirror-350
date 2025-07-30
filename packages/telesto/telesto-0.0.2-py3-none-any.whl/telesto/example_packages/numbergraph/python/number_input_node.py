#   Hyrrokkin - a library for building and running executable graphs
#
#   MIT License - Copyright (C) 2022-2025  Visual Topology Ltd

from hyrrokkin_engine.node_interface import NodeInterface

class NumberInputNode(NodeInterface):

    DEFAULT_VALUE = "10"

    def __init__(self, services):
        self.services = services
        self.clients = {}

    def open_client(self, session_id, client_name, client_options, client_service):
        self.clients[(session_id,client_name)] = client_service
        client_service.set_message_handler(lambda *msg: self.__handle_message(session_id, client_name, *msg))
        client_service.send_message(self.services.get_property("value",NumberInputNode.DEFAULT_VALUE))

    def close_client(self, session_id, client_name):
        del self.clients[(session_id,client_name)]

    def __handle_message(self, session_id, client_name, value):
        self.services.set_property("value", value)
        self.services.request_run()
        for key in self.clients:
            if key != (session_id,client_name):
                self.clients[key].send_message(self.services.get_property("value",NumberInputNode.DEFAULT_VALUE))

    async def run(self, inputs):
        value = int(self.services.get_property("value", NumberInputNode.DEFAULT_VALUE))
        return { "data_out": value }


