#! /usr/bin/env python3
"""
This script is used to identify and clean up 'obsolete' local branches that no longer exist
on the remote side, e.g. after merging a Pull Request and remove the feature branch on Github.
"""

import os
import sys
import argparse
import subprocess

prog = os.path.basename(sys.argv[0])

parser = argparse.ArgumentParser(
    description="Remove obsolete local branches that no longer exist on the remote side.",
    epilog="Find more information at https://digitalduke.github.io/git-tools/"
)

parser.add_argument(
    "--version",
    action="version",
    version="{prog} version 1.0".format(prog=prog)
)


def run(cmd):
    """ Run a shell command and return the output """

    if isinstance(cmd, str):
        cmd = cmd.split()

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip().decode()
    except Exception as e:
        sys.exit("ERROR [%s]: %s" % (prog, e))

    return output


def git_rm_local_branches():
    """ Remove local branches that no longer exist on remote repository """

    parser.parse_args()

    if not run("git rev-parse --is-inside-work-tree"):
        sys.exit("ERROR [%s]: You are not under a git repository" % prog)

    # Do a prune fetch
    run("git fetch -p")

    # Figure out the list of local branches that no longer exist on the remote side
    cmd = "git branch -vv | grep ': gone]' | awk '{ print $1 }'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    local_only_branches = p.communicate()[0].strip().decode().splitlines()

    if not local_only_branches:
        exit_str = ("No local branch is found that no longer exists on the remote side" +
                    " - You are all good.")
        sys.exit(exit_str)

    print("The following local only branches will be removed:\n%s" % local_only_branches)

    remove = input("Proceed? [Y/N] ")
    if remove in ('Y', 'y'):
        for b in local_only_branches:
            run("git branch -D %s" % b)


if __name__ == "__main__":

    git_rm_local_branches()
