#!/usr/bin/env python
# encoding: utf-8
import logging
import os
import json

from cliff.command import Command
from paperweight.texutils import find_root_tex_document, RootNotFound

from preprint.config import Configurations


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
        root_tex = find_root_tex_document(base_dir=".")
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
