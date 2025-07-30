#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import os
from poetry.plugins.application_plugin import ApplicationPlugin
from cleo.commands.command import Command
from cleo.helpers import argument
import subprocess

from poetry_plugin_ivcap.util import get_version

from .ivcap import create_service_id, service_register, tool_register
from .docker import docker_build, docker_run
from .ivcap import docker_publish

class IvcapCommand(Command):
    name = "ivcap"
    description = "IVCAP plugin `poetry ivcap <subcommand>`"
    help = """\

IVCAP plugin

Supporting the development of services and tools for the IVCAP platform

Available subcommands:
    run                 Run the service locally
    docker-build        Build the docker image for this service
    docker-run          Run the service's docker image locally
    docker-publish      Publish the service's docker image to IVCAP
    service-register    Register the service with IVCAP
    create-service-id   Create a unique service ID for the service
    tool-register       Register the service as an AI Tool with IVCAP

Example:
  poetry ivcap run -- --port 8080

Configurable options in pyproject.toml:

  [tool.poetry-plugin-ivcap]
  service-file = "service.py"  # The Python file that implements the service
  service-file = "service.py"
  service-id = "urn:ivcap:service:ac158a1f-dfb4-5dac-bf2e-9bf15e0f2cc7" # A unique identifier for the service

  docker-build-template = "docker buildx build -t #DOCKER_NAME#  ."
  docker-run-template = "docker run -rm -p #PORT#:#PORT#"
"""
    arguments = [
        argument("subcommand", optional=True, description="Subcommand: run, deploy, etc."),
        argument("args", optional=True, multiple=True, description="Additional arguments for subcommand"),
    ]

    allow_extra_args = True
    ignore_validation_errors = True

    def handle(self):
        poetry = self.application.poetry
        data = poetry.pyproject.data

        sub = self.argument("subcommand")
        args = self.argument("args")

        if sub == "run":
            self.run_service(data, args, self.line)
        elif sub == "docker-build":
            docker_build(data, self.line)
        elif sub == "docker-run":
            docker_run(data, args, self.line)
        elif sub == "docker-publish":
            docker_publish(data, self.line)
        elif sub == "service-register":
            service_register(data, self.line)
        elif sub == "create-service-id":
            sid = create_service_id(data, self.line)
            print(sid)
        elif sub == "tool-register":
            tool_register(data, self.line)
        else:
            if not (sub == None or sub == "help"):
                self.line(f"<error>Unknown subcommand: {sub}</error>")
            print(self.help)

    def run_service(self, data, args, line):
        config = data.get("tool", {}).get("poetry-plugin-ivcap", {})

        service = config.get("service-file")
        if not service:
            self.line("<error>Missing 'service-file' in [tool.poetry-plugin-ivcap]</error>")
            return

        if not '--port' in args:
            port = config.get("port")
            if port:
                args.extend(["--port", str(port)])

        env = os.environ.copy()
        env["VERSION"] = get_version(data, None, line)

        cmd = ["poetry", "run", "python", service]
        cmd.extend(args)
        self.line(f"<info>Running: {' '.join(cmd)}</info>")
        subprocess.run(cmd, env=env)

class IvcapPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("ivcap", lambda: IvcapCommand())
