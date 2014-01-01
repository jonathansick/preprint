========
preprint
========

*Tools for preparing astrophysics papers.*

Installation requires `cliff <https://cliff.readthedocs.org/en/latest/>`_, the `watchdog` package and a recent version of setuptools.
To install `preprint`, run `python setup.py install`.
Then try `preprint --help` for more info.

Command Reference
=================

watch
-----

``preprint watch`` will automatically compile your paper if a TeX or graphics source file is changed.

Usage::

    preprint [--master MASTER] watch [--exts; --cmd]

    Optional arguments:
    --master   Name of the root LaTeX file (eg, paper.tex)
    --exts     List of file extensions (defaults to `pdf eps tex`)
    --cmd      Name of command to run when a change occurs (defaults to `make`)


About
=====

Copyright 2014 Jonathan Sick, @jonathansick

Licensed BSD.
