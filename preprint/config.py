#!/usr/bin/env python
# encoding: utf-8
"""
Manager for configuration defaults.

TODO change to a JSON file since we need lists.
"""

import os
import json


class Configurations(object):
    """Configurations determines and provides default settings that can
    be overriden by the user on the command line.

    Configurations are set at two levels:

    1. There are built-in defaults that ensure all configurations are
        always set.
    2. These can be overriden by settings in a json file (an example is below).

    Each command uses these configurations to set the default state of
    each command line option. Thus each command ultimatly gets the
    final configuration state from the argparser.

    An example json file, named "preprints.json":
    
    ::
        {
            "master": "skysub.tex",
            "exts": ["tex", "eps", "pdf"],
            "cmd": "make"
        }
    """

    _DEFAULTS = {
        "master": "paper.tex",
        "exts": ['tex', 'pdf', 'eps'],
        "cmd": "make"
        }

    def __init__(self):
        super(Configurations, self).__init__()
        self._confs = dict(self._DEFAULTS)
        # Read configurations
        if os.path.exists("preprint.json"):
            with open("preprint.json", 'r') as f:
                self._confs.update(json.load(f))

    def default(self, name):
        """Get the default value for the named config, given the section."""
        return self._DEFAULTS[name]

    def config(self, name):
        """Get the configuration."""
        return self._confs[name]


if __name__ == '__main__':
    conf = Configurations()
    print conf.default("master")
    print conf.default("exts")
    print conf.default("cmd")
    print conf.config("exts")
    print type(conf.config("exts"))
    print conf.config("cmd")
