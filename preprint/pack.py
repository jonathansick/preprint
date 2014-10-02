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
import subprocess

from preprint.textools import inline, remove_comments, inline_bbl

from cliff.command import Command


class Package(Command):
    """Package manuscript for arxiv/journal submission"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Package, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help="Name of packaged manuscript (saved to build/name).")
        parser.add_argument(
            '--style',
            default="aastex",
            choices=['aastex', 'arxiv'],
            help="Build style (aastex, arxiv).")
        parser.add_argument(
            '--exts',
            nargs='*',
            default=self.app.confs.config('exts'),
            help="Figure extensions to use in order of priority")
        parser.add_argument(
            '--jpeg',
            action='store_true',
            default=False,
            help="Make JPEG versions of figures if too large (for arxiv)")
        parser.add_argument(
            '--maxsize',
            default=2.,
            type=float,
            help="Max figure size (MB) before converting to JPEG (for arxiv)")
        return parser

    def take_action(self, parsed_args):
        dirname = os.path.join("build", parsed_args.name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self._build_style = parsed_args.style
        self._ext_priority = parsed_args.exts
        self._max_size = parsed_args.maxsize

        bbl_path = ".".join((os.path.splitext(self.app.options.master)[0],
                             'bbl'))

        with codecs.open(self.app.options.master, 'r', encoding='utf-8') as f:
            root_text = f.read()
        tex = inline(root_text)
        tex = remove_comments(tex)
        tex = self._process_figures(tex, dirname)
        if os.path.exists(bbl_path):
            with codecs.open(bbl_path, 'r', encoding='utf-8') as f:
                bbl_text = f.read()
            tex = inline_bbl(tex, bbl_text)
        else:
            self.log.debug("Skipping .bbl installation")

        if self._build_style == "aastex":
            output_tex_path = os.path.join(dirname, "ms.tex")
        else:
            output_tex_path = os.path.join(
                dirname,
                os.path.basename(self.app.options.master))
        self._write_tex(tex, output_tex_path)

    def _process_figures(self, tex, dirname):
        """Discover figures and copy to root of build directory.

        Returns
        -------
        figs : dict
            A dictionary of with figure names (without extension or directory)
            as the key and the current full path as the value.
        """
        figs = discover_figures(tex, self._ext_priority)
        if self._build_style == "aastex":
            maxsize = None
        elif self._build_style == "arxiv":
            maxsize = self._max_size

        tex = install_figs(
            tex, figs, dirname,
            naming=self._build_style,
            format_priority=self._ext_priority,
            max_size=maxsize)
        return tex

    def _write_tex(self, tex, path):
        """Write the LaTeX to the output path."""
        with codecs.open(path, 'w', encoding='utf-8') as f:
            f.write(tex)


def discover_figures(tex, ext_priority):
    """Find all figures in the manuscript.

    Returns
    -------
    figs : dict
        A dictionary with figure names (without extension or directory)
        as the key and and values are dicts with keys: path, options and
        figure environment.
    """
    figs_pattern = re.compile(
        ur"\\includegraphics(.*?){(.*?)}",
        re.UNICODE)
    matches = figs_pattern.findall(tex)
    figs = {}
    for i, match in enumerate(matches):
        opts, path = match
        basename = os.path.splitext(os.path.basename(path))[0]
        # Find all formats this file exists in
        exts = _find_exts(path, ext_priority)
        # Get file sizes for all variants here
        _dir = os.path.dirname(path)
        sizes = []
        for ext in exts:
            p = os.path.join(_dir, ".".join((basename, ext)))
            sizes.append(os.path.getsize(p) / 10. ** 6.)
        figs[basename] = {"path": path,
                          "exts": exts,
                          "size_mb": sizes,
                          "options": opts,
                          "env": ur"\\includegraphics",
                          "num": i + 1}
    return figs


def _find_exts(fig_path, ext_priority):
    """Return a tuple of all formats for which a figure exists."""
    basepath = os.path.splitext(fig_path)[0]
    has_exts = []
    for ext in ext_priority:
        p = ".".join((basepath, ext))
        if os.path.exists(p):
            has_exts.append(ext)
            # print "exists", p
    print fig_path, has_exts
    return tuple(has_exts)


def install_figs(tex, figs, install_dir, naming=None,
                 format_priority=('pdf', 'eps', 'ps', 'png', 'jpg', 'tif'),
                 max_size=None):
    """Copy each figure to the build directory and update tex with new path.

    Parameters
    ----------
    tex : unicode
        The tex document as a unicode string.
    figs : dict
        A dictionary with figure names (without extension or directory)
        as the key and and values are dicts with keys: path, options and
        figure environment.
    naming : str
        Style for figure naming, (``'aastex'|'arxiv'|None``).
    format_priority : list
        List of figure file extensions, in order of preference to use in
        the final build.
    max_size : float
        Maximum size for a figure before converting it into a JPEG.
        If ``None``, no conversions are attempted.
    """
    for figname, fig in figs.iteritems():
        if len(fig['exts']) == 0:
            continue
        # get the priority graphics file type
        for ext in format_priority:
            if ext in fig['exts']:
                figsize = fig['size_mb'][fig['exts'].index(ext)]
                full_path = ".".join((os.path.splitext(fig['path'])[0], ext))
                break
        # copy fig to the build directory
        if naming == "aastex":
            install_path = os.path.join(
                install_dir,
                u"f{0:d}.{1}".format(fig['num'], ext))
        elif naming == "arxiv":
            install_path = os.path.join(
                install_dir,
                u"figure{0:d}.{1}".format(fig['num'], ext))
        else:
            install_path = os.path.join(
                install_dir,
                os.path.basename(full_path))
        figs[figname]["installed_path"] = install_path
        shutil.copy(full_path, install_path)
        if max_size and figsize > max_size:
            rasterize_figure(install_path)
        # update tex by replacing old filename with new.
        # Note that fig['env'] currently has escaped slash for re; this is
        # removed here. Might want to think of a convention so it's less kludgy
        old_fig_cmd = ur"{env}{opts}{{{path}}}".format(
            env=fig['env'].replace(u"\\\\", u"\\"),
            opts=fig['options'],
            path=fig['path'])
        new_fig_cmd = ur"{env}{opts}{{{path}}}".format(
            env=fig['env'].replace(u"\\\\", u"\\"),
            opts=fig['options'],
            path=os.path.basename(os.path.splitext(install_path)[0]))
        tex = tex.replace(old_fig_cmd, new_fig_cmd)
    return tex


def rasterize_figure(original_path):
    """Make a JPEG version of a figure, deleting the original."""
    jpg_path = os.path.splitext(original_path)[0] + ".jpg"
    subprocess.call(
        "convert -density 300 -trim -quality 80 {path} {jpgpath}".format(
            path=original_path, jpgpath=jpg_path),
        shell=True)
    os.remove(original_path)
