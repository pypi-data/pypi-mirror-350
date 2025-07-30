/*       
    Hyrrokkin - a library for building and running executable graphs

    MIT License - Copyright (C) 2022-2025  Visual Topology Ltd

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software
    and associated documentation files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or
    substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
    BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
/* hyrrokkin_engine/client_service_interface.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

/**
 * Define an interface used by nodes to communicate with clients
 *
 * @type {hyrrokkin_engine.ClientServiceInterface}
 */
hyrrokkin_engine.ClientServiceInterface = class {

    /**
     * @callback messageReceivedCallback
     *
     * @param {...*} a message consists of zero or more components
     */

    /**
     * set a function used to receive messages
     *
     * @param {messageReceivedCallback} handler a function that will be called when a message from the client arrives
     */
    set_message_handler(handler) {
    }

    /**
     * send a message to the client
     *
     * @param {...*} message consists of zero or more components
     */
    send_message(...message) {
    }
}

/* hyrrokkin_engine/client_service.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ClientService = class {

    constructor(send_fn) {
        this.event_handlers = [];
        this.client_message_handler = null;
        this.pending_client_messages = [];
        this.send_fn = send_fn;
    }

    set_message_handler(handler) {
        this.client_message_handler = handler;
        this.pending_client_messages.forEach((m) => {
            try {
                this.client_message_handler(...m)
            } catch(e) {
                console.error(e);
            }
        });
        this.pending_client_messages = [];
    }

    send_message(...message) {
        this.send_fn(...message);
    }

    recv_message(...msg) {
        if (this.client_message_handler) {
            try {
                this.client_message_handler(...msg);
            } catch(e) {
                console.error(e);
            }
        } else {
            this.pending_client_messages.push(msg);
        }
    }
}

/* hyrrokkin_engine/message_utils.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.MessageUtils = class {

    static encode_message(...message_parts) {
        let encoded_components = [];
        let headers = [];
        let component_total_len = 0;
        message_parts.forEach(content => {
            let content_b = content;
            let header = {};
            if (content instanceof ArrayBuffer) {
                header["content_type"] = "binary";
                content_b = new Uint8Array(content);
            } else if (content === null || content === undefined) {
                header["content_type"] = "null";
                content_b = new ArrayBuffer(0);
            } else if (content instanceof String) {
                content_b = new TextEncoder().encode(content);
                header["content_type"] = "string";
            } else {
                content_b = new TextEncoder().encode(JSON.stringify(content));
                header["content_type"] = "json";
            }
            header["length"] = content_b.byteLength;
            headers.push(header);
            encoded_components.push(content_b);
            component_total_len += content_b.byteLength;
        });

        let header = { "components": headers }
        let header_s = JSON.stringify(header);
        let header_b = new TextEncoder().encode(header_s);
        let header_len = new ArrayBuffer(4);
        new DataView(header_len).setInt32(0,header_b.byteLength,false);

        let msg_buffer = new ArrayBuffer(4+header_b.byteLength+component_total_len);
        let dv = new Uint8Array(msg_buffer);
        dv.set(new Uint8Array(header_len),0);
        dv.set(header_b,4);
        let offset = 4+header_b.byteLength;
        for(let idx=0; idx<encoded_components.length; idx+=1) {
            dv.set(encoded_components[idx],offset);
            offset += headers[idx].length;
        }
        return msg_buffer;
    }

    static decode_message(msg_buffer) {
        let decoded = [];
        let view = new DataView(msg_buffer);
        let header_len = view.getInt32(0);
        let header_b = msg_buffer.slice(4, 4 + header_len);
        let header_s = new TextDecoder().decode(header_b);
        let header = JSON.parse(header_s);
        let offset = 4+header_len;
        header.components.forEach(component => {
            let content_b = msg_buffer.slice(offset,offset+component.length);
            let content = null;
            switch(component.content_type) {
                case "string":
                    content = (new TextDecoder()).decode(content_b);
                    break;
                case "binary":
                    content = content_b;
                    break;
                case "json":
                    content = JSON.parse((new TextDecoder()).decode(content_b));
                    break;
            }
            offset += component.length;
            decoded.push(content);
        });
        return decoded;
    }
}

/* hyrrokkin_engine/wrapper.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.Wrapper = class {

    constructor(target_id, target_type, data_store_utils, services,  send_message_cb) {
        this.target_id = target_id;
        this.target_type = target_type;
        this.data_store_utils = data_store_utils;
        this.services = services;
        this.client_services = {};
        this.instance = null;
        this.services.wrapper = this;
        this.send_message_cb = send_message_cb;
    }

    set_instance(instance) {
        this.instance = instance;
    }

    get_instance() {
        return this.instance;
    }

    async load_properties() {
        await this.data_store_utils.load_properties();
    }

    get_property(property_name, default_value) {
        return this.data_store_utils.get_property(property_name, default_value);
    }

    set_property(property_name, property_value) {
        this.data_store_utils.set_property(property_name,property_value);
    }

    async get_data(key) {
        return await this.data_store_utils.get_data(key);
    }

    async set_data(key, data) {
        await this.data_store_utils.set_data(key, data);
    }

    get_services() {
        return this.services;
    }

    open_client(session_id, client_name, client_options) {
        if (this.instance && this.instance.open_client) {
            try {
                let client_service = new hyrrokkin_engine.ClientService( (...msg) => {
                    this.send_message_cb(session_id, client_name, ...msg);
                });
                this.instance.open_client(session_id, client_name, client_options, client_service);
                this.client_services[session_id+":"+client_name] = client_service;
            } catch(e) {
                console.error(e);
            }
        }
    }

    recv_message(session_id, client_name, ...msg) {
        let client_service = this.client_services[session_id+":"+client_name];
        if (client_service) {
            client_service.recv_message(...msg);
        }
    }

    close_client(session_id, client_name) {
        delete this.client_services[session_id+":"+client_name];
        if (this.instance && this.instance.close_client) {
            try {
                this.instance.close_client(session_id, client_name);
            } catch(e) {
                console.error(e);
            }
        }
    }
}

/* hyrrokkin_engine/port_type.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.PortType = class {
  
  constructor(direction, is_input) {
    this.direction = direction;
    this.link_type = "";
    this.metadata = {};
    this.allow_multiple_connections = null;
    this.is_input = is_input;
  }

  deserialise(obj) {
    if (obj["link_type"]) {
      this.link_type = obj["link_type"];
    }
    if (obj["metadata"]) {
      this.metadata = obj["metadata"];
    }
    if ("allow_multiple_connections" in obj) {
      this.allow_multiple_connections = obj["allow_multiple_connections"];
    } else {
      this.allow_multiple_connections = false;
    }
  }

  get_link_type() {
    return this.link_type;
  }

  get_allow_multiple_connections() {
    return this.allow_multiple_connections;
  }
}



/* hyrrokkin_engine/link_type.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.LinkType = class {
  
  constructor(link_type_id, package_type, schema) {
    let metadata = schema["metadata"] || { "name": "?", "description":"?"};
    this.id = package_type.get_qualified_id(link_type_id);
    this.package_id = package_type.get_id();
    this.name = metadata.name;
    this.description = metadata.description;
  }

  get_id() {
    return this.id;
  }

  get_package_id() {
    return this.package_id;
  }

  get_name() {
    return this.name;
  }

  get_description() {
    return this.description;
  }
}



/* hyrrokkin_engine/node_type.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.NodeType = class {

  constructor(node_type_id, package_type, schema) {
    this.id = package_type.get_qualified_id(node_type_id);
    this.package_type = package_type;
    this.schema = schema;
    this.package_id = package_type.get_id();
    this.metadata = schema["metadata"] || { "name": nodeTypeId, "description":""};

    let input_ports = schema["input_ports"] || {};
    let output_ports = schema["output_ports"] || {};

    this.input_ports = {};
    this.output_ports = {};

    for (let key in input_ports) {
      let pt = new hyrrokkin_engine.PortType("input", true);
      pt.deserialise(input_ports[key]);
      this.input_ports[key] = pt;
    }

    for (let key in output_ports) {
      let pt = new hyrrokkin_engine.PortType("output", false);
      pt.deserialise(output_ports[key]);
      this.output_ports[key] = pt;
    }
  }

  get_name() {
    return this.package_type.localise(this.metadata.name);
  }

  get_description() {
    return this.package_type.localise(this.metadata.description);
  }


  get_schema() {
    return this.schema;
  }

  allow_multiple_input_connections(input_port_name) {
    return this.input_ports[input_port_name].get_allow_multiple_connections();
  }

  allow_multiple_output_connections(output_port_name) {
    return this.output_ports[output_port_name].get_allow_multiple_connections();
  }

  get_input_link_type(input_port_name) {
    return this.input_ports[input_port_name].get_link_type();
  }

  get_output_link_type(output_port_name) {
    return this.output_ports[output_port_name].get_link_type();
  }

  get_id() {
    return this.id;
  }

  get_type() {
    return this.id;
  }

  get_package_id() {
    return this.package_id;
  }

  get_package_type() {
    return this.package_type;
  }
}




/* hyrrokkin_engine/package_type.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.PackageType = class {
  
  constructor(id, url, obj) {
    this.id = id;
    this.metadata = obj["metadata"];

    this.base_url = url;
    this.configuration = obj["configuration"];
    this.sources = [];
    this.node_types = {};
    this.link_types = {};
    this.schema = obj;

    let node_types = obj["node_types"];
    for(let node_type_id in node_types) {
        let node_type = this.create_node_type(node_type_id, node_types[node_type_id]);
        this.node_types[node_type_id] = node_type;
    }

    let link_types = obj["link_types"];
    for(let link_type_id in link_types) {
        let link_type = this.create_link_type(link_type_id, link_types[link_type_id]);
        this.link_types[link_type_id] = link_type;
    }
  }

  create_node_type(node_type_id, node_type_schema) {
     return new hyrrokkin_engine.NodeType(node_type_id, this, node_type_schema);
  }

  create_link_type(link_type_id, link_type_schema) {
     return new hyrrokkin_engine.NodeType(link_type_id, this, link_type_schema);
  }

  async load_sources() {
    const sources_url = this.base_url + "/sources_js.txt";
    try {
      this.sources = await fetch(sources_url)
          .then(
              r => r.text()
          ).then(
              sources => sources.split("\n").map(s => s.trim()).filter(s => s.length > 0)
          );
    } catch(e) {
      this.sources = [];
    }
  }

  get_sources() {
    return this.sources;
  }

  get_schema() {
    return this.schema;
  }

  get_id() {
    return this.id;
  }

  get_node_types() {
    return this.node_types;
  }

  get_node_type(node_type_id) {
    return this.node_types[node_type_id];
  }

  get_link_types() {
    return this.link_types;
  }

  get_metadata() {
    return this.metadata;
  }

  get_base_url() {
    return this.base_url;
  }

  get_resource_url(resource) {
    if (resource.startsWith("http")) {
      // resource is already an absolute URL
      return resource;
    }
    let resource_url =  this.base_url+"/"+resource;
    return String(resource_url);
  }

  get_qualified_id(id) {
    return this.id + ":" + id;
  }

  get_configuration() {
    return this.configuration;
  }
}

hyrrokkin_engine.PackageType.load = function(id, obj, url) {
  return new hyrrokkin_engine.PackageType(id, url, obj);
}



/* hyrrokkin_engine/configuration_service_interface.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

/**
 * An interface supplying services to a package configuration
 *
 * @type {hyrrokkin_engine.ConfigurationServiceInterface}
 */
hyrrokkin_engine.ConfigurationServiceInterface = class {

    /**
     * Get the unique ID of this package
     *
     * @returns {string} the package id
     */
    get_package_id() {
    }

    /**
     * Get the value of a named property
     *
     * @param {string} property_name the property name
     * @param {*} default_value a default value for the property
     *
     * @returns {*} the value of the property or the default value if the property is not defined
     */
    get_property(property_name, default_value) {
    }

    /**
     * Sets the value of a named property
     *
     * @param {string} property_name the property name
     * @param (*} property_value must be JSON serialisable
     */
    set_property(property_name, property_value) {
    }

    /**
     * Retrieve data associated with a key or null if no data is associated with that key
     *
     * @param {string} key the key value
     *
     * @return {Promise<(ArrayBuffer|null)>}
     */
    async get_data(key) {
    }

    /**
     * Store data associated with a key
     *
     * @param {string} key the key value
     * @param {(ArrayBuffer|null)} data the data value (pass null to delete data associated with the key)
     *
     * @return {Promise<void>}
     */
    async set_data(key, data) {
    }

    /**
     * Sets an informational status message for this package
     *
     * @param {string} status_msg the status message, or empty string to clear the status
     * @param {string} level, one of "info", "warning", "error"
     */
    set_status(status_msg, level) {
    }

    /**
     * Resolve a relative resource path based on the location of the package schema
     *
     * @param resource_path
     */
    resolve_resource(resource_path) {
    }

    /**
     * Gets the configuration instance associated with a package.
     *
     * @param {string} package_id the id of the package
     *
     * @returns {(object|null)} the configuration instance or null if no configuration is defined for the package
     */
    get_configuration(package_id) {
    }

    /**
     * Called to request that a client of this configuration be opened
     *
     * @param {string} client_name: the type of client to load
     * @param {string|undefined} session_id: the session in which the client should be opened (if undefined, open in all sessions)
     */
    request_open_client(client_name, session_id) {
    }

}

/* hyrrokkin_engine/configuration_service.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ConfigurationService = class extends hyrrokkin_engine.ConfigurationServiceInterface {

    constructor(package_id, base_url) {
        super();
        this.package_id = package_id;
        this.base_url = base_url;
        this.wrapper = null;
    }

    get_property(property_name, default_value) {
        return this.wrapper.get_property(property_name, default_value);
    }

    set_property(property_name, property_value) {
        this.wrapper.set_property(property_name, property_value);
    }

    resolve_resource(resource_path) {
        return this.base_url + "/" + resource_path;
    }

    async get_data(key) {
        return await this.wrapper.get_data(key);
    }

    async set_data(key, data) {
        await this.wrapper.set_data(key, data);
    }

    set_status(status_msg, level) {
        if (!status_msg) {
            status_msg = "";
        }
        if (!level) {
            level = "info";
        }
        this.wrapper.set_status(status_msg, level);
    }

    get_configuration(package_id) {
        let configuration_wrapper = this.wrapper.get_configuration(package_id);
        if (configuration_wrapper) {
            return configuration_wrapper.get_instance();
        } else {
            return null;
        }
    }

    request_open_client(client_name) {
        this.wrapper.request_open_client(client_name);
    }
}


/* hyrrokkin_engine/configuration_wrapper.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ConfigurationWrapper = class extends hyrrokkin_engine.Wrapper {

    constructor(executor, data_store_utils, package_id, services, send_message_cb) {
        super(package_id, "configuration", data_store_utils, services, send_message_cb);
        this.executor = executor;
        this.package_id = package_id;
    }

    get_configuration(package_id) {
        return this.executor.get_configuration(package_id);
    }

    set_status(status_msg, level) {
        this.executor.update_configuration_status(this.package_id, level, status_msg);
    }

    request_open_client(client_name, session_id) {
        this.executor.request_open_client(this.package_id, "configuration", session_id, client_name);
    }

    open_session(session_id) {
        if (this.instance.open_session) {
            try {
                this.instance.open_session(session_id);
            } catch(ex) {
                console.error(ex);
            }
        }
    }

    close_session(session_id) {
        if (this.instance.close_session) {
            try {
                this.instance.close_session(session_id);
            } catch(ex) {
                console.error(ex);
            }
        }
    }

    decode(encoded_bytes, link_type) {
        if (this.instance.decode) {
            try {
                return this.instance.decode(encoded_bytes, link_type);
            } catch (ex) {
                console.error(ex);
            }
        }
        return null;
    }

    encode(value, link_type) {
        if (this.instance.encode) {
            try {
                return this.instance.encode(value, link_type);
            } catch (ex) {
                console.error(ex);
            }
        }
        return null;
    }
}

/* hyrrokkin_engine/node_service_interface.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

/**
 * An interface supplying services to a node
 *
 * @type {hyrrokkin_engine.NodeServiceInterface}
 */
hyrrokkin_engine.NodeServiceInterface = class {

    /**
     * Get the unique ID of this node
     *
     * @returns {string} the node id
     */
    get_node_id() {
    }

    /**
     * Request that this node is re-run.  Typically called after a change to the node that would alter the output values
     * if there was no change to the inputs.
     */
    request_run() {
    }

    /**
     * Get the value of a named property
     *
     * @param {string} property_name the property name
     * @param {*} default_value a default value for the property
     *
     * @returns {*} the value of the property or the default value if the property is not defined
     */
    get_property(property_name, default_value) {
    }

    /**
     * Sets the value of a named property
     *
     * @param {string} property_name the property name
     * @param (*} property_value must be JSON serialisable
     */
    set_property(property_name, property_value) {
    }

    /**
     * Retrieve data associated with a key or null if no data is associated with that key
     *
     * @param {string} key the key value
     *
     * @return {Promise<(ArrayBuffer|null)>}
     */
    async get_data(key) {
    }

    /**
     * Store data associated with a key
     *
     * @param {string} key the key value
     * @param {(ArrayBuffer|null)} data the data value (pass null to delete data associated with the key)
     *
     * @return {Promise<void>}
     */
    async set_data(key, data) {
    }

    /**
     * Sets a status message for this node
     *
     * @param {string} status_msg the status message, or empty string to clear the status
     * @param {string} level, one of "info", "warning", "error"
     */
    set_status(status_msg, level) {
    }

    /**
     * Take manual control of the execution state
     *
     * @param {string} new_state one of "pending", "executing", "executed", "failed"
     */
    set_execution_state(new_state) {
    }

    /**
     * Resolve a relative resource path based on the location of the package schema
     *
     * @param resource_path
     */
    resolve_resource(resource_path) {
    }

    /**
     * Gets the configuration instance associated with a package.
     *
     * @param {string} [package_id] the id of the package, use the node's package id if not provided
     *
     * @returns {(object|null)} the configuration instance or null if no configuration is defined for the package
     */
    get_configuration(package_id) {
    }

    /**
     * Called to request that a client of this node be opened
     *
     * @param {string} client_name: the type of client to open
     * @param {string|undefined} session_id: the session in which the client should be opened (if undefined, open in all sessions)
     */
    request_open_client(client_name, session_id) {
    }

}


/* hyrrokkin_engine/node_service.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.NodeService = class extends hyrrokkin_engine.NodeServiceInterface {

    constructor(node_id, base_url) {
        super();
        this.node_id = node_id;
        this.base_url = base_url;
        this.wrapper = null;
    }

    get_property(property_name, default_value) {
        return this.wrapper.get_property(property_name, default_value);
    }

    set_property(property_name, property_value) {
        this.wrapper.set_property(property_name, property_value);
    }

    resolve_resource(resource_path) {
        return this.base_url + "/" + resource_path;
    }

    async get_data(key) {
        return await this.wrapper.get_data(key);
    }

    async set_data(key, data) {
        await this.wrapper.set_data(key, data);
    }

    get_node_id() {
        return this.node_id;
    }

    get_configuration(package_id) {
        let configuration_wrapper = this.wrapper.get_configuration(package_id);
        if (configuration_wrapper) {
            return configuration_wrapper.get_instance();
        } else {
            return null;
        }
    }

    request_run() {
        this.wrapper.request_execution(this.node_id);
    }

    set_status(status_msg, level) {
        if (!status_msg) {
            status_msg = "";
        }
        if (!level) {
            level = "info";
        }
        this.wrapper.set_status(status_msg, level);
    }

    set_execution_state(new_state) {
        this.wrapper.set_execution_state(new_state);
    }

    request_open_client(client_name, session_id) {
        this.wrapper.request_open_client(client_name, session_id);
    }
}


/* hyrrokkin_engine/node_wrapper.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.NodeWrapper = class extends hyrrokkin_engine.Wrapper {

    constructor(executor, data_store_utils, node_id, services, package_id, base_url, send_message_cb) {
        super(node_id, "node", data_store_utils, services, send_message_cb);
        this.executor = executor;
        this.package_id = package_id;
        this.base_url = base_url;
        this.node_id = node_id;
    }

    reset_execution() {
        if (this.instance && this.instance.reset_run) {
            try {
                this.instance.reset_run();
            } catch(e) {
                console.error(e);
            }
        }
    }

    set_status(status_msg, level) {
        this.executor.update_node_status(this.node_id, level, status_msg);
    }

    set_execution_state(new_state) {
        this.executor.update_execution_state(this.node_id, new_state, true);
    }

    async execute(inputs) {
        if (this.instance && this.instance.run) {
            try {
                return await this.instance.run(inputs);
            } catch(e) {
                throw e;
            }
        }
        return {};
    }

    get_configuration(package_id) {
        return this.executor.get_configuration(package_id || this.package_id);
    }

    request_execution() {
        this.executor.request_execution(this.node_id);
    }

    request_open_client(client_name, session_id) {
        this.executor.request_open_client(this.node_id, "node", session_id, client_name);
    }

    remove() {
        if (this.instance && this.instance.remove) {
            try {
                this.instance.remove();
            } catch(e) {
                console.error(e);
            }
        }
    }
}

/* hyrrokkin_engine/graph_link.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.GraphLink = class {

    constructor(executor, from_node_id, from_port, to_node_id, to_port) {
        this.executor = executor;
        this.from_node_id = from_node_id;
        this.from_port = from_port;
        this.to_node_id = to_node_id;
        this.to_port = to_port;
    }

    get_value() {
        if (this.from_node_id in this.executor.node_outputs) {
            let outputs = this.executor.node_outputs[this.from_node_id];
            if (outputs && this.from_port in outputs) {
                return outputs[this.from_port];
            }
        }
        return null;
    }
}


/* hyrrokkin_engine/graph_executor.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.GraphExecutor = class {

    constructor(data_store_utils_factory, execution_limit, execution_complete_callback,
                execution_state_callback, node_status_callback, configuration_status_callback,
                send_message_callback, output_notification_callback, request_open_client_callback) {
        hyrrokkin_engine.graph_executor = this;

        this.data_store_utils_factory = data_store_utils_factory;
        this.injected_inputs = {};  // node-id => input-port => value
        this.output_listeners = {}; // node-id => output-port => true

        this.node_wrappers = {}; // node-id => node-wrapper
        this.links = {}; // link-id => GraphLink
        this.out_links = {}; // node-id => output-port => [GraphLink]
        this.in_links = {};  // node-id => input-port => [GraphLink]

        this.configuration_wrappers = {}; // package-id => configuration-wrapper
        this.base_urls = {}; // package-id => base_url

        this.dirty_nodes = {}; // node-id => True
        this.executing_nodes = {}; // node-id => True
        this.executed_nodes = {};  // node-id => True
        this.failed_nodes = {};    // node-id => Exception
        this.execution_limit = execution_limit;
        this.node_outputs = {}; // node-id => output-port => value

        this.paused = true;

        this.node_types = {};
        this.package_schemas = {};

        this.execution_complete_callback = execution_complete_callback;
        this.execution_state_callback = execution_state_callback;
        this.node_status_callback = node_status_callback;
        this.configuration_status_callback = configuration_status_callback;
        this.send_message_callback = send_message_callback;
        this.output_notification_callback = output_notification_callback;
        this.request_open_client_callback = request_open_client_callback;
    }

    inject_input(node_id, input_port_name, encoded_bytes) {
        if (encoded_bytes === null) {
            if (node_id in this.injected_inputs) {
                if (input_port_name in this.injected_inputs[node_id]) {
                    delete this.injected_inputs[node_id][input_port_name];
                }
            }
        } else {
            if (!(node_id in this.injected_inputs)) {
                this.injected_inputs[node_id] = {};
            }
            this.injected_inputs[node_id][input_port_name] = encoded_bytes;
        }
        this.mark_dirty(node_id);
    }

    add_output_listener(node_id, output_port_name) {
        if (!(node_id in this.output_listeners)) {
            this.output_listeners[node_id] = {};
        }
        this.output_listeners[node_id][output_port_name] = true;
    }

    remove_output_listener(node_id, output_port_name) {
        if (node_id in this.output_listeners) {
            if (output_port_name in this.output_listeners[node_id]) {
                delete this.output_listeners[node_id][output_port_name];
            }
        }
    }

    get executing_node_count() {
        return Object.keys(this.executing_nodes).length;
    }

    count_failed() {
        return Object.keys(this.failed_nodes).length;
    }

    clear() {
        let node_ids = Object.keys(this.node_wrappers);
        for(let idx=0; idx<node_ids.length; idx++) {
            this.remove_node(node_id);
        }

        this.links = {};
        this.out_links = {};
        this.in_links = {};
    }

    valid_node(node_id) {
        return (node_id in this.node_wrappers);
    }

    pause() {
        this.paused = true;
    }

    resume() {
        this.paused = false;
        this.dispatch().then(r => {
        });
    }

    mark_dirty(node_id) {
        if (node_id in this.dirty_nodes) {
            return;
        }

        this.dirty_nodes[node_id] = true;
        this.reset_execution(node_id);
        delete this.node_outputs[node_id];

        /* mark all downstream nodes as dirty */
        for (let out_port in this.out_links[node_id]) {
            let outgoing_links = this.out_links[node_id][out_port];
            outgoing_links.map((link) => this.mark_dirty(link.to_node_id));
        }
    }

    reset_execution(node_id) {
        if (!(node_id in this.node_wrappers)) {
            return;
        }
        let node = this.node_wrappers[node_id];
        this.update_execution_state(node_id, "pending");
        delete this.failed_nodes[node_id];
        delete this.executed_nodes[node_id];
        node.reset_execution();
    }

    async dispatch() {
        if (this.paused) {
            return;
        }
        let launch_nodes = [];
        let launch_limit = (this.execution_limit - this.executing_node_count);
        if (launch_limit > 0) {
            for (let node_id in this.dirty_nodes) {
                if (this.can_execute(node_id)) {
                    launch_nodes.push(node_id);
                }
                if (launch_nodes.length >= launch_limit) {
                    break;
                }
            }
        }

        if (launch_nodes.length === 0 && this.executing_node_count === 0) {
            this.execution_complete();
        }

        for (let idx = 0; idx < launch_nodes.length; idx++) {
            let node_id = launch_nodes[idx];
            this.execute(node_id);
        }
    }

    can_execute(node_id) {
        if (node_id in this.executing_nodes) {
            // cannot execute a node that is already executing
            return false;
        }
        for (let in_port in this.in_links[node_id]) {
            let in_links = this.in_links[node_id][in_port];
            for (let idx in in_links) {
                let in_link = in_links[idx];
                let pred_node_id = in_link.from_node_id;
                if (!(pred_node_id in this.executed_nodes)) {
                    return false;
                }
            }
        }
        return true;
    }

    pre_execute(node_id) {
        let inputs = {};
        let node_type_id = this.node_types[node_id];
        let package_id = node_type_id.split(":")[0];
        let node_type_name = node_type_id.split(":")[1];
        let node_type = this.package_schemas[package_id].get_node_type(node_type_name);
        let in_links = this.in_links[node_id] || {};
        for (let input_port_name in in_links) {
            if (in_links[input_port_name].length > 0) {
                let allow_multiple_connections = node_type.allow_multiple_input_connections(input_port_name);
                if (allow_multiple_connections) {
                    inputs[input_port_name] = [];
                    for (let idx in in_links[input_port_name]) {
                        let in_link = in_links[input_port_name][idx];
                        inputs[input_port_name].push(in_link.get_value());
                    }
                } else {
                    inputs[input_port_name] = in_links[input_port_name][0].get_value();
                }
            }
        }

        // add in any injected input values
        if (node_id in this.injected_inputs) {
            for (let injected_input_port_name in this.injected_inputs[node_id]) {
                let allow_multiple_connections = node_type.allow_multiple_input_connections(injected_input_port_name);
                let package_link_type = node_type.get_input_link_type(injected_input_port_name).split(":");
                let package_id = package_link_type[0];
                let link_type = package_link_type[1];
                let configuration_wrapper = this.configuration_wrappers[package_id];
                let injected_value = configuration_wrapper.decode(this.injected_inputs[node_id][injected_input_port_name],link_type);
                if (allow_multiple_connections) {
                    if (!(injected_input_port_name in inputs)) {
                        inputs[injected_input_port_name] = [];
                    }
                    inputs[injected_input_port_name].push(injected_value);
                } else {
                    inputs[injected_input_port_name] = injected_value;
                }
            }
        }

        return inputs;
    }

    execute(node_id) {
        if (!(node_id in this.node_wrappers)) {
            return;
        }
        delete this.dirty_nodes[node_id];
        this.executing_nodes[node_id] = true;
        let node = this.node_wrappers[node_id];

        let inputs = this.pre_execute(node_id);
        this.update_execution_state(node_id, "executing");

        node.execute(inputs).then(
            (outputs) => this.post_execute(node_id, outputs),
            (reason) => this.post_execute(node_id, null, reason)).then(
            () => this.dispatch()
        );
    }

    post_execute(node_id, outputs, reject_reason) {
        if (!this.valid_node(node_id)) {
            return; // node has been deleted since it started executing
        }
        delete this.executing_nodes[node_id];
        delete this.node_outputs[node_id];
        if (reject_reason) {
            this.update_execution_state(node_id, "failed");
            if (reject_reason.stack) {
                // console.error(reject_reason.stack);
            }
            this.failed_nodes[node_id] = reject_reason;
        } else {
            this.update_execution_state(node_id, "executed");
            this.node_outputs[node_id] = outputs;
            this.executed_nodes[node_id] = true;
        }

        let node_type_id = this.node_types[node_id];
        let package_id = node_type_id.split(":")[0];
        let node_type_name = node_type_id.split(":")[1];
        let node_type = this.package_schemas[package_id].get_node_type(node_type_name);

        if (node_id in this.output_listeners && this.output_notification_callback) {
            for (let port_name in outputs) {
                if (port_name in this.output_listeners[node_id]) {
                    let package_link_type = node_type.get_output_link_type(port_name).split(":");
                    let package_id = package_link_type[0];
                    let link_type = package_link_type[1];
                    let configuration_wrapper = this.configuration_wrappers[package_id];
                    let encoded_bytes = configuration_wrapper.encode(outputs[port_name],link_type);
                    this.output_notification_callback(node_id, port_name, encoded_bytes);
                }
            }
        }
    }

    create_configuration_service(package_id, base_url) {
        return new hyrrokkin_engine.ConfigurationService(package_id, base_url);
    }

    async add_package(package_id, schema, base_url, configuration_instance, configuration_service) {
        this.package_schemas[package_id] = hyrrokkin_engine.PackageType.load(package_id, schema, base_url);
        this.base_urls[package_id] = base_url;
        if (configuration_instance !== null && configuration_service !== null) {
            await this.register_package(package_id, base_url, configuration_instance, configuration_service);
        }
    }

    async register_package(package_id, base_url, configuration_instance, configuration_service) {
        let wrapper = new hyrrokkin_engine.ConfigurationWrapper(this, this.data_store_utils_factory(package_id, "configuration"), package_id, configuration_service,
            (session_id, client_name,...msg) => this.send_message_callback(package_id, "configuration",session_id, client_name, ...msg));

        await wrapper.load_properties();

        try {
            if (configuration_instance.load) {
                await configuration_instance.load();
            }
            wrapper.set_instance(configuration_instance);
        } catch(ex) {
            console.error(ex);
            wrapper.set_instance(null);
        }
        this.configuration_wrappers[package_id] = wrapper;
        return wrapper;
    }

    get_configuration(package_id) {
        return this.configuration_wrappers[package_id];
    }

    create_node_service(node_id, package_id) {
        return new hyrrokkin_engine.NodeService(node_id, this.base_urls[package_id]);
    }

    async register_node(node_id, node_type_id, instance, service) {
        let package_id = node_type_id.split(":")[0];
        let base_url = this.base_urls[package_id];

        let wrapper = new hyrrokkin_engine.NodeWrapper(this, this.data_store_utils_factory(node_id, "node"), node_id, service, package_id, base_url,
            (session_id, client_name,...msg) => this.send_message_callback(node_id, "node", session_id, client_name, ...msg));

        await wrapper.load_properties();

        try {
            if (instance.load) {
                await instance.load();
            }
            wrapper.set_instance(instance);
        } catch(ex) {
            console.error(ex);
            wrapper.set_instance(null);
        }

        return wrapper;
    }

    async add_node(node_id, node_type_id, instance, service) {
        let wrapper = await this.register_node(node_id,node_type_id, instance, service);
        this.node_types[node_id] = node_type_id;
        this.node_wrappers[node_id] = wrapper;
        this.in_links[node_id] = {};
        this.out_links[node_id] = {};
        this.node_outputs[node_id] = {};
        this.mark_dirty(node_id);
        this.dispatch().then(r => {
        });
    }

    async add_link(link_id, from_node_id, from_port, to_node_id, to_port) {

        let link = new hyrrokkin_engine.GraphLink(this, from_node_id, from_port, to_node_id, to_port);
        this.links[link_id] = link;

        if (!(from_port in this.out_links[from_node_id])) {
            this.out_links[from_node_id][from_port] = [];
        }

        if (!(to_port in this.in_links[to_node_id])) {
            this.in_links[to_node_id][to_port] = [];
        }

        this.out_links[from_node_id][from_port].push(link);
        this.in_links[to_node_id][to_port].push(link);

        this.mark_dirty(to_node_id);

        this.dispatch().then(r => {
        });
    }

    async load_target(target_id, target_type, properties, data) {
        let wrapper = null;
        if (target_type === "node") {
            wrapper = this.node_wrappers[target_id];
        } else {
            wrapper = this.configuration_wrappers[target_id];
        }
        for(let property_name in properties) {
            wrapper.set_property(property_name,properties[property_name]);
        }
        for(let data_key in data) {
            await wrapper.set_data(data_key, data[data_key]);
        }
    }

    async remove_link(link_id) {
        let link = this.links[link_id];
        delete this.links[link_id];

        let arr_out = this.out_links[link.from_node_id][link.from_port];
        arr_out.splice(arr_out.indexOf(link), 1);

        let arr_in = this.in_links[link.to_node_id][link.to_port];
        arr_in.splice(arr_in.indexOf(link), 1);

        this.mark_dirty(link.to_node_id);

        this.dispatch().then(r => {
        });
    }

    async remove_node(node_id) {
        // at this point any links into and out of this node should have been removed
        this.node_wrappers[node_id].remove();
        delete this.executing_nodes[node_id];
        delete this.failed_nodes[node_id];
        delete this.executed_nodes[node_id];
        delete this.dirty_nodes[node_id];
        delete this.node_wrappers[node_id];
        delete this.node_outputs[node_id];
        delete this.node_types[node_id];
    }

    get_node(node_id) {
        return this.node_wrappers[node_id];
    }

    request_execution(node_id) {
        this.mark_dirty(node_id);
        this.dispatch().then(r => {
        });
    }

    request_open_client(target_id, target_type, session_id, client_name) {
        if (this.request_open_client_callback) {
            this.request_open_client_callback(target_id, target_type, session_id, client_name);
        }
    }

    execution_complete() {
        if (this.execution_complete_callback) {
            this.execution_complete_callback();
        }
    }

    update_execution_state(node_id, execution_state, is_manual) {
        if (this.execution_state_callback) {
            this.execution_state_callback(node_id, execution_state, is_manual !== undefined ? is_manual : false);
        }
    }

    update_node_status(node_id, level, msg) {
        if (this.node_status_callback) {
            this.node_status_callback(node_id, level, msg);
        }
    }

    update_configuration_status(package_id, level, msg) {
        if (this.configuration_status_callback) {
            this.configuration_status_callback(package_id, level, msg);
        }
    }

    get_node_property(node_id, property_name) {
        if (node_id in this.node_wrappers) {
            return this.node_wrappers[node_id].get_property(property_name);
        } else {
            return null;
        }
    }

    set_node_property(node_id, property_name, property_value) {
        if (node_id in this.node_wrappers) {
            this.node_wrappers[node_id].set_property(property_name, property_value);
        }
    }

    get_configuration_property(package_id, property_name) {
        if (package_id in this.configuration_wrappers) {
            return this.configuration_wrappers[package_id].get_property(property_name);
        } else {
            return null;
        }
    }

    set_configuration_property(package_id, property_name, property_value) {
        if (package_id in this.configuration_wrappers) {
            this.configuration_wrappers[package_id].set_property(property_name, property_value);
        }
    }

    open_session(session_id) {
        for(let package_id in this.configuration_wrappers) {
            this.configuration_wrappers[package_id].open_session(session_id);
        }
    }

    close_session(session_id) {
        for(let package_id in this.configuration_wrappers) {
            this.configuration_wrappers[package_id].close_session(session_id);
        }
    }

    open_client(target_id, target_type, session_id, client_name, client_options) {
        let wrapper = null;
        if (target_type === "node") {
            wrapper = this.node_wrappers[target_id];
        } else if (target_type === "configuration") {
            wrapper = this.configuration_wrappers[target_id];
        }
        if (wrapper) {
            wrapper.open_client(session_id, client_name, client_options);
        }
    }

    recv_message(target_id, target_type, session_id, client_name, ...msg) {
        let wrapper = null;
        if (target_type === "node") {
            wrapper = this.node_wrappers[target_id];
        } else if (target_type === "configuration") {
            wrapper = this.configuration_wrappers[target_id];
        }

        if (wrapper) {
            wrapper.recv_message(session_id, client_name, ...msg);
        }
    }

    close_client(target_id, target_type, session_id, client_name) {
        let wrapper = null;
        if (target_type === "node") {
            wrapper = this.node_wrappers[target_id];
        } else if (target_type === "configuration") {
            wrapper = this.configuration_wrappers[target_id];
        }
        if (wrapper) {
            wrapper.close_client(session_id, client_name);
        }
    }

    close() {
    }
}

/* hyrrokkin_engine_utils/expr_checker.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ExpressionChecker = class {

    constructor() {
        this.unary_operator_typemaps = {};
        this.binary_operator_typemaps = {};
        this.function_typemaps = {};
        this.literal_typemapper = null;
    }

    add_unary_operator_types(name,output_type,input_type) {
        if (!(name in this.unary_operator_typemaps)) {
            this.unary_operator_typemaps[name] = [];
        }
        this.unary_operator_typemaps[name].push([output_type,input_type]);
    }

    add_binary_operator_types(name,output_type, input_type1, input_type2) {
        if (!(name in this.binary_operator_typemaps)) {
            this.binary_operator_typemaps[name] = [];
        }
        this.binary_operator_typemaps[name].push([output_type,input_type1,input_type2]);
    }

    add_function_types(name,output_type,...input_types) {
        if (!(name in this.function_typemaps)) {
            this.function_typemaps[name] = [];
        }
        this.function_typemaps[name].push([output_type].concat(input_types));
    }

    add_literal_typemapper(mapper_fn) {
        this.literal_typemapper = mapper_fn;
    }

    typematch(candidate_types, typemap_types) {
        if (candidate_types.length !== typemap_types.length) {
            return false;
        }
        for(let idx=0; idx<candidate_types.length; idx++) {
            if (candidate_types[idx] !== typemap_types[idx]) {
                if (typemap_types[idx] !== "*") {
                    return false;
                }
            }
        }
        return true;
    }

    check_expression(parsed_expression, name_typemap) {
        if (parsed_expression.name) {
            if (!(parsed_expression.name in name_typemap)) {
                return {"error_type":"invalid_name", "name":parsed_expression.name, "context": parsed_expression};
            } else {
                parsed_expression.type = name_typemap[parsed_expression.name];
                return null;
            }
        }

        if (parsed_expression.literal) {
            let typename = this.literal_typemapper(parsed_expression.literal);
            if (!typename) {
                return {"error_type":"literal_type_error", "literal":parsed_expression.literal, "context": parsed_expression};
            } else {
                parsed_expression.type = typename;
                 return null;
            }
        }

        if (parsed_expression.operator || parsed_expression.function) {
            for(let idx=0; idx<parsed_expression.args.length; idx++) {
                let error = this.check_expression(parsed_expression.args[idx], name_typemap);
                if (error !== null) {
                    return error;
                }
            }

            let types = [];
            parsed_expression.args.forEach(arg => {
                types.push(arg.type);
            });
            let typemap = null;

            if (parsed_expression.operator) {
                if (parsed_expression.args.length === 1) {
                    typemap = this.unary_operator_typemaps[parsed_expression.operator];
                } else {
                    typemap = this.binary_operator_typemaps[parsed_expression.operator];
                }
            } else {
                typemap = this.function_typemaps[parsed_expression.function];
            }

            if (typemap === undefined) {
                // operator or function name lookup failed
                if (parsed_expression.operator) {
                    return {
                        "error_type": "operator_type_missing",
                        "operator": parsed_expression.operator,
                        "context": parsed_expression
                    };
                } else {
                    return {
                        "error_type": "function_type_missing",
                        "function": parsed_expression.function,
                        "context": parsed_expression
                    };
                }
            }
            for(let idx=0; idx<typemap.length; idx++) {
                if (this.typematch(types,typemap[idx].slice(1))) {
                    parsed_expression.type = typemap[idx][0];
                    return null;
                }
            }
            // no type match
            if (parsed_expression.operator) {
                    return {
                        "error_type": "operator_type_error",
                        "operator": parsed_expression.operator,
                        "types": types,
                        "context": parsed_expression
                    };
            } else {
                return {
                    "error_type": "function_type_error",
                    "function": parsed_expression.function,
                    "types": types,
                    "context": parsed_expression
                };
            }
        }
    }
}

/* hyrrokkin_engine_utils/expr_parser.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ExpressionParser = class {

    constructor() {
        this.input = undefined;
        this.unary_operators = {};
        this.binary_operators = {};
        this.reset();
    }

    reset() {
        // lexer state
        this.index = 0;
        this.tokens = [];
        this.current_token_type = undefined; // s_string, d_string, string, name, operator, number, open_parenthesis, close_parenthesis, comma
        this.current_token_start = 0;
        this.current_token = undefined;
    }

    add_unary_operator(name) {
        this.unary_operators[name] = true;
    }

    add_binary_operator(name,precedence) {
        this.binary_operators[name] = precedence;
    }

    is_alphanum(c) {
        return (this.is_alpha(c) || (c >= "0" && c <= "9"));
    }

    is_alpha(c) {
        return ((c >= "a" && c <= "z") || (c >= "A" && c <= "Z"));
    }

    flush_token() {
        if (this.current_token_type !== undefined) {
            if (this.current_token_type === "name") {
                // convert to name => operator if the name matches known operators
                if (this.current_token in this.binary_operators || this.current_token in this.unary_operators) {
                    this.current_token_type = "operator";
                }
            }
            this.tokens.push([this.current_token_type, this.current_token, this.current_token_start]);
        }
        this.current_token = "";
        this.current_token_type = undefined;
        this.current_token_start = undefined;
    }

    read_whitespace(c) {
        switch(this.current_token_type) {
            case "s_string":
            case "d_string":
                this.current_token += c;
                break;
            case "name":
            case "operator":
            case "number":
                this.flush_token();
                break;
        }
    }

    read_doublequote() {
        switch(this.current_token_type) {
            case "d_string":
                this.flush_token();
                break;
            case "s_string":
                this.current_token += '"';
                break;
            default:
                this.flush_token();
                this.current_token_type = "d_string";
                this.current_token_start = this.index;
                break;
        }
    }

    read_singlequote() {
        switch(this.current_token_type) {
            case "s_string":
                this.flush_token();
                break;
            case "d_string":
                this.current_token += "'";
                break;
            default:
                this.flush_token();
                this.current_token_type = "s_string";
                this.current_token_start = this.index;
                break;
        }
    }

    read_digit(c) {
        switch(this.current_token_type) {
            case "operator":
                this.flush_token();
            case undefined:
                this.current_token_type = "number";
                this.current_token_start = this.index;
                this.current_token = c;
                break;
            case "d_string":
            case "s_string":
            case "name":
            case "number":
                this.current_token += c;
                break;
        }
    }

    read_e(c) {
        switch(this.current_token_type) {
            case "number":
                // detect exponential notation E or e
                this.current_token += c;
                // special case, handle negative exponent eg 123e-10
                if (this.input[this.index+1] === "-") {
                    this.current_token += "-";
                    this.index += 1;
                }
                break;

            default:
                this.read_default(c);
                break;
        }
    }

    read_parenthesis(c) {
        switch(this.current_token_type) {
            case "s_string":
            case "d_string":
                this.current_token += c;
                break;
            default:
                this.flush_token();
                this.tokens.push([(c === "(") ? "open_parenthesis" : "close_parenthesis",c, this.index]);
                break;
        }
    }

    read_comma(c) {
        switch(this.current_token_type) {
            case "d_string":
            case "s_string":
                this.current_token += c;
                break;
            default:
                this.flush_token();
                this.tokens.push(["comma",c, this.index]);
                break;
        }
    }

    read_default(c) {
        switch(this.current_token_type) {
            case "d_string":
            case "s_string":
                this.current_token += c;
                break;
            case "name":
                if (this.is_alphanum(c) || c === "_" || c === ".") {
                    this.current_token += c;
                } else {
                    this.flush_token();
                    this.current_token_type = "operator";
                    this.current_token_start = this.index;
                    this.current_token = c;
                }
                break;
            case "number":
                this.flush_token();
                // todo handle exponential notation eg 1.23e10
                if (this.is_alphanum(c)) {
                    throw {"error":"invalid_number","error_pos":this.index,"error_content":c};
                } else {
                    this.flush_token();
                    this.current_token_type = "operator";
                    this.current_token_start = this.index;
                    this.current_token = c;
                }
                break;
            case "operator":
                if (this.is_alphanum(c)) {
                    this.flush_token();
                    this.current_token_type = "name";
                    this.current_token_start = this.index;
                    this.current_token = c;
                } else {
                    if (this.current_token in this.unary_operators || this.current_token in this.binary_operators) {
                        this.flush_token();
                        this.current_token_type = "operator";
                        this.current_token_start = this.index;
                    }
                    this.current_token += c;
                }
                break;
            case undefined:
                this.current_token = c;
                if (this.is_alpha(c)) {
                    this.current_token_type = "name";
                } else {
                    this.current_token_type = "operator";
                }
                this.current_token_start = this.index;
                break;
            default:
                throw {"error":"internal_error","error_pos":this.index};
        }
    }

    read_eos() {
        switch(this.current_token_type) {
            case "d_string":
            case "s_string":
                throw {"error":"unterminated_string","error_pos":this.input.length};
            default:
                this.flush_token();
        }
    }

    merge_string_tokens() {
        let merged_tokens = [];
        let buff = "";
        let buff_pos = -1;
        for(let idx=0; idx<this.tokens.length;idx++) {
            let t = this.tokens[idx];
            let ttype = t[0];
            let tcontent = t[1];
            let tstart = t[2];
            if (ttype === "s_string" || ttype === "d_string") {
                buff += tcontent;
                buff_pos = (buff_pos < 0) ? tstart : buff_pos;
            } else {
                if (buff_pos >= 0) {
                    merged_tokens.push(["string",buff,buff_pos]);
                    buff = "";
                    buff_pos = -1;
                }
                merged_tokens.push(t);
            }
        }
        if (buff_pos >= 0) {
            merged_tokens.push(["string", buff, buff_pos]);
        }
        this.tokens = merged_tokens;
    }

    lex() {
        this.reset();
        this.index = 0;
        while(this.index < this.input.length) {
            let c = this.input.charAt(this.index);
            switch(c) {
                case " ":
                case "\t":
                case "\n":
                    this.read_whitespace(c);
                    break;
                case "\"":
                    this.read_doublequote();
                    break;
                case "'":
                    this.read_singlequote();
                    break;
                case "(":
                case ")":
                    this.read_parenthesis(c);
                    break;
                case ",":
                    this.read_comma(c);
                    break;
                case "0":
                case "1":
                case "2":
                case "3":
                case "4":
                case "5":
                case "6":
                case "7":
                case "8":
                case "9":
                case ".":
                    this.read_digit(c);
                    break;
                case "e":
                case "E":
                    this.read_e(c);
                    break;
                default:
                    this.read_default(c);
                    break;
            }
            this.index += 1;
        }
        this.read_eos();
        this.merge_string_tokens();
        return this.tokens;
    }

    get_ascending_precedence() {
        let prec_list = [];
        for(let op in this.binary_operators) {
            prec_list.push(this.binary_operators[op]);
        }

        prec_list = [...new Set(prec_list)];

        prec_list = prec_list.sort();

        return prec_list;
    }

    parse(s) {
        this.input = s;
        try {
            this.lex();
            this.token_index = 0;
            let parsed = this.parse_expr();
            this.strip_debug(parsed);
            return parsed;
        } catch(ex) {
            return ex;
        }
    }

    get_parser_context() {
        return {
            "type": this.tokens[this.token_index][0],
            "content": this.tokens[this.token_index][1],
            "pos": this.tokens[this.token_index][2],
            "next_type": (this.token_index < this.tokens.length - 1) ? this.tokens[this.token_index+1][0] : null,
            "last_type": (this.token_index > 0) ? this.tokens[this.token_index-1][0] : null
        }
    }

    parse_function_call(name) {
        let ctx = this.get_parser_context();
        let result = {
            "function": name,
            "args": [],
            "pos": ctx.pos
        }
        // skip over function name and open parenthesis
        this.token_index += 2;

        // special case - no arguments
        ctx = this.get_parser_context();
        if (ctx.type === "close_parenthesis") {
            return result;
        }

        while(this.token_index < this.tokens.length) {
            ctx = this.get_parser_context();
            if (ctx.last_type === "close_parenthesis") {
                return result;
            } else {
                if (ctx.type === "comma") {
                    throw {"error": "comma_unexpected", "error_pos": ctx.pos};
                }
                // read an expression and a following comma or close parenthesis
                result.args.push(this.parse_expr());
            }
        }
        return result;
    }

    parse_expr() {
        let args = [];
        while(this.token_index < this.tokens.length) {
            let ctx = this.get_parser_context();
            switch(ctx.type) {
                case "name":
                    if (ctx.next_type === "open_parenthesis") {
                        args.push(this.parse_function_call(ctx.content));
                    } else {
                        this.token_index += 1;
                        args.push({"name":ctx.content,"pos":ctx.pos});
                    }
                    break;
                case "string":
                    args.push({"literal":ctx.content,"pos":ctx.pos});
                    this.token_index += 1;
                    break;
                case "number":
                    args.push({"literal":Number.parseFloat(ctx.content),"pos":ctx.pos});
                    this.token_index += 1;
                    break;
                case "open_parenthesis":
                    this.token_index += 1;
                    args.push(this.parse_expr());
                    break;
                case "close_parenthesis":
                case "comma":
                    this.token_index += 1;
                    return this.refine_expr(args,this.token_index-1);
                case "operator":
                    args.push({"operator":ctx.content,"pos":ctx.pos});
                    this.token_index += 1;
                    break;
            }
        }
        return this.refine_expr(args,this.token_index);
    }

    refine_binary(args) {
        let precedences = this.get_ascending_precedence();
        for(let precedence_idx=0; precedence_idx < precedences.length; precedence_idx++) {
            let precedence = precedences[precedence_idx];
            for(let idx=args.length-2; idx>=0; idx-=2) {
                let subexpr = args[idx];
                if (subexpr.operator && this.binary_operators[subexpr.operator] === precedence) {
                    let lhs = args.slice(0,idx);
                    let rhs = args.slice(idx+1,args.length);
                    return {"operator":subexpr.operator,"pos":subexpr.pos,"args":[this.refine_binary(lhs),this.refine_binary(rhs)]};
                }
            }
        }
        return args[0];
    }

    refine_expr(args,end_pos) {
        if (args.length === 0) {
            throw {"error": "expression_expected", "pos": end_pos};
        }
        // first deal with unary operators
        for(let i=args.length-1; i>=0; i--) {
            // unary operators
            let arg = args[i];
            let prev_arg = (i>0) ? args[i-1] : undefined;
            let next_arg = (i<args.length-1) ? args[i+1] : undefined;
            if (arg.operator && (arg.operator in this.unary_operators)) {
                if (prev_arg === undefined || prev_arg.operator) {
                    if (next_arg !== undefined) {
                        // special case, convert unary - followed by a number literal to a negative number literal
                        if (arg.operator === "-" && typeof next_arg.literal === "number") {
                            args = args.slice(0, i).concat([{
                                "literal": -1*next_arg.literal,
                                "pos": arg.pos
                            }]).concat(args.slice(i + 2, args.length));
                        } else {
                            args = args.slice(0, i).concat([{
                                "operator": arg.operator,
                                "pos": arg.pos,
                                "args": [next_arg]
                            }]).concat(args.slice(i + 2, args.length));
                        }
                    }
                }
            }
        }

        // check that args are correctly formed, with operators in every second location, ie "e op e op e" and all operators
        // are binary operators with no arguments already assigned
        for(let i=0; i<args.length; i+=1) {
            let arg = args[i];
            if (i % 2 === 1) {
                if (!arg.operator || "args" in arg) {
                    throw {"error": "operator_expected", "error_pos": arg.pos };
                } else {
                    if (!(arg.operator in this.binary_operators)) {
                        throw {"error": "binary_operator_expected", "error_pos": arg.pos};
                    }
                }
            }
            if (i % 2 === 0 || i === args.length-1) {
                if (arg.operator && !("args" in arg)) {
                    throw {"error": "operator_unexpected", "error_pos": arg.pos};
                }
            }
        }

        return this.refine_binary(args);
    }

    strip_debug(expr) {
        if ("pos" in expr) {
            delete expr.pos;
        }
        if ("args" in expr) {
            expr.args.forEach(e => this.strip_debug(e));
        }
    }

}


/* hyrrokkin_engine/node_interface.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

/**
 * An interface describing methods that nodes should implement
 *
 * @type {hyrrokkin_engine.NodeInterface}
 */
hyrrokkin_engine.NodeInterface = class {

    /**
     * Construct an instance of this node
     *
     * @param {hyrrokkin_engine.NodeServiceInterface} services a service object supplying useful functionality to the node
     */
    constructor(services) {
    }

    /**
     * Implement this to load any resources needed.  Called immediately after construction.
     *
     * @return {Promise<void>}
     */
    async load() {
    }

    /**
     * Implement this to be notified when a call to the run method is pending.
     */
    reset_run() {
    }

    /**
     * Called to run the node, reading inputs and returning outputs
     *
     * @param {object} inputs an object containing input values where the key is an input port name and the value is an array of values presented by nodes connected to the port
     *
     * @return {Promise<object>} an object containing output values where the key is an output port name
     */
    async run(inputs) {
    }

    /**
     * Called when a client is opened
     *
     * @param {string} session_id the session id in which the client is opened
     * @param {string} client_name the name of the client that has been opened
     * @param (object} client_options
     * @param {hyrrokkin_engine.ClientServiceInterface} client_service an instance providing methods to send and receive messages
     */
    open_client(session_id, client_name, client_options, client_service) {
    }

    /**
     * Called when a client is closed
     *
     * @param {string} session_id the session id in which the client was opened
     * @param {string} client_name the name of the client that has been opened
     */
    close_client(sesion_id, client_name) {
    }

    /**
     * Called when the node is removed
     */
    close() {
    }
}


/* hyrrokkin_engine/configuration_interface.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

/**
 * Defines an interface that package configuration classes should implement
 *
 * @type {hyrrokkin_engine.ConfigurationInterface}
 */
hyrrokkin_engine.ConfigurationInterface = class {

    /**
     * The configuration constructor is passed a configuration service instance
     *
     * @param {hyrrokkin_engine.ConfigurationServiceInterface} configuration_service
     */
    constructor(configuration_service) {
    }

    /**
     * Called after construction.  Load any resources associated with this Configuration
     *
     * @return {Promise<void>}
     */
    async load() {
    }

    /**
     * Called when a session is opened
     *
     * @param session_id {string} identify the session being opened
     */
    open_session(session_id) {
    }

    /**
     * Called when a session is closed
     *
     * @param session_id {string} identify the session being closed
     */
    close_session(session_id) {
    }

    /**
     * Decode binary data into a value valid for a particular link type
     *
     * @param encoded_bytes {ArrayBuffer} binary data to decode
     * @param link_type {string} the link type associated with the value
     *
     * @return {*}
     */
    decode(encoded_bytes, link_type) {
    }

    /**
     * Encode a value associated with a link type to binary data
     *
     * @param value {*} the value to encode
     * @param link_type {string} the link type associated with the value
     *
     * @return {ArrayBuffer}
     */
    encode(value, link_type) {
    }

    /**
     * Called when a client is opened
     *
     * @param {string} session_id the session id in which the client is opened
     * @param {string} client_name the name of the client that has been opened
     * @param (object} client_options
     * @param {hyrrokkin_engine.ClientServiceInterface} client_service an instance providing methods to send and receive messages
     */
    open_client(session_id, client_name, client_options, client_service) {
    }

    /**
     * Called when a client is closed
     *
     * @param {string} session_id the session id in which the client was opened
     * @param {string} client_name the name of the client to be closed
     */
    close_client(session_id, client_name) {
    }

}


/* hyrrokkin_engine/inmemory_data_store_utils.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.InMemoryDataStoreUtils = class  {

    constructor(target_id, target_type) {
        this.target_id = target_id;
        this.target_type = target_type;
        this.properties = {};
        this.data = {};
    }

    static check_valid_data_key(key) {
        if (!key.match(/^[0-9a-zA-Z_]+$/)) {
            throw new Error("data key can only contain alphanumeric characters and underscores");
        }
    }

    static check_valid_data_value(data) {
        if (data instanceof ArrayBuffer) {
            return;
        } else if (data === null) {
            return;
        }
        throw new Error("data value can only be null or ArrayBuffer")
    }

    async load_properties() {
        return this.properties;
    }

    get_properties() {
        return this.properties;
    }

    async save_properties() {
    }

    get_property(name, default_value) {
        if (name in this.properties) {
            return this.properties[name];
        } else {
            return default_value;
        }
    }

    set_property(name, value) {
        this.properties[name] = value;
    }

    async get_data(key) {
        hyrrokkin_engine.InMemoryDataStoreUtils.check_valid_data_key(key);
        if (key in this.data) {
            return this.data;
        }
        return null;
    }

    async set_data(key, data) {
        hyrrokkin_engine.InMemoryDataStoreUtils.check_valid_data_key(key);
        hyrrokkin_engine.InMemoryDataStoreUtils.check_valid_data_value(data);
        this.data[key] = data;
    }
}

/* hyrrokkin_engine_drivers/execution_worker.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ExecutionWorker = class {

    constructor(send_fn) {
        this.graph_executor = null;
        this.packages = {};
        this.message_queue = [];
        this.handling = false;
        this.client_services = {};
        this.send_fn = send_fn;
        this.injected_inputs = {};
        this.output_listeners = {};
        this.read_only = false;
    }

    async init(o) {

        this.read_only = o["read_only"];
        let workspace_id = o["workspace_id"]; // set only when running in-client
        let topology_id = o["topology_id"];   // set only when running in-client
        let execution_limit = o["execution_limit"];
        let execution_folder = o["execution_folder"]; // set when running in server

        let data_store_utils_factory = null;
        if (execution_folder) {
            data_store_utils_factory = (target_id, target_type) => new hyrrokkin_engine.DenoDataStoreUtils(execution_folder, target_id, target_type, this.read_only);
        } else {
            if (topology_id) {
                data_store_utils_factory = (target_id, target_type) => new hyrrokkin_engine.ClientDataStoreUtils(workspace_id, topology_id, target_id, target_type, this.read_only);
            } else {
                data_store_utils_factory = (target_id, target_type) => new hyrrokkin_engine.InMemoryDataStoreUtils(target_id, target_type);
            }
        }

        this.graph_executor = new hyrrokkin_engine.GraphExecutor(data_store_utils_factory, execution_limit,
            () => {
                this.send({"action":"execution_complete", "count_failed":this.graph_executor.count_failed()});
            },
            (node_id,execution_state,is_manual) => {
                this.send({"action":"update_execution_state","node_id":node_id, "execution_state":execution_state, "is_manual": is_manual});
            },
            (node_id, level, msg) => {
                this.send({"action":"update_status", "status":level, "message":msg, "origin_type":"node", "origin_id":node_id});
            },
            (package_id,level,msg) => {
                this.send({"action":"update_status", "status":level, "message":msg, "origin_type":"configuration", "origin_id":package_id});
            },
            (origin_id, origin_type, session_id, client_name, ...msg) => {
                this.send({"action":"client_message", "origin_id":origin_id, "origin_type":origin_type, "session_id":session_id, "client_name":client_name}, ...msg);
            },
            (node_id, output_port_name, encoded_bytes) => {
                this.send({"action":"output_notification", "node_id":node_id, "output_port_name":output_port_name},encoded_bytes);
            },
            (origin_id, origin_type, session_id, client_name) => {
                this.send({"action":"request_open_client", "origin_id":origin_id, "origin_type":origin_type, "session_id":session_id, "client_name":client_name});
            });

        if (o["paused"]) {
            this.graph_executor.pause();
        }
    }

    async add_package(o) {
        let package_id = o["package_id"];
        let schema = o["schema"];
        let base_url = o["folder"];
        let services = null;
        let instance = null;
        if (hyrrokkin_engine.registry.defines_configuration(package_id)) {
            services = this.graph_executor.create_configuration_service(package_id, base_url);
            instance = hyrrokkin_engine.registry.create_configuration(package_id, services);
        }
        await this.graph_executor.add_package(package_id, schema, base_url, instance, services);
    }

    async add_node(o) {
        let node_id = o["node_id"];
        let node_type_id = o["node_type_id"];
        let package_id = node_type_id.split(":")[0];
        let service = this.graph_executor.create_node_service(node_id, package_id);
        let instance = hyrrokkin_engine.registry.create_node(node_type_id, service);
        await this.graph_executor.add_node(node_id,node_type_id,instance,service);
    }

    async load_target(o, properties, ...datalist) {
        let target_id = o["target_id"];
        let target_type = o["target_type"];
        let datakeys = o["datakeys"];
        let data = {};
        for(let idx=0; idx<datakeys.length; idx++) {
            data[datakeys[idx]] = datalist[idx];
        }
        await this.graph_executor.load_target(target_id, target_type, properties, data);
    }

    async remove_node(o) {
        await this.graph_executor.remove_node(o["node_id"]);
    }

    inject_input(o, encoded_bytes) {
        this.graph_executor.inject_input(o["node_id"], o["input_port_name"], encoded_bytes);
    }

    add_output_listener(o) {
        this.graph_executor.add_output_listener(o["node_id"], o["output_port_name"]);
    }

    remove_output_listener(o) {
        this.graph_executor.remove_output_listener(o["node_id"], o["output_port_name"]);
    }

    async add_link(o) {
        await this.graph_executor.add_link(o["link_id"], o["from_node_id"], o["from_port"], o["to_node_id"],o["to_port"]);
    }

    async remove_link(o) {
        await this.graph_executor.remove_link(o["link_id"]);
    }

    async clear(o) {
        await this.graph_executor.clear();
    }

    open_session(o) {
        let session_id = o["session_id"];
        this.graph_executor.open_session(session_id);
    }

    close_session(o) {
        let session_id = o["session_id"];
        this.graph_executor.close_session(session_id);
    }

    open_client(o) {
        let target_id = o["target_id"];
        let target_type = o["target_type"];
        let client_name = o["client_name"];
        let session_id = o["session_id"];
        let client_options = o["client_options"];
        this.graph_executor.open_client(target_id, target_type, session_id, client_name, client_options);
    }

    client_message(o,...msg) {
        let target_id = o["target_id"];
        let target_type = o["target_type"];
        let client_name = o["client_name"];
        let session_id = o["session_id"];
        this.graph_executor.recv_message(target_id, target_type, session_id, client_name, ...msg);
    }

    close_client(o) {
        let target_id = o["target_id"];
        let target_type = o["target_type"];
        let client_name = o["client_name"];
        let session_id = o["session_id"];
        this.graph_executor.close_client(target_id, target_type, session_id, client_name);
    }

    pause(o) {
        this.graph_executor.pause();
    }

    resume(o) {
        this.graph_executor.resume();
    }

    async close() {
        await this.graph_executor.close();
    }

    async recv(msg) {
        if (this.handling) {
            this.message_queue.push(msg);
        } else {
            this.handling = true;
            try {
                await this.handle(msg);
            } finally {
                while(true) {
                    let msg = this.message_queue.shift();
                    if (msg) {
                        try {
                            await this.handle(msg);
                        } catch(ex) {
                        }
                    } else {
                        break;
                    }
                }
                this.handling = false;
            }
        }
    }

    async handle(msg) {
        let o = msg[0];
        switch(o.action) {
            case "init":
                await this.init(o);
                this.send({"action":"init_complete"});
                break;
            case "add_package":
                await this.add_package(o);
                break;
            case "add_node":
                await this.add_node(o);
                break;
            case "remove_node":
                await this.remove_node(o);
                break;
            case "inject_input":
                this.inject_input(o, msg[1]);
                break;
            case "add_output_listener":
                this.add_output_listener(o);
                break;
            case "remove_output_listener":
                this.remove_output_listener(o);
                break;
            case "add_link":
                await this.add_link(o);
                break;
            case "load_target":
                await this.load_target(o,...msg.slice(1));
                break;
            case "remove_link":
                await this.remove_link(o);
                break;
            case "open_session":
                this.open_session(o);
                break;
            case "close_session":
                this.close_session(o);
                break;
            case "open_client":
                this.open_client(o);
                break;
            case "client_message":
                this.client_message(o, ...msg.slice(1));
                break;
            case "client_event":
                this.client_event(o);
                break;
            case "close_client":
                this.close_client(o);
                break;
            case "pause":
                this.pause(o);
                break;
            case "resume":
                this.resume(o);
                break;
            case "clear":
                await this.clear(o);
                break;
            case "close":
                await this.close();
                return false;
        }
        return true;
    }

    send(control_packet,...extra) {
        let message_parts = [control_packet];
        extra.forEach(o => {
            message_parts.push(o);
        })
        this.send_fn(message_parts);
    }
}


/* hyrrokkin_engine/registry.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.Registry = class {

    constructor() {
        this.configuration_factories = {};
        this.node_factories = {};
    }

    register_configuration_factory(package_id, configuration_factory) {
        this.configuration_factories[package_id] = configuration_factory;
    }

    register_node_factory = function(node_type_id,node_factory) {
        this.node_factories[node_type_id] = node_factory;
    }

    defines_configuration(package_id) {
        return (package_id in this.configuration_factories);
    }

    create_configuration(package_id, configuration_services) {
        return this.configuration_factories[package_id](configuration_services);
    }

    create_node(node_type_id, node_services) {
        return this.node_factories[node_type_id](node_services);
    }
}

hyrrokkin_engine.registry = new hyrrokkin_engine.Registry();

/* hyrrokkin_engine_drivers/client/index_db.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.IndexDB = class {

    constructor(name) {
        this.name = "topology-"+name;
    }

    async init() {
        this.db = await this.open();
    }

    async open() {
        return await new Promise((resolve,reject) => {
            const request = indexedDB.open(this.name, 1);
            request.onsuccess = (evt) => {
                resolve(evt.target.result);
            }
            request.onerror = (evt) => {
                resolve(null);
            }
            request.onupgradeneeded = (evt) => {
                // Save the IDBDatabase interface
                let db = evt.target.result;
                db.createObjectStore("data", {});
            }
        });
    }


    async get(key) {
        return await new Promise((resolve,reject) => {
            const transaction = this.db.transaction(["data"], "readonly");
            const request = transaction.objectStore("data").get(key);
            request.onsuccess = (evt) => {
                resolve(evt.target.result);
            }
            request.onerror = (evt) => {
                resolve(undefined);
            }
        });
    }

    async put(key, value) {
        return await new Promise((resolve,reject) => {
            const transaction = this.db.transaction(["data"], "readwrite");
            const request = transaction.objectStore("data").put(value,key);
            request.onsuccess = (evt) => {
                resolve(true);
            }
            request.onerror = (evt) => {
                resolve(true);
            }
        });
    }

    async delete(key) {
        return await new Promise((resolve,reject) => {
            const transaction = this.db.transaction(["data"], "readwrite");
            const request = transaction.objectStore("data").delete(key);
            request.onsuccess = (evt) => {
                resolve(evt.target.result);
            }
            request.onerror = (evt) => {
                resolve(undefined);
            }
        });
    }

    async getAllKeys() {
        return await new Promise((resolve,reject) => {
            const transaction = this.db.transaction(["data"], "readonly");
            const request = transaction.objectStore("data").getAllKeys();
            request.onsuccess = (evt) => {
                resolve(evt.target.result);
            }
            request.onerror = (evt) => {
                resolve(undefined);
            }
        });
    }
}

hyrrokkin_engine.IndexDB.create = async function(name) {
    let db = new hyrrokkin_engine.IndexDB(name);
    await db.init();
    return db;
}

hyrrokkin_engine.IndexDB.remove = async function(name) {
    return await new Promise((resolve,reject) => {
        const request = indexedDB.deleteDatabase("topology-"+name);
        request.onsuccess = (evt) => {
            resolve(true);
        }
        request.onerror = (evt) => {
            resolve(false);
        }
    });
}

/* hyrrokkin_engine_drivers/client/client_storage.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ClientStorage = class {

    constructor(db_name) {
        this.db_name = db_name;
        this.db = null;
    }

    static check_valid_data_key(key) {
        if (!key.match(/^[0-9a-zA-Z_]+$/)) {
            throw new Error("data key can only contain alphanumeric characters and underscores");
        }
    }

    static check_valid_data_value(data) {
        if (data instanceof ArrayBuffer) {
            return;
        } else if (data === null) {
            return;
        }
        throw new Error("data value can only be null or ArrayBuffer")
    }

    async open() {
        this.db = await hyrrokkin_engine.IndexDB.create(this.db_name);
    }

    close() {
        this.db = null;
    }

    async get_item(key) {
        if (!this.db) {
            await this.open();
        }
        let result = await this.db.get(key);
        if (result === undefined) {
            result = null;
        }
        return result;
    }

    async set_item(key, value) {
        if (!this.db) {
            await this.open();
        }
        await this.db.put(key, value);
    }

    async remove_item(key) {
        if (!this.db) {
            await this.open();
        }
        await this.db.delete(key);
    }

    async remove() {
        this.close();
        await hyrrokkin_engine.IndexDB.remove(this.db_name);
    }

    async get_keys() {
        if (!this.db) {
            await this.open();
        }
        return await this.db.getAllKeys();
    }

    async clear() {
        // clear the database by removing and re-opening
        await this.remove();
        await this.open();
    }

    async copy_to(to_db_name) {
        await this.open();
        let other = await new hyrrokkin_engine.ClientStorage(to_db_name);
        await other.open();
        await other.clear();
        let keys = await this.get_keys();
        for(let idx in keys) {
            let key = keys[idx];
            let value = await this.get_item(key);
            await other.set_item(key, value);
        }
        other.close();
    }
}

/* hyrrokkin_engine_drivers/client/client_data_store_utils.js */

var hyrrokkin_engine = hyrrokkin_engine || {};

hyrrokkin_engine.ClientDataStoreUtils = class  {

    constructor(workspace_id, topology_id, target_id, target_type, read_only) {
        this.workspace_id = workspace_id;
        this.topology_id = topology_id;
        this.target_id = target_id;
        this.target_type = target_type;
        this.properties = {};
        this.data_cache = {};
        this.read_only = read_only;
    }

    get_workspace_path(path) {
        return "workspace."+this.workspace_id+"."+path;
    }

    get_topology_path(path) {
        return "workspace."+this.workspace_id+".topology."+path
    }

    async open_workspace() {
        let db = new hyrrokkin_engine.ClientStorage(this.get_workspace_path("__root__"));
        await db.open();
        return db;
    }

    async load_properties() {
        let db = new hyrrokkin_engine.ClientStorage(this.get_topology_path(this.topology_id));
        let path = this.target_type + "/" + this.target_id + "/properties.json";
        let properties = await db.get_item(path);
        this.properties = properties !== null ? JSON.parse(properties) : {};
        return this.properties;
    }

    get_properties() {
        return this.properties;
    }

    async save_properties() {
        if (!this.read_only) {
            let db = new hyrrokkin_engine.ClientStorage(this.get_topology_path(this.topology_id));
            let path = this.target_type + "/" + this.target_id + "/properties.json";
            await db.set_item(path, JSON.stringify(this.properties));
        }
    }

    get_property(name, default_value) {
        if (name in this.properties) {
            return this.properties[name];
        } else {
            return default_value;
        }
    }

    set_property(name, value) {
        this.properties[name] = value;
        this.save_properties().then(() => {});
    }

    async get_data(key) {
        hyrrokkin_engine.ClientStorage.check_valid_data_key(key);
        if (key in this.data_cache) {
            return this.data_cache[key];
        } else {
            let db = new hyrrokkin_engine.ClientStorage(this.get_topology_path(this.topology_id));
            let path = this.target_type + "/" + this.target_id + "/data/" + key;
            return await db.get_item(path);
        }
    }

    async set_data(key, data) {
        hyrrokkin_engine.ClientStorage.check_valid_data_key(key);
        hyrrokkin_engine.ClientStorage.check_valid_data_value(data);
        if (this.read_only) {
            this.data_cache[key] = data;
        } else {
            let db = new hyrrokkin_engine.ClientStorage(this.get_topology_path(this.topology_id));
            let path = this.target_type + "/" + this.target_id + "/data/" + key;
            if (data === null) {
                await db.remove_item(path);
            } else {
                await db.set_item(path, data);
            }
        }
    }
}

