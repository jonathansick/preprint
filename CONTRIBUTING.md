# Contributing to Preprint

Thanks for helping out with preprint. The prerequisite for working on preprint is a [GitHub](http://github.com) account. This document gives tips on how to submit bug reports, or if you're a developer, how to build the source code to test changes, and what to do when submitting a pull request.

## Contents

* [Submitting a Bug Report (Issues)](#issues)
* [Building & Editing preprint (Development)](#dev)
  - [Code Overview & Philosophy](#code-overview)
  - [Building preprint](#building)
  - [Making & Submitting Changes (Pull Request)](#pull-requests)

***

<a name="issues"></a>
## Submitting a Bug Report

If preprint doesn't work right, *submit an [Issue](https://github.com/jonathansick/preprint/issues)*.

To help us out, you'll want to re-run your preprint command with the `--debug` flag turned on.

When submitting an [Issue](https://github.com/jonathansick/preprint/issues), mention the command or paper you're running, and copy the debugging output of the log file or terminal.

*Thank you!*

***

<a name="dev"></a>
## Building & Editing Preprint

<a name="code-overview"></a>
### Code Overview & Philosophy

Preprint is a command line tool built around the [cliff](https://cliff.readthedocs.org/en/latest/) framework. This means that each subcommand needs to be registered as a setuptools entrypoint. See [`setup.py`](https://github.com/jonathansick/preprint/blob/master/setup.py) and [`preprint/make.py`](https://github.com/jonathansick/preprint/blob/master/preprint/make.py) for an example of a simple command. Before building a new command, create an Issue and I can help you set it up.

<a name="building"></a>
### Building Preprint

First, clone the source code from GitHub:

    git clone https://github.com/jonathansick/preprint.git
    cd preprint

(If you're making changes to the source, you'll want to work from your own fork, see below.)

To install, run

    python setup.py install

To check your installation, you can run commands like:

    rehash
    which preprint
    preprint --version
    preprint --help

<a name="pull-request"></a>
### Making & Submitting Changes (Pull Request)

Here are some guidelines for developing Preprint to fix a bug or implement a new feature.

1. Submit an [Issue](https://github.com/jonathansick/preprint/issues) so we know what you're up to. This Issue will get closed by the pull request, and also make sure that effort isn't duplicated.
2. Fork Preprint; [this guide](https://guides.github.com/activities/forking/) will tell you how.
3. Work from a branch, e.g., `git co -b dev/my_fix`.
4. Make sure your changes conform to [PEP8](http://legacy.python.org/dev/peps/pep-0008/). The pep8 package helps with this: `pip install pep8`. Also, all variables should be named `like_this` and not `likeThis` (i.e., use underscore separators, not camel case).
5. Submit the Pull Request as mentioned in the GitHub guide. In the comment for your pull request, mention the Issue number (e.g. 'fixes #33.')

*Thank you*