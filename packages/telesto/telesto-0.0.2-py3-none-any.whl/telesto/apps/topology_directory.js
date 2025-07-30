/*
  Telesto
  Copyright (C) 2025 Visual Topology Ltd

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.

  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var telesto = telesto || {};

telesto.TopologyDirectory = class {

    constructor(services, parameters) {
        this.services = services;
        this.parameters = parameters;
        this.designer_app_name = parameters.designer_app_name;

        this.services.add_message_listener(async (msg) => {
            await this.recv(msg);
        });

        this.skadi_directory_api = null;
    }

    send(msg) {
        this.services.send(JSON.stringify(msg));
    }

    async recv(msg_txt) {
        let payload = JSON.parse(msg_txt);
        let topologies = payload["topologies"];
        let applications = payload["applications"];
        let options = {
            "l10n_url": "static/skadi/l10n",
            "package_urls": this.parameters["package_urls"],
            "title": "Topology Directory"
        }
        if ("skadi_options" in this.parameters) {
            for (let option in this.parameters["skadi_options"]) {
                if (!(option in options)) {
                    options[option] = this.parameters["skadi_options"][option];
                }
            }
        }
        let topology_store = new telesto.TopologyStore(this,topologies);
        let plugins = {
            "topology_store": topology_store
        }
        this.skadi_directory_api = new skadi.DirectoryApi("skadi_container", options, plugins, applications);

        this.skadi_directory_api.set_open_topology_in_designer_handler((topology_id) => {
            let target_url = "../../" + this.designer_app_name + "/" + topology_id + "/index.html";
            window.open(target_url);
        });

        await this.skadi_directory_api.load();
    }
}



