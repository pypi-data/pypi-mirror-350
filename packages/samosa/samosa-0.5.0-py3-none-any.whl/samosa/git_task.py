#!/usr/bin/env python3
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
import os
import stat
import subprocess
import sys
from importlib import resources
from time import sleep

import pygit2
from pygit2 import Repository
from pygit2._pygit2 import GIT_BRANCH_LOCAL, GIT_BRANCH_REMOTE  # noqa
import sh


def shell(*args, limit=0):
    count = 0
    for line in sh.git(args, _iter=True):
        print(line.strip())
        count += 1
        if 0 < limit < count:
            return


def run_subprocess(*args):
    args = ["git"] + list(args)
    output = subprocess.check_output(args, universal_newlines=True)
    print(output)


def get_config_key(config, key):
    try:
        return list(config.get_multivar(key))[-1]
    except IndexError:
        return None


def get_remote_address(repo, key):
    try:
        return repo.remotes[key].url
    except KeyError:
        return None


def print_samosa_message(line1, line2):
    samosa1 = "* *"
    samosa2 = " * "

    diff = abs(len(line1) - len(line2))
    spacer = " " * diff

    if len(line1) < len(line2):
        line1 += spacer
    else:
        line2 += spacer

    print(f"\n{line1}  {samosa1}\n{line2}  {samosa2}\n", file=sys.stdout)


def valid_suffix(address):
    for suffix in [
        "example.com",
        "example.edu",
        "example.net",
        "example.org",
        ".example",
        ".invalid",
    ]:
        if address.endswith(suffix):
            return False

    return True


def debug_print_config(config):
    for entry in config:
        print(f"{entry.name}: {entry.value} ({entry.level})")


def debug_print_remotes(repo):
    for item in repo.remotes:
        print(item.name)


def get_root_from_path(path):
    return pygit2.discover_repository(path)


def initialise_repository(path):
    _existing = get_root_from_path(path)
    if _existing is not None:
        exit(f"There is already a repository at {_existing}")

    pygit2.init_repository(path)


def add_remote(root, remote_name, remote_url, perform_fetch=True):
    _ = Repository(root, flags=0)

    shell("remote", "add", remote_name, remote_url)

    if perform_fetch:
        shell("fetch", "--all")


def checkout_branch(root, name):
    repo: Repository = Repository(root, flags=0)

    if name == "main":
        shell("checkout", "--track", "upstream/main", "-B", "main")
    elif local_branch := repo.branches.get(name):
        repo.checkout(local_branch)
    else:
        shell("checkout", "--track", "upstream/main", "-b", name)


def fix_and_validate_root(root, quiet_if_valid=False):
    repo: Repository = Repository(root, flags=0)
    config = repo.config.snapshot()

    if os.getenv("DEBUG", default=False):
        debug_print_config(config)
        debug_print_remotes(repo)

    errors = []

    # USERNAME IS VALID

    username = get_config_key(config, "user.name")
    if username is None or username in ["example", "invalid"]:
        errors.append(
            'Fix invalid username with: git config --local user.name "Your Name"'
        )

    # EMAIL ADDRESS IS VALID

    email_address = get_config_key(config, "user.email")
    if email_address is None or not valid_suffix(email_address):
        errors.append(
            'Fix invalid email address with: git config --local user.email "address@mail.example"'
        )

    # ANY REMOTE EXISTS

    if len(repo.remotes) == 0:
        errors.append("No remotes defined!")

    # ORIGIN REMOTE (test occurs later)

    origin_address = get_remote_address(repo, "origin")
    if origin_address is None:
        errors.append(
            "Fix missing origin with: samosa add origin "
            "git@example.example:origin/example.git"
        )

    # UPSTREAM REMOTE EXISTS

    upstream_address = get_remote_address(repo, "upstream")
    if upstream_address is None:
        errors.append(
            "Fix missing upstream with: samosa add upstream "
            "git@example.example:upstream/example.git"
        )

    remote_push_default = get_config_key(config, "remote.pushdefault")
    if remote_push_default is None or remote_push_default != "origin":
        sh.git("config", "remote.pushdefault", "origin")
        remote_push_default = "origin"

    branch_push_default = get_config_key(config, "push.default")
    if branch_push_default is None or branch_push_default != "current":
        sh.git("config", "push.default", "current")
        branch_push_default = "current"

    # PRE-COMMIT HOOK EXISTS

    pre_commit_status = "Not set"
    pre_commit_path = os.path.join(root, "hooks/pre-commit")
    if not os.path.isfile(pre_commit_path):
        try:
            with resources.open_text("samosa.resource", "pre-commit") as source, open(
                pre_commit_path, "w"
            ) as target:
                for line in source:
                    target.write(line)

        except IOError:
            errors.append(
                "Pre-commit hook is missing and cannot be added. Please create .git/hooks/pre-commit"
            )

    # PRE-COMMIT HOOK IS EXECUTABLE

    if os.path.isfile(pre_commit_path):
        # set owner execution
        mode = os.stat(pre_commit_path).st_mode
        os.chmod(pre_commit_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        # confirm owner execution
        if os.stat(pre_commit_path).st_mode & stat.S_IXUSR:
            pre_commit_status = "Set"
        else:
            errors.append(
                "Fix missing executable bit with: chmod u+x .git/hooks/pre-commit"
            )

    # LOCAL MAIN BRANCH EXISTS

    local_main_branch = repo.lookup_branch("main", GIT_BRANCH_LOCAL)
    if local_main_branch is None:
        local_main_name = "missing"
        errors.append("No local branch named main!")
    else:
        local_main_name = "main"

    # UPSTREAM MAIN BRANCH EXISTS

    upstream_main_branch = repo.lookup_branch("upstream/main", GIT_BRANCH_REMOTE)
    if upstream_main_branch is None:
        errors.append("No upstream branch named main!")

    # set upstream of `local/main` TO `upstream/main`
    if local_main_branch and upstream_main_branch:
        local_main_branch.upstream = upstream_main_branch

    # CONFIRM UPSTREAM OF `local/main` is `upstream/main`

    if local_main_branch and local_main_branch.upstream:
        local_main_upstream = local_main_branch.upstream.raw_branch_name.decode()
        if local_main_upstream != "upstream/main":
            errors.append(
                "Fix upstream target with: git branch main --set-upstream-to=upstream/main"
            )
    else:
        local_main_upstream = "missing"  # No additional errors required

    # FINAL CHECK FOR PRE-COMMIT

    if pre_commit_status == "Not set":
        errors.append("Pre-commit hook still not set!")

    # IF VALID AND QUIET, EXIT EARLY

    is_valid = not any(errors)
    if is_valid and quiet_if_valid:
        return True

    # OTHERWISE, NOISY RESULTS

    summary = [
        f"  Upstream: {upstream_address}",
        f"    Origin: {origin_address}",
        f" Pull from: {local_main_name} <- {local_main_upstream}",
        f"   Push to: current -> {remote_push_default}:{branch_push_default}",
        f"Pre-commit: {pre_commit_status}",
        f" Signature: {username} <{email_address}>",
    ]

    print("\n".join(summary), file=sys.stdout)

    sleep(0.5)  # force result to appear after summary

    if is_valid:
        print_samosa_message("This repository", "is samosa standard")
        return True
    else:
        print("ERRORS:\n" + "\n".join(errors), file=sys.stderr)
        return False
