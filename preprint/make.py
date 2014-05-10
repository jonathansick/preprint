#!/usr/bin/env python
# encoding: utf-8
import logging
import subprocess

from cliff.command import Command

from .vc import run_vc


class Make(Command):
    """Do a one-off compilation of the paper"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Make, self).get_parser(prog_name)
        parser.add_argument(
            '--cmd',
            default=self.app.confs.config('cmd'),
            help="Command to run for compilation")
        return parser

    def take_action(self, parsed_args):
        run_vc()
        cmd = parsed_args.cmd.format(master=self.app.options.master)
        self.log.debug("Compiling with {0}".format(cmd))
        subprocess.call(cmd, shell=True)
