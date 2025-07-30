#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
from poetry.plugins.application_plugin import ApplicationPlugin
from cleo.commands.command import Command
from cleo.helpers import argument
import subprocess

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
  poetry ivcap run

Configurable optiosn in pyproject.toml:

  [tool.poetry-plugin-ivcap]
  service-file = "service.py"  # The Python file that implements the service
  service-file = "service.py"
  service-id = "urn:ivcap:service:ac158a1f-dfb4-5dac-bf2e-9bf15e0f2cc7" # A unique identifier for the service

  docker-build-template = "docker buildx build -t #DOCKER_NAME#  ."
  docker-run-template = "docker run -rm -p #PORT#:#PORT#"
"""
    arguments = [
        argument("subcommand", optional=True, description="Subcommand: run, deploy, etc.")
    ]

    def handle(self):
        poetry = self.application.poetry
        data = poetry.pyproject.data

        sub = self.argument("subcommand")
        if sub == "run":
            self.run_service(data)
        elif sub == "docker-build":
            docker_build(data, self.line)
        elif sub == "docker-run":
            docker_run(data, self.line)
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

    def run_service(self, data):
        config = data.get("tool", {}).get("poetry-plugin-ivcap", {})

        service = config.get("service-file")
        port = config.get("port")

        if not service or not port:
            self.line("<error>Missing 'service-file' or 'port' in [tool.poetry-plugin-ivcap]</error>")
            return

        self.line(f"<info>Running: python {service} --port {port}</info>")
        subprocess.run(["poetry", "run", "python", service, "--port", str(port)])

class IvcapPlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("ivcap", lambda: IvcapCommand())
