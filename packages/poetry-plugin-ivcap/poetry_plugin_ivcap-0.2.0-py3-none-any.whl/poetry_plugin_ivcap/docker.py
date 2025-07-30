#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import os
import re
import sys
import tempfile
from typing import Dict, Optional
from pydantic import BaseModel, Field
import subprocess

from .util import command_exists, get_name

DOCKER_BUILD_TEMPLATE = """
docker buildx build
    -t #DOCKER_NAME#
    --platform linux/#ARCH#
    --build-arg VERSION=#VERSION#
    --build-arg BUILD_PLATFORM=linux/#ARCH#
    -f #PROJECT_DIR#/#DOCKERFILE#
    --load #PROJECT_DIR#
"""

DOCKER_RUN_TEMPLATE = """
	docker run -it
        -p #PORT#:#PORT#
		--platform=linux/#ARCH#
		--rm \
		#NAME#_#ARCH#:#TAG# --port #PORT#
"""

class DockerConfig(BaseModel):
    name: Optional[str] = Field(None)
    tag: Optional[str] = Field(None)
    arch: Optional[str] = Field(None)
    version: Optional[str] = Field(None)
    dockerfile: Optional[str] = Field("Dockerfile")
    project_dir: Optional[str] = Field(".")

    @property
    def docker_name(self) -> str:
        return f"{self.name}_{self.arch}:{self.tag}"

    def from_build_template(self, data: dict) -> str:
        pdata = data.get("tool", {}).get("poetry-plugin-ivcap", {})
        template = pdata.get("docker-build-template", DOCKER_BUILD_TEMPLATE).strip()
        t = template.strip()\
            .replace("#DOCKER_NAME#", self.docker_name)\
            .replace("#NAME#", self.name)\
            .replace("#TAG#", self.tag)\
            .replace("#ARCH#", self.arch)\
            .replace("#VERSION#", self.version)\
            .replace("#DOCKERFILE#", self.dockerfile)\
            .replace("#PROJECT_DIR#", self.project_dir)\
            .split()
        return t

    def from_run_template(self, data) -> str:
        pdata = data.get("tool", {}).get("poetry-plugin-ivcap", {})
        template = pdata.get("docker-run-template", DOCKER_RUN_TEMPLATE).strip()
        opts = pdata.get("docker-run-opts", {"port": 8080})
        t = template.strip()\
            .replace("#NAME#", self.name)\
            .replace("#TAG#", self.tag)\
            .replace("#ARCH#", self.arch)\
            .replace("#VERSION#", self.version)\
            .replace("#PROJECT_DIR#", self.project_dir)

        for key, value in opts.items():
            t = t.replace(f"#{key.upper()}#", str(value))

        return t.split()


def docker_build(data: dict, line, arch = None) -> None:
    check_docker_cmd(line)
    config = _docker_cfg(data, line, arch)
    build_cmd = config.from_build_template(data)
    line(f"<info>INFO: {' '.join(build_cmd)}</info>")
    process = subprocess.Popen(build_cmd, stdout=sys.stdout, stderr=sys.stderr)
    exit_code = process.wait()
    if exit_code != 0:
        line(f"<error>ERROR: Docker build failed with exit code {exit_code}</error>")
    else:
        line("<info>INFO: Docker build completed successfully</info>")
    return config.docker_name

def docker_run(data: dict, line) -> None:
    check_docker_cmd(line)
    config = _docker_cfg(data, line)
    build_run = config.from_run_template(data)
    line(f"<info>INFO: {' '.join(build_run)}</info>")
    process = subprocess.Popen(build_run, stdout=sys.stdout, stderr=sys.stderr)
    exit_code = process.wait()
    if exit_code != 0:
        line(f"<error>ERROR: Docker run failed with exit code {exit_code}</error>")
    else:
        line("<info>INFO: Docker run completed successfully</info>")

def _docker_cfg(data: dict, line, arch = None) -> DockerConfig:
    project_data = data.get("project", {})
    name = get_name(data)
    version = project_data.get("version", None)

    pdata = data.get("tool", {}).get("poetry-plugin-ivcap", {})
    config = DockerConfig(name=name, version=version, **pdata.get("docker", {}))
    if arch:
        # override architecture if provided
        config.arch = arch

    if not config.version:
        try:
            config.version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
        except Exception as e:
            line(f"<error>Error retrieving latest tag: {e}</error>")
            config.version = "???"

    if not config.tag:
        try:
            config.tag = subprocess.check_output(['git', 'rev-parse', "--short", 'HEAD']).decode().strip()
        except Exception as e:
            line(f"<warning>WARN: retrieving commit hash: {e}</warning>")
            config.tag = "latest"

    if not config.arch:
        try:
            config.arch = subprocess.check_output(['uname', '-m']).decode().strip()
        except Exception as e:
            line(f"<error>ERROR: cannot obtain build architecture: {e}</error>")
            os.exit(1)

    return config

def docker_push(docker_img, line):
    push_cmd = ["ivcap", "package", "push", "--force", "--local", docker_img]
    line(f"<debug>Running: {' '.join(push_cmd)} </debug>")
    p1 = subprocess.Popen(push_cmd, stdout=subprocess.PIPE, stderr=sys.stderr)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Pipe its output to tee (or to the screen via /dev/tty)
        p2 = subprocess.Popen(
            ["tee", tmp_path],
            stdin=p1.stdout,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        p1.stdout.close()
        # Wait for both to finish
        p2.communicate()
        exit_code = p1.wait()
        if exit_code != 0:
            line(f"<error>ERROR: package push failed with exit code {exit_code}</error>")
            sys.exit(1)

        # Lookginf for "45a06508-5c3a-4678-8e6d-e6399bf27538/gene_onology_term_mapper_amd64:9a9a7cc pushed\n"
        pattern = re.compile(
            r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/[^\s]+) pushed'
        )
        package_name = None
        with open(tmp_path, 'r') as f:
            for l in f:
                match = pattern.search(l)
                if match:
                    package_name = match.group(1)
                    break

        if not package_name:
            line("<error>ERROR: No package name found in output</error>")
            sys.exit(1)

        line("<info>INFO: package push completed successfully</info>")
        return package_name
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def check_docker_cmd(line):
    if not command_exists("docker"):
        line("<error>'docker' command not found. Please install it first.</error>")
        sys.exit(1)
