#
# Copyright (c) 2025 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#
import os
import re
import subprocess
import sys
import tempfile
import uuid
import humanize

from .docker import _docker_cfg, docker_build, docker_push
from .util import command_exists, execute_subprocess_and_capture_output, get_name, string_to_number

def docker_publish(data, line):
    check_ivcap_cmd(line)
    #dname = docker_build(data, line, arch="amd64")
    dname = "gene_onology_term_mapper_amd64:9a9a7cc"
    print(dname)

    size_cmd = ["docker", "inspect", "--format='{{.Size}}'", dname]
    line(f"<debug>Running: {' '.join(size_cmd)} </debug>")
    size = string_to_number(subprocess.check_output(size_cmd).decode())
    if size is None:
        line("<error>Failed to retrieve image size</error>")
        return
    line(f"<info>INFO: Image size {humanize.naturalsize(size)}</info>")
    pkg_name = docker_push(dname, line)

def service_register(data, line):
    check_ivcap_cmd(line)
    config = data.get("tool", {}).get("poetry-plugin-ivcap", {})

    service = config.get("service-file")
    if not service:
        line("<error>Missing 'service-file' in [tool.poetry-plugin-ivcap]</error>")
        return

    dcfg = _docker_cfg(data, line, "amd64")
    pkg_cmd = ["ivcap", "package", "list", dcfg.docker_name]
    line(f"<debug>Running: {' '.join(pkg_cmd)} </debug>")
    pkg = subprocess.check_output(pkg_cmd).decode()
    if not pkg or pkg == "":
        line(f"<error>No package '{dcfg.docker_name}' found. Please build and publish it first.</error>")
        return
    service_id = get_service_id(data, line)

    cmd = ["poetry", "run", "python", service, "--print-service-description"]
    line(f"<debug>Running: {' '.join(cmd)} </debug>")
    svc = subprocess.check_output(cmd).decode()

    svc = svc.replace("#DOCKER_IMG#", pkg.strip())\
            .replace("#SERVICE_ID#", service_id)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(svc)
        tmp_path = tmp.name  # Save the file name for subprocess

    try:
        policy = get_policy(data, line)
        up_cmd = ["ivcap", "aspect", "update", "--policy", policy, service_id, "-f", tmp_path]
        try:
            line(f"<debug>Running: {' '.join(up_cmd)} </debug>")
            jaid = subprocess.check_output(up_cmd).decode().strip()
            p = re.compile(r'.*(urn:[^"]*)')
            aid = p.search(jaid).group(1)
            line(f"<info>INFO: service definition successfully uploaded - {aid}</info>")
        except Exception as e:
            line(f"<error>ERROR: cannot upload service definitiion: {e}</error>")
            sys.exit(1)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def tool_register(data, line):
    check_ivcap_cmd(line)
    config = data.get("tool", {}).get("poetry-plugin-ivcap", {})

    service = config.get("service-file")
    if not service:
        line("<error>Missing 'service-file' in [tool.poetry-plugin-ivcap]</error>")
        return

    cmd = ["poetry", "run", "python", service, "--print-tool-description"]
    line(f"<debug>Running: {' '.join(cmd)} </debug>")
    svc = subprocess.check_output(cmd).decode()

    service_id = get_service_id(data, line)
    svc = svc.replace("#SERVICE_ID#", service_id)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        tmp.write(svc)
        tmp_path = tmp.name  # Save the file name for subprocess

    try:
        policy = get_policy(data, line)
        up_cmd = ["ivcap", "aspect", "update", "--policy", policy, service_id, "-f", tmp_path]
        try:
            line(f"<debug>Running: {' '.join(up_cmd)} </debug>")
            jaid = subprocess.check_output(up_cmd).decode().strip()
            p = re.compile(r'.*(urn:[^"]*)')
            aid = p.search(jaid).group(1)
            line(f"<info>INFO: tool description successfully uploaded - {aid}</info>")
        except Exception as e:
            line(f"<error>ERROR: cannot upload tool description: {e}</error>")
            sys.exit(1)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def get_service_id(data, line):
    service_id = data.get("tool", {}).get("poetry-plugin-ivcap", {}).get("service-id")
    if not service_id:
        service_id = create_service_id(data, line)
    return service_id

def create_service_id(data, line):
    check_ivcap_cmd(line)
    name = get_name(data)
    account_id = get_account_id(data, line)
    id = uuid.uuid5(uuid.NAMESPACE_DNS, f"{name}{account_id}")
    return f"urn:ivcap:service:{id}"

def get_policy(data, line):
    policy = data.get("tool", {}).get("poetry-plugin-ivcap", {}).get("policy")
    if not policy:
        policy = "urn:ivcap:policy:ivcap.open.metadata"
    return policy

def get_account_id(data, line):
    check_ivcap_cmd(line)
    cmd = ["ivcap", "context", "get", "account-id"]
    line(f"<debug>Running: {' '.join(cmd)} </debug>")
    try:
        account_id = subprocess.check_output(cmd).decode().strip()
        return account_id
    except subprocess.CalledProcessError as e:
        line(f"<error>Error retrieving account ID: {e}</error>")
        sys.exit(1)

def check_ivcap_cmd(line):
    if not command_exists("ivcap"):
        line("<error>'ivcap' command not found. Please install the IVCAP CLI tool.</error>")
        line("<error>... see https://github.com/ivcap-works/ivcap-cli?tab=readme-ov-file#install-released-binaries for instructions</error>")
        os.exit(1)
