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

import re
import codecs
from preprint.gittools import read_git_blob


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
    bib_pattern = re.compile(ur'\\bibliography{.*}', re.UNICODE)
    result = bib_pattern.sub(bbl_tex, root_tex)
    return result


def inline(root_text):
    """Inline all input latex files. The inlining is accomplished
    recursively.

    All files are opened as UTF-8 unicode files.

    Parameters
    ----------
    root_txt : unicode
        Text to process (and include in-lined files).

    Returns
    -------
    txt : unicode
        Text with referenced files included.
    """
    input_pattern = re.compile(ur'\\input{(.*)}', re.UNICODE)
    result = input_pattern.sub(_sub_line, root_text)
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
        # Recursively inline files
        included_text = inline_blob(commit_ref, included_text)
        return included_text
    input_pattern = re.compile(ur'\\input{(.*)}', re.UNICODE)
    result = input_pattern.sub(_sub_blob, root_text)
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
    # Expression via http://stackoverflow.com/a/13365225
    return re.sub(ur'[^\\]%.*', ur'', tex)


def main():
    with codecs.open("root.tex", 'r', encoding='utf-8') as f:
        txt = f.read()
        print txt
        print inline(txt)


if __name__ == '__main__':
    main()
