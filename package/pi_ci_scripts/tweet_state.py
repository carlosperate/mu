#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script to tweet a message for the Raspberry Pi CI/build server.
#
# It requires all command line arguments to be provided and based on those it
# will create a message and tweet it to the account set up in the tweet_data.py
# file.
# As this file contains login information it is not included in the repository,
# all the file contains is:
# CONSUMER_KEY    = '********** YOUR INFO **********'
# CONSUMER_SECRET = '********** YOUR INFO **********'
# ACCESS_KEY      = '********** YOUR INFO **********'
# ACCESS_SECRET   = '********** YOUR INFO **********'
#
# This script should work on both Python 2 and 3.
#
from __future__ import unicode_literals, absolute_import, print_function
import sys
import optparse
#from twython import Twython

# This file is excluded from the repository and contains account data
import twitter_data as td

TWITTER_ACCOUNTS_TO_NOTIFY = ["@carlosperate"]
TWEET_LENGTH = 140


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
        msg = "Hurray! %s build %s has passed!!!" % (project, build)
    elif state == 'fail':
        msg = "Oh no! Something broke %s build %s!!!" % (project, build)
        for account in TWITTER_ACCOUNTS_TO_NOTIFY:
            msg += " %s" % account
    elif state == 'work':
        msg = "Another day, another dollar, working on %s build %s..." % \
              (project, build)

    return msg


def tweet_msg(msg):
    """
    :param msg: Message to tweet, must be less than TWEET_LENGTH characters.
    """
    if len(msg) > TWEET_LENGTH:
        print("Error: Message is too long for twitter (%s chars):\n\t%s") % \
              (len(msg), msg)
        tweet_error("Error: Prepared message > %s chars!" % TWEET_LENGTH)
        exit()

    twitter = Twython(td.CONSUMER_KEY, td.CONSUMER_SECRET,
                      td.ACCESS_KEY, td.ACCESS_SECRET)
    twitter.update_status(status=msg)
    print("Twitter message (%s characters):\n\t%s" % (len(msg), msg))


def tweet_error(msg):
    """
    :param msg: Error message to tweet, will get trimmed to fit twitter length.
    """
    mentions = ""
    for account in TWITTER_ACCOUNTS_TO_NOTIFY:
            mentions += " %s" % account
    if len(msg) > (TWEET_LENGTH - len(mentions)):
        msg = msg[:(TWEET_LENGTH - len(mentions))]
    msg += mentions

    twitter = Twython(td.CONSUMER_KEY, td.CONSUMER_SECRET,
                      td.ACCESS_KEY, td.ACCESS_SECRET)
    twitter.update_status(status=msg)
    print("Twitter ERROR message (%s characters):\n\t%s" % (len(msg), msg))


def main():
    if len(TWITTER_ACCOUNTS_TO_NOTIFY) > 75:
        print("There are too many Twitter accounts to notify.")
        exit()

    project, build, state = process_cmd_args()
    msg = prepare_msg(project, build, state)
    if msg is None:
        tweet_error("The twitter message could not be created!")
        exit()
    tweet_msg(msg)


if "__main__":
    main()
