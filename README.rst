########
preprint
########

*Tools for preparing astrophysics papers.*

Installation requires `cliff <https://cliff.readthedocs.org/en/latest/>`_, the ``watchdog`` package and a recent version of setuptools.
To install ``preprint``, run ``python setup.py install``.
Then try ``preprint --help`` for more info.

Preprint currently supports the following command (see below for a reference):

- ``preprint watch`` to automatically compile the paper if source is changed

I'm working on a ``latexdiff`` driver command, along with an arXiv/AASTeX submission packaging command.
Check the `Github Issues <https://github.com/jonathansick/preprint/issues>`_ to submit additional ideas.

====================================
Configuration System / preprint.json
====================================

``preprint`` configurations are determined from (in order of increasing precedence): internal defaults, a project-specific JSON file, command line arguments.

The JSON configurations file makes ``preprint`` much easier to use.
The configuration file should be named ``preprint.json``, and be located in the root directory of the LaTeX project.
Here is an example of its format::

    { 
        "master": "paper.tex",
        "exts": ['tex', 'pdf', 'eps'],
        "cmd": "make"
    }

If set in ``preprint.json``, any command line setting of the same name does not need to repeated.

=================
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


=====
About
=====

`Preprint is developed on Github <https://github.com/jonathansick/preprint>`_. Contributions and suggestions are welcome.

Copyright 2014 Jonathan Sick, @jonathansick

Licensed BSD.
