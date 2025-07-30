#!/usr/bin/env python3
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
import os

import click

from samosa import git_task


def get_raw_root_or_exit():
    root = git_task.get_root_from_path(os.getcwd())
    if not root:
        exit("No repository found.")

    return root


def get_valid_root_or_exit():
    root = get_raw_root_or_exit()
    if not git_task.fix_and_validate_root(root, quiet_if_valid=True):
        exit(1)

    return root


@click.group()
def samosa():
    """
    Enforce a triangular Git workflow. If this is not possible, explain why.
    """


@samosa.command()
@click.argument("remote")
@click.argument("url")
def add(remote, url):
    """
    Add URL as remote repository named REMOTE.
    """

    root = get_valid_root_or_exit()
    git_task.add_remote(root, remote, url)


@samosa.command()
@click.argument("branch")
def checkout(branch):
    """
    Check out a new or existing BRANCH.
    """

    root = get_valid_root_or_exit()
    git_task.checkout_branch(root, branch)


@samosa.command()
@click.argument("url")
def clone(url):
    """
    Clone remote URL as a local repository.
    """

    working_path = os.getcwd()
    git_task.initialise_repository(working_path)
    root = get_raw_root_or_exit()

    print("Adding remotes...")
    git_task.add_remote(root, "origin", url, perform_fetch=False)
    git_task.add_remote(root, "upstream", url)

    print("Checking out main branch...")
    git_task.checkout_branch(root, "main")

    print("Validating local repository...")
    if git_task.fix_and_validate_root(root, quiet_if_valid=True):
        exit(0)
    else:
        exit(1)


@samosa.command()
@click.argument("message")
def commit(message):
    """
    Commit changes with a signed MESSAGE.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("add", ".")
    git_task.shell("commit", "-asm", message)


@samosa.command()
def fetch():
    """
    Fetch all remote updates without changing local files.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("fetch", "--all")


@samosa.command()
def diff():
    """
    Compare with upstream.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("--no-pager", "diff", "upstream/main")


@samosa.command()
def status():
    """
    Inspect and repair local repository. Provide manual instructions if necessary.
    """

    root = get_raw_root_or_exit()
    if git_task.fix_and_validate_root(root, quiet_if_valid=False):
        exit(0)
    else:
        exit(1)


@samosa.command()
def force():
    """
    Force-push changes to remote branch.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("--no-pager", "push", "--force")


@samosa.command()
def graph():
    """
    Show detailed commit graph.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("log", "--graph", "--oneline", "--decorate", "--all", limit=20)


@samosa.command()
def init():
    """
    Initialise an empty local repository.
    """

    working_path = os.getcwd()
    git_task.initialise_repository(working_path)
    root = get_raw_root_or_exit()

    if git_task.fix_and_validate_root(root, quiet_if_valid=True):
        exit(0)
    else:
        exit(1)


@samosa.command()
def log():
    """
    Show streamlined commit log.
    """

    _ = get_valid_root_or_exit()
    git_task.shell("log", "--first-parent", "--oneline", limit=10)


@samosa.command()
@click.argument("branch", required=False)
def pull(branch):
    """
    Pull changes from remote. Use default settings.

    If BRANCH is named, do not use default settings, instead rebase changes from named upstream branch.
    """

    _ = get_valid_root_or_exit()
    if branch is None:
        git_task.shell("pull")
    else:
        git_task.shell("pull", "upstream", branch, "--rebase")


@samosa.command()
def push():
    """
    Push changes to remote branch.
    """

    _ = get_valid_root_or_exit()
    git_task.run_subprocess("--no-pager", "push")
