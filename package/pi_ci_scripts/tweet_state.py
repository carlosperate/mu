#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
import sys
import optparse
from twython import Twython

# This file is excluded from the repository and contains account data
import twitter_data as td


def process_cmd_args():
    """
    Parses the command line argument flgas into the return values.
    :return: Tuple with the build number and build state.
    """
    parser = optparse.OptionParser()
    parser.add_option("-p", "--project", help="Project name", default=None)
    parser.add_option("-b", "--build", help="Build number", default=None)
    parser.add_option("-s", "--state", help="Build state (work/pass/fail)",
                      default=None)
    (opts, args) = parser.parse_args()
    opts = vars(opts)

    for item in opts:
        if opts[item] is None:
            print("All flags are required in this script (info with -h flag).")
            exit()
        if item == "state" and (opts[item] not in ("pass", "fail", "work")):
            print("The state flag must have the value 'pass', 'fail', 'work'.")
            print(opts[item])
            exit()

    return opts["project"], opts["build"], opts["state"]


def prepare_msg(project, build, state):
    """
    :param project: Project name
    :param build: Build number
    :param state: Build state (pass/fail/work)
    :return: A string message with the build state.
    """
    msg = None
    if state == 'pass':
        msg = "Hurray! The %s build %s has passed!!!" % (project, build)
    elif state == 'fail':
        msg = "Oh no! Something broke %s build %s!!! @carlosperate" % \
              (project, build)
    elif state == 'work':
        msg = "Another day, another dollar, working on %s build %s..." % \
              (project, build)

    return msg


def tweet_msg(msg):
    """
    :param msg: Message to tweet, must be less than 140 characters long.
    """
    if len(msg) > 140:
        print("The prepared message is larger than 140 characters (%s):\n\t%s"
              % (len(msg), msg))
        exit()
    twitter = Twython(td.CONSUMER_KEY, td.CONSUMER_SECRET,
                      td.ACCESS_KEY, td.ACCESS_SECRET)
    twitter.update_status(status=msg)
    print("Twitter message (%s characters):\n\t%s" % (len(msg), msg))


def main():
    project, build, state = process_cmd_args()
    msg = prepare_msg(project, build, state)
    if msg is None:
        "The twitter message could not be created."
        exit()
    tweet_msg(msg)


if "__main__":
    main()
