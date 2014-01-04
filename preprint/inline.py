#!/usr/bin/env python
# encoding: utf-8
"""
Inline \input{*} latex files. Useful for packaging and latexdiff.

There are groups of functions: tools for working with latex files on the
regular filesystem, and functions for working with files embedded as
blobs in the git tree.

For files on the file system:

- :func:`inline` and :func:`_sub_inline`.

For files in the git tree:

- :func:`read_git_blob` to read text from a git blob
- :func:`inline_blob` to inline text from files in the git tree.
"""

import re
import codecs
import git
import os


def inline(root_text):
    """Inline all input latex files. The inlining is accomplished
    recursively.

    All files are opened as UTF-8 unicode files.

    Parameters
    ----------
    root_txt : str
        Text to process (and include in-lined files).

    Returns
    -------
    txt : str
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


def read_git_blob(commit_ref, path):
    """Get text from a git blob."""
    repo = git.Repo('.')
    tree = repo.tree(commit_ref)
    dirname, fname = os.path.split(path)
    if dirname == '':
        text =_read_blob(tree, fname)
    else:
        components = path.split(os.sep)
        text = _read_blob_in_tree(tree, components)
    return text


def _read_blob_in_tree(tree, components):
    """Recursively open trees to ultimately read a blob"""
    if len(components) == 1:
        # Tree is direct parent of blob
        return _read_blob(tree, components[0])
    else:
        # Still trees to open
        dirname = components.pop(0)
        for t in tree.trees:
            if t.name == dirname:
                return _read_blob_in_tree(t, components)


def _read_blob(tree, filename):
    for blb in tree.blobs:
        if blb.name == filename:
            txt = unicode(blb.data_stream.read(), 'utf-8')
            # txt = txt.encode('utf-8')
            return txt
    return None


def main():
    with codecs.open("root.tex", 'r', encoding='utf-8') as f:
        txt = f.read()
        print txt
        print inline(txt)


if __name__ == '__main__':
    main()
