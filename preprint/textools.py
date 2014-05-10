#!/usr/bin/env python
# encoding: utf-8
"""
Utilities for maniuplating latex documents.


Inlining latex documents
------------------------

Inline \input{*} latex files. Useful for packaging and latexdiff.

There are groups of functions: tools for working with latex files on the
regular filesystem, and functions for working with files embedded as
blobs in the git tree.

- :func:`inline` and :func:`_sub_inline` for inlining documents in the
  filesystem.
- :func:`inline_blob` to inline text from files in the git tree.
"""

import os
import re
import codecs
from preprint.gittools import read_git_blob


bib_pattern = re.compile(ur'\\bibliography{.*}', re.UNICODE)
input_pattern = re.compile(ur'\\input{(.*)}', re.UNICODE)
input_ifexists_pattern = re.compile(
    ur'\\InputIfFileExists{(.*)}{(.*)}{(.*)}',
    re.UNICODE)


def inline_bbl(root_tex, bbl_tex):
    """Inline a compiled bibliography (.bbl) in place of a bibliography
    environment.

    Parameters
    ----------
    root_tex : unicode
        Text to process.
    bbl_tex : unicode
        Text of bibliography file.

    Returns
    -------
    txt : str
        Text with bibliography included.
    """
    bbl_tex = bbl_tex.replace(u'\\', u'\\\\')
    result = bib_pattern.sub(bbl_tex, root_tex)
    return result


def _sub_line(match):
    """Function to be used with re.sub to inline files for each match."""
    fname = match.group(1)
    if not fname.endswith('.tex'):
        full_fname = ".".join((fname, 'tex'))
    else:
        full_fname = fname
    with codecs.open(full_fname, 'r', encoding='utf-8') as f:
        included_text = f.read()
    # Recursively inline files
    included_text = inline(included_text)
    return included_text


def _sub_line_ifexists(match):
    """Function to be used with re.sub for the input_ifexists_pattern."""
    fname = match.group(1)
    if os.path.exists(fname):
        if not fname.endswith('.tex'):
            full_fname = ".".join((fname, 'tex'))
        else:
            full_fname = fname
        with codecs.open(full_fname, 'r', encoding='utf-8') as f:
            included_text = f.read()
        # Append extra info after input
        included_text = "\n".join((included_text, match.group(2)))
    else:
        # Use the fall-back clause in InputIfExists
        included_text = match.group(3)

    # Recursively inline files
    included_text = inline(included_text)
    return included_text


def inline(root_text,
           replacer=_sub_line,
           ifexists_replacer=_sub_line_ifexists):
    """Inline all input latex files. The inlining is accomplished
    recursively.

    All files are opened as UTF-8 unicode files.

    Parameters
    ----------
    root_txt : unicode
        Text to process (and include in-lined files).
    replacer : function
        Function called by :func:`re.sub` to replace ``\input`` expressions
        with a latex document. Changeable only for testing purposes.
    ifexists_replacer : function
        Function called by :func:`re.sub` to replace ``\InputIfExists``
        expressions with a latex document. Changeable only for
        testing purposes.

    Returns
    -------
    txt : unicode
        Text with referenced files included.
    """
    result = input_pattern.sub(replacer, root_text)
    result = input_ifexists_pattern.sub(ifexists_replacer, result)
    return result


def inline_blob(commit_ref, root_text):
    """Inline all input latex files that exist as git blobs in a tree object.
    
    The inlining is accomplished recursively.

    All files are opened as UTF-8 unicode files.

    Parameters
    ----------
    commit_ref : str
        String identifying a git commit/tag.
    path : str
        Path of file to process in the tree

    Returns
    -------
    txt : str
        Text with referenced files included.
    """
    def _sub_blob(match):
        """Function to be used with re.sub to inline files for each match."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ".".join((fname, 'tex'))
        else:
            full_fname = fname
        included_text = read_git_blob(commit_ref, full_fname)
        if included_text is None:
            # perhaps file is not in VC
            # FIXME need to deal possibility is does not exist there either
            with codecs.open(full_fname, 'r', encoding='utf-8') as f:
                included_text = f.read()
        # Recursively inline files
        included_text = inline_blob(commit_ref, included_text)
        return included_text

    def _sub_blob_ifexists(match):
        """Function to be used with re.sub for the input_ifexists_pattern."""
        fname = match.group(1)
        if not fname.endswith('.tex'):
            full_fname = ".".join((fname, 'tex'))
        else:
            full_fname = fname

        included_text = read_git_blob(commit_ref, full_fname)
        if included_text is not None:
            # Append extra info after input
            included_text = "\n".join((included_text, match.group(2)))

        if included_text is None:
            # Use the fall-back clause in InputIfExists
            included_text = match.group(3)

        # Recursively inline files
        included_text = inline_blob(commit_ref, included_text)
        return included_text

    result = input_pattern.sub(_sub_blob, root_text)
    result = input_ifexists_pattern.sub(_sub_blob_ifexists, result)
    return result


def remove_comments(tex):
    """Delete latex comments from a manuscript.
    
    Parameters
    ----------
    tex : unicode
        The latex manuscript

    Returns
    -------
    tex : unicode
        The manuscript without comments.
    """
    # Expression via http://stackoverflow.com/a/13365453
    return re.sub(ur'(?<!\\)%.*', ur'', tex)


def main():
    with codecs.open("root.tex", 'r', encoding='utf-8') as f:
        txt = f.read()
        print txt
        print inline(txt)


if __name__ == '__main__':
    main()
