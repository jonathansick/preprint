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


def test_ifexists_inline():
    """Test :func:`inline` to detecting ``\InputIfFileExists{*}`` commands."""
    data = u"Keep\n\InputIfFileExists{test}{a}{b}"
    processed_data = inline(
        data, ifexists_replacer=_mock_sub_line, replacer=_mock_sub_line)
    assert processed_data == u"Keep\nReplaced"
