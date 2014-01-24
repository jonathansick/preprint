#!/usr/bin/env python
# encoding: utf-8
"""
Tests for regular expression detection of ``\inline{*}`` commands.
"""

from preprint.textools import inline


def _mock_sub_line(match):
    return u"Replaced"


def test_standard_inline():
    """Test :func:`inline` to detecting ``\inline{*}`` commands."""
    data = u"Keep\n\input{test}"
    processed_data = inline(data, replacer=_mock_sub_line)
    assert processed_data == u"Keep\nReplaced"
