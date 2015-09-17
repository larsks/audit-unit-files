#!/usr/bin/python

import os
import sys
import argparse
import iniparse
import logging

LOG = logging.getLogger(__name__)


class IniChecker(object):
    def __init__(self):
        self.required = iniparse.ConfigParser()

    def add_required(self, path):
        self.required.read(path)

    def check_one_file(self, path):
        this = iniparse.ConfigParser()
        this.read(path)

        has_errors = False

        for section in self.required.sections():
            if not this.has_section(section):
                LOG.error('file %s is missing required section %s',
                          path,
                          section)
                has_errors = True
                continue

            for optname, optval in self.required.items(section):
                if not this.has_option(section, optname):
                    LOG.error('file %s is missing required option %s/%s',
                              path,
                              section,
                              optname)
                    has_errors = True
                    continue

                if optval == '__exists__':
                    continue

                thisval =  this.get(section, optname)
                if thisval != optval:
                    LOG.error('file %s has option %s/%s = "%s", '
                              'should be "%s"',
                              path,
                              section,
                              optname,
                              thisval,
                              optval)
                    has_errors = True
                    continue

        return not has_errors


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--require', '-r',
                   action='append',
                   default=[])
    p.add_argument('--all', '-a',
                   action='store_true')
    p.add_argument('files', nargs='*')
    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig()

    checker = IniChecker()

    for path in args.require:
        checker.add_required(path)

    has_errors = False
    for path in args.files:
        if not checker.check_one_file(path):
            has_errors = True

            if not args.all:
                break

    if has_errors:
        sys.exit(1)

if __name__ == '__main__':
    main()

