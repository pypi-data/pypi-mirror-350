# Telesto
# Copyright (C) 2025  Visual Topology Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import io
import os
import stat
import json
import logging
import os.path
import shutil


from hyrrokkin.schema.schema import Schema
from hyrrokkin_engine.message_utils import MessageUtils
from hyrrokkin.api.topology import Topology
from narvi.base.webapp_base import WebappBase
from hyrrokkin.engine_launchers.python_engine_launcher import PythonEngineLauncher

def get_topology_path(webapp_services, workspace):
    topology_id = webapp_services.get_service_id()
    workspace_folder = workspace["path"]
    topology_path = os.path.join(workspace_folder, topology_id)
    return topology_path


class TopologyRunner(WebappBase):

    def __init__(self, webapp_services, packages, workspace_path, hyrrokkin_options):
        self.webapp_services = webapp_services
        self.service_id = self.webapp_services.get_service_id()

        self.topology_path = os.path.join(workspace_path,self.service_id)

        # see if the topology.json file is writable
        file_stat = os.stat(os.path.join(self.topology_path,"topology.json"))
        file_mode = file_stat.st_mode
        if stat.S_IWUSR & file_mode:
            self.read_only = False
        else:
            self.read_only = True

        self.node_statuses = {}
        self.configuration_statuses = {}
        self.package_urls = []
        self.schema = Schema()
        self.session_ids = set()

        self.in_process = hyrrokkin_options.get("in_process",False)
        self.execution_limit = hyrrokkin_options.get("execution_limit", 1)

        package_list = [p["package"] for _, p in packages.items()]

        os.makedirs(self.topology_path, exist_ok=True)

        self.logger = logging.getLogger("TopologyDesigner")

        self.client_services = {}

        self.topology = Topology(execution_folder=self.topology_path, package_list=package_list)
        self.topology.load_dir()

        self.runner = self.topology.open_runner(
                engine_launcher=PythonEngineLauncher(execution_limit=self.execution_limit,in_process=self.in_process),
                status_event_handler=lambda target_id, target_type, msg, status:
                    self.update_status(target_id,target_type, msg, status),
                execution_event_handler=lambda at_time, n_id, execution_state, exception_or_result, is_manual:
                    self.update_node_execution_state(at_time, n_id, execution_state, is_manual),
                read_only=self.read_only)

        self.runner.set_execution_complete_callback(lambda: self.execution_complete())
        self.runner.set_request_open_client_callback(lambda *args: self.handle_open_client_request(*args))

        self.webapp_services.add_message_listener(lambda msg, sid: self.recv(msg, sid))
        self.webapp_services.add_session_open_listener(lambda app_name, sid, query_parameters, headers: self.handle_session_open(sid))
        self.webapp_services.add_session_close_listener(lambda sid: self.handle_session_close(sid))

        self.webapp_services.add_app_close_listener(lambda: self.close())

        handler_id, self.download_url = self.webapp_services.create_request_service(app_name="topology_designer",handler_pattern="download", request_method="GET", handler=lambda path_parameters, query_parameters, headers, request_body: self.download_topology())

        self.runner.start(terminate_on_complete=False)

    def recv(self, msg, from_session_id):
        if not isinstance(msg,bytes):
            o = json.loads(msg)
            handled = self.handle_json_message(o, from_session_id)
        else:
            dec_msg = MessageUtils.decode_message(msg)
            handled = self.handle_binary_message(dec_msg, from_session_id)
        if not handled:
            self.logger.warning(f"Unhandled message from {from_session_id}")

    def handle_session_open(self, sid):
        o = {"action":"init"}
        download_url = self.get_download_url()
        if download_url:
            o["download_url"] = download_url
        o["topology"] = self.topology.serialise()

        self.webapp_services.send(json.dumps(o), for_session_id=sid)
        for msg in self.node_statuses.values():
            self.webapp_services.send(json.dumps(msg), for_session_id=sid)
        for msg in self.configuration_statuses.values():
            self.webapp_services.send(json.dumps(msg), for_session_id=sid)

        self.session_ids.add(sid)
        self.runner.open_session(sid)

    def handle_open_client_request(self, origin_id, origin_type, session_id, client_name):
        o = {
            "action": "open_client_request",
            "target_id": origin_id,
            "target_type": origin_type,
            "client_name": client_name
        }
        if session_id is None:
            self.webapp_services.send(json.dumps(o))
        else:
            self.webapp_services.send(json.dumps(o), for_session_id=session_id)

    def handle_session_close(self, sid):
        self.session_ids.remove(sid)
        self.runner.close_session(sid)

    def forward_message_to_client(self, msg, target_type, target_id, client_name, session_id):
        header = {
            "action": "client_message",
            "client_name": client_name,
            "target_type": target_type,
            "target_id": target_id
        }
        msg = [header]+list(msg)
        enc_msg = MessageUtils.encode_message(*msg)
        self.webapp_services.send(enc_msg, for_session_id=session_id)

    def update_status(self, target_id, target_type, msg, status):
        if target_type == "configuration":
            o = {
                "action": "set_configuration_status",
                "package_id": target_id,
                "status_message": msg,
                "status_state": status
            }
            self.configuration_statuses[target_id] = o
        elif target_type == "node":
            o = {
                "action": "set_node_status",
                "node_id": target_id,
                "status_message": msg,
                "status_state": status
            }
            self.node_statuses[target_id] = o
        else:
            raise ValueError(f"Invalid target_type={target_type}")
        self.webapp_services.send(json.dumps(o))

    def update_node_execution_state(self, at_time, node_id, execution_state, is_manual):
        o = {
            "action": "set_node_execution_state",
            "node_id": node_id,
            "execution_state": execution_state
        }
        self.webapp_services.send(json.dumps(o))

    def execution_complete(self):
        o = {
            "action": "execution_complete"
        }
        self.webapp_services.send(json.dumps(o))

    def close(self):
        if not self.service_id:
            self.logger.info("Removing execution folder: " + self.topology_path)
            shutil.rmtree(self.topology_path)

    def get_download_url(self):
        return self.download_url

    def download_topology(self):
        return (200,self.topology.save_zip(),"application/zip",{})

    def handle_json_message(self, msg, from_session_id):
        action = msg["action"]
        if action == "add_node":
            node_id = msg["node_id"]
            node_type = msg["node_type"]
            x = msg["x"]
            y = msg["y"]
            metadata = msg["metadata"]
            self.topology.add_node(node_id,node_type,{},metadata, x, y)
            self.webapp_services.send(msg,except_session_id=from_session_id)
            return True
        elif action == "move_node":
            node_id = msg["node_id"]
            x = msg["x"]
            y = msg["y"]
            self.topology.update_node_position(node_id,x,y)
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "update_node_metadata":
            node_id = msg["node_id"]
            self.topology.update_node_metadata(node_id,msg["metadata"])
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "add_link":
            link_id = msg["link_id"]
            from_node_id = msg["from_node"]
            from_port_name = msg["from_port"]
            to_node_id = msg["to_node"]
            to_port_name = msg["to_port"]
            self.topology.add_link(link_id, from_node_id, from_port_name, to_node_id, to_port_name)
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "remove_node":
            node_id = msg["node_id"]
            self.topology.remove_node(node_id)
            if node_id in self.node_statuses:
                del self.node_statuses[node_id]
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "remove_link":
            link_id = msg["link_id"]
            self.topology.remove_link(link_id)
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "clear":
            self.topology.clear()
            self.webapp_services.send(msg, except_session_id=from_session_id)
            return True
        elif action == "pause_execution":
            self.runner.pause()
            return True
        elif action == "resume_execution":
            self.runner.resume()
            return True
        elif action == "restart_execution":
            self.runner.restart()
            return True
        elif action == "open_client":
            client_name = msg["client_name"]
            target_type = msg["target_type"]
            target_id = msg["target_id"]
            client_options = msg["client_options"]
            key = (target_type, target_id, from_session_id, client_name)
            if target_type == "node":
                self.client_services[key] = self.runner.attach_node_client(target_id, from_session_id, client_name, client_options)
            elif target_type == "configuration":
                self.client_services[key] = self.runner.attach_configuration_client(target_id, from_session_id, client_name, client_options)
            else:
                self.logger.warning(f"Unable to open client for target_type={target_type}")
                return True
            self.client_services[key].set_message_handler(lambda *msg: self.forward_message_to_client(msg, target_type, target_id, client_name, from_session_id))
            return True
        elif action == "close_client":
            client_name = msg["client_name"]
            target_type = msg["target_type"]
            target_id = msg["target_id"]
            key = (target_type, target_id, from_session_id, client_name)
            if key in self.client_services:
                self.client_services[key].close()
                del self.client_services[key]
            return True
        else:
            return False

    def handle_binary_message(self, dec_msg, from_session_id):
        header = dec_msg[0]
        content = dec_msg[1:]
        action = header["action"]
        if action == "upload_topology":
            self.load_from(content[0])
            return True
        elif action == "client_message":
            client_name = header["client_name"]
            target_type = header["target_type"]
            target_id = header["target_id"]
            key = (target_type, target_id, from_session_id, client_name)
            if key in self.client_services:
                self.client_services[key].send_message(*content)
            return True
        else:
            return False

    def load_from(self, from_bytes):
        f = io.BytesIO(from_bytes)
        self.runner.pause()
        (loaded_node_ids, loaded_link_ids, node_renamings) = self.topology.load_zip(f)
        for node_id in loaded_node_ids:
            msg = self.topology.serialise_node()
            msg["action"] = "add_node"
            self.webapp_services.send(json.dumps(msg))
        for link_id in loaded_link_ids:
            msg = self.topology.serialise_link(link_id)
            msg["action"] = "add_link"
            self.webapp_services.send(json.dumps(msg))
        self.runner.resume()

    def save(self):
        if self.topology_path:
            with open(self.topology_path,"wb") as f:
                self.topology.save(f)




