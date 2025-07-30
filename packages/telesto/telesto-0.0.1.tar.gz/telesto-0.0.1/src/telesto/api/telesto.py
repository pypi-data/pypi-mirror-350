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
import logging
import sys
from importlib.resources import files

from narvi.api.server import NarviServer
from hyrrokkin.execution_manager.process_runner import ProcessRunner

class Telesto:

    def __init__(self, configuration):
        self.logger = logging.getLogger("telesto")
        self.host = configuration.get("host","localhost")
        self.port = configuration.get("port",8889)
        self.workspace_id = configuration["workspace_id"]
        self.workspace_name = configuration["workspace_name"]
        self.workspace_path = configuration["workspace_path"]

        self.workspace_description = configuration.get("workspace_description","")
        self.base_url = configuration.get("base_url","/telesto")
        self.applications = configuration.get("application", {})
        self.in_process = configuration.get("in_process", False)
        self.web_server_type = configuration.get("webserver", "tornado") # or "builtin"

        self.skadi_options = configuration.get("skadi_options", {})
        self.hyrrokkin_options = configuration.get("hyrrokkin_options", {})

        self.package_list = configuration.get("packages", [])
        self.package_folders = {}
        self.packages = {}

        for package_resource in self.package_list:
            package_folder = Telesto.get_path_of_resource(package_resource)
            print(package_resource, package_folder)
            schema_path = os.path.join(package_folder,"schema.json")
            # check package can be loaded
            package_id = None
            try:
                with open(schema_path) as f:
                    o = json.loads(f.read())
                    package_id = o["id"]
            except:
                self.logger.error(f"Unable to load package {package_resource} from {schema_path}")
                sys.exit(0)
            self.package_folders[package_id] = package_folder
            self.packages[package_id] = { "package": package_resource }

        self.designer_app_name = "topology_designer"
        self.directory_app_name = "topology_directory"

        self.launch_ui = configuration.get("launch_ui","")

        if self.web_server_type == "tornado":
            try:
                # check tornado is installed
                import tornado
            except:
                # if not, fallback to the builtin webserver
                self.logger.warning("tornado web-server not installed, falling back to builtin web-server")
                self.web_server_type = "builtin"

    @staticmethod
    def get_path_of_resource(package, resource=""):
        if resource:
            return str(files(package).joinpath(resource))
        else:
            return str(files(package))

    def get_resource_roots(self, from_roots={}):

        telesto_static_folder = Telesto.get_path_of_resource("telesto.static")
        narvi_static_folder = Telesto.get_path_of_resource("narvi.static")
        print(narvi_static_folder)
        apps_common_folder = Telesto.get_path_of_resource("telesto.apps.common")
        resource_roots = {}
        resource_roots[("static","**")] = telesto_static_folder
        resource_roots["**/skadi-page.js"] = os.path.join(telesto_static_folder,"skadi-page.js")
        resource_roots[("narvi", "narvi.js")] = narvi_static_folder
        resource_roots[("common", "topology_engine.js")] = apps_common_folder
        resource_roots[("common", "topology_store.js")] = apps_common_folder

        for package_id, package_folder in self.package_folders.items():
            resource_roots[(f"schema/{package_id}","**")] = package_folder
        resource_roots.update(**from_roots)
        return resource_roots

    def get_platform_extensions(self):

        # for (package_name,package) in schema.get_packages().items():
        #     self.schema_urls.append(package.get_id() + "/schema.json")
        #     metadata = package.get_metadata()
        #     package_id = package.get_id()
        #     link = metadata.get("link","")
        #     if link:
        #         link = self.base_url+"/app/"+package_id+"/"+link
        #     TopologyWebApp.package_metadata.append((metadata.get("name","?"),
        #                                              metadata.get("version","?"),
        #                                             metadata.get("description","?"),
        #                                             link))

        from hyrrokkin import __version__ as HYRROKKIN_VERSION
        from telesto import __version__ as TELESTO_VERSION
        metadata = [("Hyrrokkin", HYRROKKIN_VERSION, "Open Source License V3.0",
                 "https://github.com/vistual-topology/hyrrokkin"),
                ("Telesto", TELESTO_VERSION, "Open Source License V3.0",
                 "https://github.com/visual-topology/telesto")]

        platform_extensions = []
        for (name, version, license, url) in metadata:
            platform_extensions.append({"name": name, "version": version, "license_name": license, "url": url})
        return platform_extensions

    def run(self):
        self.logger.info("starting telesto")

        server = NarviServer(host=self.host, port=self.port, web_server_type=self.web_server_type,
                             base_path=self.base_url, admin_path="/status.json")

        package_urls = []
        for package_id in self.packages:
            package_urls.append(f"schema/{package_id}")

        applications = {}

        topology_workspace_path = os.path.join(self.workspace_path, "topologies")

        for app_name, app_config in self.applications.items():
            self.logger.info(f"registering application {app_name}")
            name = app_config.get("name")
            description = app_config.get("description", "")
            topology_id = app_config.get("topology_id", "")
            shared = app_config.get("shared", False)

            application_package = app_config.get("application_package")

            topology_path = os.path.join(topology_workspace_path, topology_id,"topology.json")
            if not os.path.exists(topology_path):
                self.logger.error(
                    f"Application {app_name} configuration error, no topology found in {topology_path}")
                sys.exit(-1)

            topology_runner = server.register_service(namespace=self.workspace_id, app_service_name="topology_runner",
                                                      app_cls_name="telesto.app_services.topology_runner.TopologyRunner",
                                                      app_parameters={
                                                          "packages": self.packages,
                                                          "workspace_path": topology_workspace_path,
                                                          "hyrrokkin_options": self.hyrrokkin_options
                                                      }, shared_service=shared, fixed_service_id=topology_id)

            application_resource_roots = self.get_resource_roots({
                "topology_application.js": Telesto.get_path_of_resource("telesto.apps","topology_application.js"),
                "**": Telesto.get_path_of_resource(application_package)
            })

            server.register_app(app_name=app_name,
                application_service=topology_runner,
                app_parameters={
                    "base_url": self.base_url,
                    "package_urls": package_urls,
                    "platform_extensions": self.get_platform_extensions(),
                    "workspace_id": self.workspace_id,
                    "topology_id": topology_id
                },
                resource_roots=application_resource_roots)

            applications[app_name] = {
                "name": name,
                "description": description,
                "url": f"{self.base_url}/{self.workspace_id}/{app_name}/index.html"
            }

        local_url = ""


        topology_runner=server.register_service(namespace=self.workspace_id,app_service_name="topology_runner",
                app_cls_name="telesto.app_services.topology_runner.TopologyRunner",
                app_parameters={
                   "packages": self.packages,
                   "workspace_path": topology_workspace_path,
                   "hyrrokkin_options": self.hyrrokkin_options
               }, shared_service=True)

        local_url = f"http://{self.host}:{self.port}{self.base_url}/{self.workspace_id}/topology_directory/index.html"

        designer_resource_roots = self.get_resource_roots({
            "index.html": Telesto.get_path_of_resource("telesto.apps","topology_designer.html"),
            "topology_designer.js": Telesto.get_path_of_resource("telesto.apps","topology_designer.js")
        })

        server.register_app(app_name=self.designer_app_name,
            application_service=topology_runner,
            app_parameters={
                "package_urls":package_urls,
                "topology": {},
                "read_only":False,
                "platform_extensions": self.get_platform_extensions(),
                "restartable": not self.in_process,
                "skadi_options": self.skadi_options
            },
            resource_roots=designer_resource_roots,
            service_chooser_app_name="topology_directory")

        directory_service = server.register_service(namespace=self.workspace_id,
            app_cls_name="telesto.app_services.topology_directory.TopologyDirectory",
            app_service_name="directory_service",
            app_parameters={
                "workspace_path": topology_workspace_path,
                "packages": self.packages,
                "applications": applications
            },
            fixed_service_id="topology_directory")

        directory_resource_roots = self.get_resource_roots({
            "index.html": Telesto.get_path_of_resource("telesto.apps","topology_directory.html"),
            "topology_directory.js": Telesto.get_path_of_resource("telesto.apps","topology_directory.js")
        })
        server.register_app(app_name=self.directory_app_name,
            application_service=directory_service,
            app_parameters={
                "designer_app_name": self.designer_app_name,
                "base_url": self.base_url,
                "package_urls": package_urls,
                "skadi_options": self.skadi_options
            },
            resource_roots=directory_resource_roots)

        # called when the web server is listening
        def open_callback():
            if self.launch_ui and local_url:
                cmd = self.launch_ui.replace("URL",local_url)
                pr = ProcessRunner(cmd.split(" "), exit_callback=lambda: server.close())
                pr.start()

        server.print_services()
        server.run(open_callback)
