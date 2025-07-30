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

import logging
import argparse
import tomllib

from telesto.api.telesto import Telesto

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--configuration_path", help="Specify the path to a configuration file", default="telesto.toml")

    # these options allow settings in the configuration file to be overridden
    parser.add_argument("--host", help="Specify the host name for serving files", default=None)
    parser.add_argument("--port", type=int, help="Specify the port number for serving files", default=None)
    parser.add_argument("--base_url", help="Specify the base url for the web server", default=None)
    parser.add_argument("--in_process", type=bool, help="Specify whether executions happen in the same process as the web services or in sub-processes", default=None)
    parser.add_argument("--webserver", help="Specify the webserver to use, either tornado or builtin", default=None)
    parser.add_argument("--launch_ui", help="a command to run to launch a web browser, if running a local app.  Include 'URL' in the string.", default=None)

    parser.add_argument("--workspace_id", help="Specify the workspace's id", default=None)
    parser.add_argument("--workspace_name", help="Specify the workspace's name", default=None)
    parser.add_argument("--workspace_description", help="Specify the workspace's description", default=None)
    parser.add_argument("--workspace_path", help="Specify the filesystem location where topologies in the workspace are stored", default=None)

    logging.basicConfig(level=logging.INFO)

    args = parser.parse_args()

    # read the configuration file
    with open(args.configuration_path) as f:
        config = tomllib.loads(f.read())

    # override from the command line
    for key in ["host","port","base_url","workspace_id", "in_process", "workspace_name", "workspace_description", "workspace_path"]:
        value = getattr(args,key)
        if value:
            config[key] = value

    if args.workspace_path:
        config["workspace-path"] = args.workspace_path

    app = Telesto(config)

    app.run()


if __name__ == '__main__':
    main()