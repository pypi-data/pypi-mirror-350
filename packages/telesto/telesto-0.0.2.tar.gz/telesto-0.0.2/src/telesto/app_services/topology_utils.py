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

import json
import os.path

import logging

logger = logging.getLogger("topology_utils")

def list_topologies(workspace_folder):
    topologies = {}
    os.makedirs(workspace_folder,exist_ok=True)
    if os.path.isdir(workspace_folder):
        topology_ids = os.listdir(workspace_folder)
        for topology_id in topology_ids:
            topology_path = os.path.join(workspace_folder,topology_id,"topology.json")
            try:
                package_ids = []
                with open(topology_path) as f:
                    obj = json.loads(f.read())
                    metadata = obj.get("metadata",{})
                    for node_id in obj.get("nodes",{}):
                        node_type = obj["nodes"][node_id].get("node_type","")
                        if node_type:
                            package_id = node_type.split(":")[0]
                            if package_id not in package_ids:
                                package_ids.append(package_id)

                topologies[topology_id] = {"metadata":metadata, "package_ids":package_ids }
            except Exception as ex:
                logger.exception(f"reading topology {topology_id}")
    return topologies