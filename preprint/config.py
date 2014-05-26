#!/usr/bin/env python
# encoding: utf-8
"""
Manager for configuration defaults.
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

    An example json file, named "preprint.json":
    
    ::
        {
            "master": "skysub.tex",
            "exts": ["tex", "eps", "pdf"],
            "cmd": "latexmk -f -pdf -bibtex-cond {master}"
        }


    *Notes on the ``cmd`` option:* this open accepts a ``master`` template
    variable that will be replaced with the value of the ``master``
    configuration variable. This can be used to tell the appropriate latex
    build command what the master tex file is (see example above).
    """

    _DEFAULTS = {
        "master": "paper.tex",
        "exts": ["tex", "pdf", "eps"],
        "cmd": "latexmk -f -pdf -bibtex-cond {master}"}

    def __init__(self):
        super(Configurations, self).__init__()
        self._confs = dict(self._DEFAULTS)
        # Read configurations
        if os.path.exists("preprint.json"):
            with open("preprint.json", 'r') as f:
                self._confs.update(json.load(f))
        self._sanitize_path('master')

    def default(self, name):
        """Get the default value for the named config, given the section."""
        return self._DEFAULTS[name]

    def config(self, name):
        """Get the configuration."""
        if name == "cmd":
            return self._confs['cmd'].format(master=self._confs['master'])
        else:
            return self._confs[name]

    @property
    def default_dict(self):
        return dict(self._DEFAULTS)

    def _sanitize_path(self, key):
        """Sanitize the path of a configuration given `key`."""
        p = self._confs[key]
        p = os.path.expandvars(os.path.expanduser(p))
        if os.path.dirname(p) == ".":
            p = os.path.basename(p)
        self._confs[key] = p


if __name__ == '__main__':
    conf = Configurations()
    print conf.default("master")
    print conf.default("exts")
    print conf.default("cmd")
    print conf.config("exts")
    print type(conf.config("exts"))
    print conf.config("cmd")
