#!/usr/bin/env python
# encoding: utf-8
"""
Inline \input{*} latex files. Useful for packaging and latexdiff.

Inspired by

- http://dropbearcode.blogspot.ca/2011/09/multiple-file-latex-diff.html
- http://stackoverflow.com/questions/393843/python-and-regular-expression-with-unicode
"""

import re
import codecs


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


def main():
    with codecs.open("root.tex", 'r', encoding='utf-8') as f:
        txt = f.read()
        print txt
        print inline(txt)


if __name__ == '__main__':
    main()
