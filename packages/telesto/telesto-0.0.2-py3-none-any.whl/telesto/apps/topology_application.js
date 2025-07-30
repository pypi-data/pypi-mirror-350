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

telesto.topology_application = null;

telesto.TopologyApplication = class {

    constructor(services, parameters) {
        this.services = services;
        this.parameters = parameters;

        this.services.add_message_listener((msg) => {
            this.recv(msg);
        });


        this.engine = new telesto.TopologyEngine(this,this.parameters["restartable"] || false);
        this.engine.set_load_callback((skadi_api) => this.load_callback(skadi_api));

        let plugins = {
            "engine": this.engine,
            "topology_store": new telesto.TopologyStore(this, null),
            "resource_loader": null
        }

        let options = {
            "package_urls":this.parameters["package_urls"],
            "platform_extensions": this.parameters["platform_extensions"],
            "workspace_id": this.parameters["workspace_id"]
        }

        let topology_id = this.parameters["topology_id"];

        skadi.start_application(topology_id, options, plugins).then(async skadi_app => {
            await skadi_app.start();
            configure_application_page(skadi_app);
        });
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

    load_callback(skadi_api) {

    }
}



