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

telesto.TopologyStore = class extends skadi.StoreBase {

    constructor(webapp, topologies) {
        super();
        this.webapp = webapp;
        this.topologies = topologies;
    }

    /**
     * Initialise the store
     *
     * @returns {Promise<void>}
     */
    async init()  {
    }

    /**
     * Create a new, empty, topology in the store
     *
     * @param {string} topology_id
     * @param {?string} from_topology_id
     * @returns {Promise<void>}
     */
    async create_topology(topology_id, from_topology_id) {
        this.webapp.send({"action":"create_topology","topology_id":topology_id, "from_topology_id":from_topology_id});
    }

    /**
     * Remove a topology from the store, if it exists
     *
     * @param topology_id
     * @returns {Promise<void>}
     */
    async remove_topology(topology_id) {
        this.webapp.send({"action":"remove_topology", "topology_id":topology_id});
    }

    /**
     * @typedef  TopologyMetadata
     * @type {object}
     * @property {string} name - the topology name.
     * @property {string} description - the topology name.
     * @property {?string} version - the topology version.
     * @property {?number} authors - list of authors.
     *
     */

    /**
     * Get an array of all the topology ids in the store
     *
     * @returns {Promise<string[]>}
     */
    async list_topologies() {
        return Object.keys(this.topologies);
    }

    /**
     * Check if a topology exists in the store
     *
     * @param {string} topology_id the id of the topology
     * @returns {Promise<boolean>}
     */
    async topology_exists(topology_id) {
        return topology_id in this.topologies;
    }

    /**
     * Return a list of topologies, where the key is the topology metadata
     *
     * @returns {Promise<Object.<string, TopologyMetadata>>}
     */
    async get_topology_details() {
        return this.topologies;
    }

    /**
     * Get the metadata for a topology
     *
     * @returns {Promise<TopologyMetadata>}
     */
    async get_topology_metadata(topology_id) {
        return this.topologies[topology_id];
    }

    /**
     * Load the topology from the store into the bound skadi instance
     *
     * @param {string} topology_id the id of the topology to load
     *
     * @returns {Promise<void>}
     */
    async load_topology(topology_id) {
        return {};
    }

    /**
     *
     */
    bind() {
    }

    async save() {
    }

    async get_save_link() {
        return this.webapp.get_download_url();
    }

    async load_from(file, node_renamings) {
        // FIXME what about node renamings?
        file.arrayBuffer().then(array_buffer => {
            this.webapp.upload(array_buffer);
        });
    }

    get_file_suffix() {
        return ".zip";
    }
}
