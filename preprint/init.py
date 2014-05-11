#!/usr/bin/env python
# encoding: utf-8
import logging
import fnmatch
import os
import codecs
import re
import json

from cliff.command import Command

from preprint.config import Configurations


docclass_pattern = re.compile(ur'\\documentclass{.*}', re.UNICODE)


class Init(Command):
    """Initialze the project with preprint.json configurations."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Init, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        write_configs()
        self.log.info("Wrote preprint.json")


def write_configs():
    """Write a default configurations file for the current project."""
    try:
        root_tex = find_root_paper()
    except RootNotFound:
        root_tex = "article.tex"
    configs = Configurations()
    config_dict = configs.default_dict
    config_dict['master'] = root_tex
    if os.path.exists("preprint.json"):
        os.remove("preprint.json")
    with open("preprint.json", 'w') as f:
        f.write(json.dumps(config_dict,
                           sort_keys=True,
                           indent=4,
                           separators=(',', ': ')))


def find_root_paper():
    """Find the tex article in the current directory that can be considered
    a root. We do this by searching contents for `\documentclass`.
    """
    log = logging.getLogger(__name__)
    for tex_path in tex_documents():
        with codecs.open(tex_path, 'r', encoding='utf-8') as f:
            text = f.read()
            if len(docclass_pattern.findall(text)) > 0:
                log.debug("Found root tex {0}".format(tex_path))
                return tex_path
    log.warning("Could not find a root .tex file")
    raise RootNotFound


def tex_documents(ignore_dirs=('build',)):
    """Iterate through all .tex documents in the current directory"""
    for path, dirlist, filelist in os.walk("."):
        for name in fnmatch.filter(filelist, "*.tex"):
            yield os.path.join(path, name)


class RootNotFound(BaseException):
    pass
