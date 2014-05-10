########
preprint
########

*Tools for preparing astrophysics papers.* Preprint lets you automatically compile, typeset document differences and package the manuscript for publication.

Installation requires `cliff <https://cliff.readthedocs.org/en/latest/>`_, the `watchdog <https://pypi.python.org/pypi/watchdog>`_ package, the `GitPython >=0.3 <https://pypi.python.org/pypi/GitPython/0.3.2.RC1>`_ package, and a recent version of setuptools.

To install from PyPI::

    pip install preprint

Or to install from source, check the code out and run::

    python setup.py install

After installing, try ``preprint --help`` for more info.

Preprint currently supports the following commands (see below for a reference):

- ``preprint make`` to do a one-off compilation of the paper,
- ``preprint watch`` to automatically compile the paper if source is changed,
- ``preprint diff`` to run ``latexdiff`` against a commit in Git,
- ``preprint pack`` to package the document for journals or the arXiv.

Check the `GitHub Issues <https://github.com/jonathansick/preprint/issues>`_ to submit additional ideas.

====================================
Configuration System / preprint.json
====================================

``preprint`` configurations are determined from (in order of increasing precedence): internal defaults, a project-specific JSON file, and command line arguments.

The JSON configurations file makes ``preprint`` much easier to use.
The configuration file should be named ``preprint.json``, and be located in the root directory of the LaTeX project.
Here is an example of its format::

    { 
        "master": "paper.tex",
        "exts": ["tex", "pdf", "eps"],
        "cmd": "latexmk -f -pdf -bibtex-cond {master}"
    }

If set in ``preprint.json``, any command line setting of the same name does not need to repeated.

Note that the ``cmd`` command, which provides the latex build command, includes a ``master`` variable.
This variable will take the value of the ``master`` configuration value, and thus custom latex compilation commands can be flexibly given the name of the main tex file.

=================
Command Reference
=================

make
----

``preprint make`` will perform a one-off compilation of your paper.

Usage::

    preprint [--master MASTER] make [--cmd CMD]

    Optional arguments:
    --master   Name of the root LaTeX file (eg, paper.tex)
    --cmd      Name of command to run when a change occurs


If ``preprint.json`` is setup, you can just run::

    preprint make


watch
-----

``preprint watch`` will automatically compile your paper if a TeX or graphics source file is changed.

Usage::

    preprint [--master MASTER] watch [--exts EXT1, ..., EXTN; --cmd CMD; --diff [SHA]]

    Optional arguments:
    --master   Name of the root LaTeX file (eg, paper.tex)
    --exts     List of file extensions (defaults to `pdf eps tex`)
    --cmd      Name of command to run when a change occurs
    --diff     Run a latexdiff compile against the given commit SHA from the git repository (HEAD if blank).

For example, to continuously compile the document whenever ``.tex`` or figures have changed, and assuming you've setup a ``preprint.json`` file with the name of your master document, just run::

    preprint watch

To continuously run a latexdiff-based compile, showing all changes you've made against the HEAD of the git repository, run::

    preprint watch --diff

The document will be saved to ``build/PAPER_NAME_diff.pdf``.
This is a nice way of keeping track of what you're doing.

Finally, to continuously run a latexdiff-based compile against an arbitrary commit in your git history, just copy the commit SHA fragment (say, ``b91688d``) and run::

    preprint watch --diff b91688d


diff
----

``preprint diff`` will typeset the document with revisions highlighted between the currently checked-out version, and a previous git commit.
This command is powered by the `latexdiff <http://latexdiff.berlios.de>`_ (which is probably installed with your tex distribution).
The command also requires `latexmk <http://users.phys.psu.edu/~collins/software/latexmk-jcc/>`_ to compile the difference document.
This command is compatible with documents that use ``\input{}`` to combine text documents; in fact, included documents are inlined recursively.
``preprint diff`` was inspired by `this blog post <http://astrowizici.st/blog/2013/10/04/publishing-with-git/>`_ by Andy Casey.

Usage::

    preprint [--master MASTER] diff PREV_SHA [-n NAME]

    Arguments:
    PREV_SHA   A SHA fragment or tag name pointing to the previous revision.

    Optional arguments:
    --master   Name of the root LaTeX file (eg, paper.tex)
    -n         Output name of the difference document (eg. diff.tex)


pack
----

``preprint pack`` prepares a preprint for submission to a journal.
This pipeline includes:

1. Creating a build directory and copying over just the required manuscript files,
2. Inlining all inputted latex files (either with ``\input{}`` or ``\InputIfFileExists`` syntax),
3. Copying the ``.bbl`` bibliography or inlining it into the manuscript, as necessary.
4. Moving figures to the root directory and updating tex source,
5. Deleting comments; don't be a tweet on @OverheardOnAph,
6. Renaming figures to conform to AASTeX if necessary,
7. Making JPEG versions of figures to to fulfill arXiv file size requirements, if necessary. This requires `imagemagick <http://www.imagemagick.org/script/index.php>`_.

This command is inspired by Erik Tollerud's `Astropysics package <http://pythonhosted.org/Astropysics/coremods/publication.html>`_, but is designed around regular expressions for text transformation.
The implementation should thus be easier.

Usage::

    preprint [--master MASTER] pack NAME [--style STYLE; --exts EXT1, ..., EXTN]

    Arguments:
    NAME   Name of the build. Products copied to build/NAME directory.

    Optional arguments:
    --master   Name of the root LaTeX file (eg, paper.tex)
    --exts     File format priority for figures (e.g., ``eps, pdf``)
    --style    Style for the build (default is ``aastex``, can also be ``arxiv``).
    --maxsize  Maximum size of figure in MB before compressing into jpg (for
               ``arxiv``). Default is 2.5 MB.

Note that the ``--exts`` option can be used to prefer a certain file format for the build if you maintain both EPS and PDF figure sets.
For example, to generate a manuscript for a AAS journal, run::

    preprint pack my_aas_build --style aastex --exts eps

And to build for the arxiv, where PDF figures are preferred, run::

    preprint pack my_arxiv_build --style arxiv --exts pdf

=====
About
=====

`Preprint is developed on GitHub <https://github.com/jonathansick/preprint>`_.
Contributions and suggestions are welcome;
read `the CONTRIBUTING guidelines <https://github.com/jonathansick/preprint/blob/master/CONTRIBUTING.md>`_ for instructions on how to help.

Copyright 2014 Jonathan Sick, @jonathansick

Licensed BSD.
