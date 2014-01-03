#!/usr/bin/env python
# encoding: utf-8
"""
Command for running latexdiff.
"""

import logging
import os
import subprocess
import codecs
import git

from preprint.inline import inline, inline_blob, read_git_blob

from cliff.command import Command


class Diff(Command):
    """Run latexdiff between HEAD and a git ref."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Diff, self).get_parser(prog_name)
        parser.add_argument('prev_commit',
            help="Commit SHA to compare HEAD against.")
        parser.add_argument('-n', '--name',
            default="diff",
            help="Name of the difference file.")
        return parser

    def take_action(self, parsed_args):
        # Inline current and previous versions of the document
        current_path = self._inline_current(self.app.options.master)
        prev_path = self._inline_prev(parsed_args.prev_commit,
                self.app.options.master)

        # Run latexmk
        diff_path = os.path.splitext(parsed_args.name)[0]
        ldiff_cmd = "latexdiff {prev} {current} > {diff}.tex".format(
                prev=prev_path,
                current=current_path,
                diff=diff_path)
        subprocess.call(ldiff_cmd, shell=True)

        # Compile the diff document with latexmk
        ltmk_cmd = "latexmk -f -pdf -bibtex-cond -c -gg {0}.tex".format(
                diff_path)
        subprocess.call(ltmk_cmd, shell=True)

    def _inline_current(self, root_tex):
        """Inline the current manuscript."""
        with codecs.open(root_tex, 'r', encoding='utf-8') as f:
            root_text = f.read()
            root_text = inline(root_text)
        output_path = "_current.tex"
        if os.path.exists(output_path):
            os.remove(output_path)
        with codecs.open(output_path, 'w', encoding='utf-8') as f:
            f.write(root_text)
        return output_path

    def _inline_prev(self, commit_ref, root_tex):
        """Inline the previous manuscript in the git tree."""
        root_text = read_git_blob(commit_ref, root_tex)
        root_text = inline_blob(commit_ref, root_text)
        output_path = "_prev.tex"
        if os.path.exists(output_path):
            os.remove(output_path)
        with codecs.open(output_path, 'w', encoding='utf-8') as f:
            f.write(root_text)
        return output_path

    def _get_n_commits(self):
        """docstring for _get_n_commits"""
        repo = git.Repo(".")
        print "HEAD", repo.head.commit.hexsha
        commits = list(repo.iter_commits())
        n = len(commits)
        return n

    def _get_commits(self):
        """docstring for _get_commits"""
        repo = git.Repo(".")
        commits = list(repo.iter_commits())
        # for cm in commits:
        #     print cm.committed_date, cm.hexsha
        return commits

    def _match_commit(self, sha):
        """Match the sha fragment to a commit."""
        commits = self._get_commits()
        for cm in commits:
            if cm.hexsha.startswith(sha):
                print sha, "match", cm.hexsha
                return cm
        return None
