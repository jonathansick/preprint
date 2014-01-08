#!/usr/bin/env python
# encoding: utf-8
"""
Command for packaging the manuscript for submission.
"""

import logging
import os
import shutil
import codecs
import re

from preprint.inline import inline

from cliff.command import Command


class Package(Command):
    """Package manuscript for arxiv/journal submission"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Package, self).get_parser(prog_name)
        parser.add_argument('name',
            help="Name of packaged manuscript (saved to build/name).")
        return parser

    def take_action(self, parsed_args):
        dirname = os.path.join("build", parsed_args.name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with codecs.open(self.app.options.master, 'r', encoding='utf-8') as f:
            root_text = f.read()

        tex = inline(root_text)
        tex = self._delete_comments(tex)
        tex = self._flatten_figures(tex, dirname)

        output_tex_path = os.path.join(dirname,
                os.path.basename(self.app.options.master))
        self._write_tex(tex, output_tex_path)

    def _delete_comments(self, tex):
        """Remove all comments from the manuscript."""
        # Expression via http://stackoverflow.com/a/13365225
        return re.sub(ur'[^\\]%.*', ur'', tex)

    def _flatten_figures(self, tex, dirname):
        """Discover figures and copy to root of build directory.
        
        Returns
        -------
        figs : dict
            A dictionary of with figure names (without extension or directory)
            as the key and the current full path as the value.
        """
        figs = discover_figures(tex)
        tex = install_figs(tex, figs, dirname,
                aas_numbering=False)
        print figs
        return tex

    def _write_tex(self, tex, path):
        """Write the LaTeX to the output path."""
        with codecs.open(path, 'w', encoding='utf-8') as f:
            f.write(tex)


def discover_figures(tex):
    """Find all figures in the manuscript.

    Returns
    -------
    figs : dict
        A dictionary with figure names (without extension or directory)
        as the key and and values are dicts with keys: path, options and
        figure environment.
    """
    figs_pattern = re.compile(ur"\\includegraphics(.*?){(.*?)}",
            re.UNICODE)
    matches = figs_pattern.findall(tex)
    figs = {}
    for i, match in enumerate(matches):
        opts, path = match
        basename = os.path.splitext(os.path.basename(path))[0]
        figs[basename] = {"path": path,
                          "exts": _find_exts(path),
                          "options": opts,
                          "env": ur"\\includegraphics",
                          "num": i}
    return figs


def _find_exts(fig_path):
    """Return a tuple of all formats for which a figure exists."""
    basepath = os.path.splitext(fig_path)[0]
    has_exts = []
    for ext in ('pdf', 'eps', 'ps', 'png', 'jpg', 'tif'):
        p = ".".join((basepath, ext))
        if os.path.exists(p):
            has_exts.append(ext)
            # print "exists", p
    print fig_path, has_exts
    return tuple(has_exts)


def install_figs(tex, figs, install_dir, aas_numbering=False,
        format_priority=('pdf', 'eps', 'ps', 'png', 'jpg', 'tif')):
    """Copy each figure to the build directory and update tex with new path.
    """
    for figname, fig in figs.iteritems():
        print figname, fig
        if len(fig['exts']) == 0: continue
        # get the priority graphics file type
        for ext in format_priority:
            if ext in fig['exts']:
                full_path = ".".join((os.path.splitext(fig['path'])[0], ext))
                break
        # copy fig to the build directory
        install_path = os.path.join(install_dir, os.path.basename(full_path))
        figs[figname]["installed_path"] = install_path
        shutil.copy(full_path, install_path)
        # update tex by replacing old filename with new.
        old_fig_cmd = ur"{0}{1}{{2}}".format(fig['env'], fig['options'],
            fig['path'])
        new_fig_cmd = ur"{0}{1}{{2}}".format(fig['env'], fig['options'],
            os.path.basename(os.path.splitext(fig['path'])[0]))
        tex = re.sub(old_fig_cmd, new_fig_cmd, tex)
    return tex
