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

telesto.topology_designer = null;

telesto.TopologyDesigner = class  {

    constructor(services, parameters) {
        this.services = services;
        this.skadi = null;
        this.services.add_message_listener((msg) => {
            this.recv(msg);
        });
        this.download_url = "";

        const path = window.location.pathname;

        const path_parts = path.split("/");
        const path_len = path_parts.length;

        let workspace_id = path_parts[path_len-4];
        let topology_id = path_parts[path_len-2];

        this.engine = new telesto.TopologyEngine(this,parameters["restartable"] || false);
        let plugins = {
            "engine": this.engine,
            "topology_store": new telesto.TopologyStore(this, {})
        }

        let options = {
            "package_urls":parameters["package_urls"],
            "platform_extensions": parameters["platform_extensions"],
            "workspace_id": workspace_id,
            "topology_id": topology_id,
            "designer_title": "Telesto Topology Designer",
            "directory_title": "Telesto Topology Directory",
            "splash": {
                "title": "Telesto Topology Designer",
                "image_url": "skadi/images/skadi.svg"
            },
            "directory_url": "../../topology_directory/index.html"
        }

        if ("skadi_options" in parameters) {
            for (let option in parameters["skadi_options"]) {
                if (!(option in options)) {
                    options[option] = parameters["skadi_options"][option];
                }
            }
        }

        skadi.start_designer(topology_id, "skadi_container", options, plugins)
            .then(skadi_designer_api => this.init(skadi_designer_api), err => console.error(err));
        telesto.topology_designer = this;
    }

    send(msg) {
        if (msg instanceof ArrayBuffer) {
            this.services.send(msg);
        } else {
            this.services.send(JSON.stringify(msg));
        }
    }

    recv(msg) {
        this.engine.handle(msg);
    }

    set_download_url(url) {
        this.download_url = url;
    }

    get_download_url() {
        return this.download_url;
    }

    upload(file_contents) {
        let msg_header = {
            "action": "upload_topology"
        }
        let message_content = [msg_header].concat(file_contents);
        let enc_msg = NarviMessageUtils.encode_message(...message_content);
        this.send(enc_msg);
    }

    init(skadi_designer_api) {
        this.skadi = skadi_designer_api;
    }

    load(from_obj) {
        this.send(from_obj); // binary message will be automatically interpreted by the peer as a load command
    }
}


