/*   Skadi - A visual modelling tool for constructing and executing directed graphs.

     Copyright (C) 2022-2024 Visual Topology Ltd

     Licensed under the MIT License
*/

/* src/js/page/page_service.js */

var skadi = skadi || {};

skadi.PageService = class {

    constructor(w) {
        this.event_handlers = [];
        this.page_message_handler = null;
        this.pending_page_messages = [];
        this.window = w;
        window.addEventListener("message", (event) => {
            if (event.source === this.window) {
                this.recv_message(event.data);
            }
        });
    }

    init(language, bundle) {
        let msg_header = {
            "type": "page_init",
            "bundle": bundle,
            "language": language
        }
        this.send_fn(msg_header);
    }

    send_fn(...msg) {
        this.window.postMessage(msg,window.location.origin);
    }

    set_message_handler(handler) {
        this.page_message_handler = handler;
        this.pending_page_messages.forEach((m) => this.page_message_handler(...m));
        this.pending_page_messages = [];
    }

    send_message(...message) {
        let msg_header = {
            "type": "page_message"
        }
        this.send_fn(...[msg_header,message]);
    }

    recv_message(msg) {
        let header = msg[0];
        let type = header.type;
        switch (type) {
            case "page_message":
                if (this.page_message_handler) {
                    this.page_message_handler(...msg[1]);
                } else {
                    this.pending_page_messages.push(msg[1]);
                }
                break;
            default:
                console.error("Unknown message type received from page: " + msg.type);
        }
    }

}

/* src/js/plugins/store_base.js */

var skadi = skadi || {};

skadi.StoreBase = class {

    /**
     * Initialise the store
     *
     * @returns {Promise<void>}
     */
    async init()  {
    }

    /**
     * Create a new topology in the store
     *
     * @param {string} topology_id ID of new topology
     * @param {?string} from_topology_id ID of a topology to copy, if provided
     * @returns {Promise<void>}
     */
    async create_topology(topology_id, from_topology_id) {
    }

    /**
     * Remove a topology from the store, if it exists
     *
     * @param topology_id
     * @returns {Promise<void>}
     */
    async remove_topology(topology_id) {

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

    }

    /**
     * Check if a topology exists in the store
     *
     * @param {string} topology_id the id of the topology
     * @returns {Promise<boolean>}
     */
    async topology_exists(topology_id) {

    }

    /**
     * Return a list of topologies, where the key is the topology metadata
     *
     * @returns {Promise<Object.<string, TopologyMetadata>>}
     */
    async get_topology_details() {

    }

    /**
     * Get the metadata for a topology
     *
     * @returns {Promise<TopologyMetadata>}
     */
    async get_topology_metadata(topology_id) {

    }

    /**
     * Load the topology from the store into the bound skadi instance
     *
     * @param {string} topology_id the id of the topology to load
     *
     * @returns {Promise<void>}
     */
    async load_topology(topology_id) {
    }

    /**
     *
     */
    bind() {
    }

    async save() {
    }

    async get_save_link() {
    }

    async load_from(file, node_renamings) {
    }

    get_file_suffix() {
    }

}

/* src/js/graph_worker_engine/worker.js */

var skadi = skadi || {};

skadi.Worker = class {

    constructor() {
        this.driver = null;
    }

    async init(o) {
        o["imports"].forEach( name => {
            importScripts(name);
        });

    }

    async recv(msg) {
        // first message should be init
        let o = msg[0];
        if (o.action == "init") {
            await this.init(o);
            this.driver = new hyrrokkin_engine.ExecutionWorker(message_parts => this.send(message_parts));
        }
        if (this.driver) {
            this.driver.recv(msg);
        }
    }

    send(message_parts) {
        postMessage(message_parts);
    }
}

skadi.worker = new skadi.Worker();

onmessage = async (e) => {
    await skadi.worker.recv(e.data);
}

