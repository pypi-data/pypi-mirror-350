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

import os
import json
import shutil
import logging

from narvi.base.webapp_base import WebappBase
from .topology_utils import list_topologies

class TopologyDirectory(WebappBase):

    package_metadata = []

    def __init__(self, webapp_services, workspace_path, packages, applications):
        self.logger = logging.getLogger("TopologyDirectory")
        self.webapp_services = webapp_services
        self.applications = applications
        self.workspace_folder = workspace_path
        self.package_urls = []
        self.webapp_services.add_message_listener(lambda msg, sid: self.recv(msg, sid))
        self.webapp_services.add_session_open_listener(lambda app_name, sid, query_parameters, headers: self.handle_session_open(app_name, sid,query_parameters,headers))

        for package_id in packages:
            self.package_urls.append(f"schema/{package_id}")

    def recv(self, msg, from_session_id):
        o = json.loads(msg)
        topology_id = o["topology_id"]

        if o["action"] == "remove_topology":
            if os.path.exists(os.path.join(self.workspace_folder, topology_id, "topology.json")):
                shutil.rmtree(os.path.join(self.workspace_folder,topology_id))
        if o["action"] == "create_topology":
            topology_id = o["topology_id"]
            from_topology_id = o.get("from_topology_id",None)
            to_folder = os.path.join(self.workspace_folder, topology_id)
            if from_topology_id:
                from_folder = os.path.join(self.workspace_folder, from_topology_id)
                if os.path.isdir(from_folder):
                    shutil.copytree(from_folder, to_folder)
                    return
            path = os.path.join(to_folder, "topology.json")
            if not os.path.exists(path):
                folder = os.path.dirname(path)
                os.makedirs(folder,exist_ok=True)
                with open(path,"w") as f:
                    f.write(json.dumps({"nodes": {}, "links": {}, "metadata": {}},indent=4))

    def handle_session_open(self, app_name, sid, query_parameters, headers):
        payload = {"topologies":list_topologies(self.workspace_folder),"applications":self.applications}
        self.webapp_services.send(json.dumps(payload), for_session_id=sid)

    @staticmethod
    def get_metadata():
        from telesto import VERSION
        return [("Topology Directory",VERSION,"Browse and create topologies...","https://github.com/telesto/visual-topology")]




