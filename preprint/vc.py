#!/usr/bin/env python
# encoding: utf-8
"""
Runs the vc tool, if available, to update the version control string in your
latex document.

See http://www.ctan.org/pkg/vc
"""

import os
import subprocess
import logging


log = logging.getLogger(__name__)


def vc_exists():
    """Return `True` if the project uses vc."""
    if os.path.exists('vc') and os.path.exists('vc-git.awk'):
        log.debug("Found a vc installation")
        return True
    else:
        log.debug("Did not find a vc installation")
        return False


def run_vc():
    """Run the vc tool."""
    if vc_exists():
        log.debug("Running vc")
        subprocess.call("./vc", shell=True)
