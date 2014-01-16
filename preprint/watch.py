import logging
import os
import subprocess
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from cliff.command import Command

from preprint.latexdiff import git_diff_pipeline


class Watch(Command):
    """Watch for changes and compile paper"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Watch, self).get_parser(prog_name)
        parser.add_argument('--exts',
            nargs='*',
            default=self.app.confs.config('exts'),
            help="File extensions to look for")
        parser.add_argument('--cmd',
            default=self.app.confs.config('cmd'),
            help="Command to run on changes")
        parser.add_argument('--diff',
            nargs='?',
            const='HEAD',
            default=None,
            help="Typeset diff against git commit")
        return parser

    def take_action(self, parsed_args):
        ignore = (os.path.splitext(self.app.options.master)[0] + ".pdf",
            'build', '_current.tex', '_prev.tex')
        if parsed_args.diff is None:
            handler = RegularChangeHandler(parsed_args.cmd, parsed_args.exts,
                    ignore)
        else:
            handler = DiffChangeHandler(self.app.options.master,
                    parsed_args.diff, parsed_args.exts, ignore)
        self._watch(handler)

    def _watch(self, handler):
        observer = Observer()
        observer.schedule(handler, '.')
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class BaseChangeHandler(FileSystemEventHandler):
    """React to modified files."""
    def __init__(self, exts, ignores):
        super(BaseChangeHandler, self).__init__()
        self._exts = exts
        self._ignores = ignores

    def on_any_event(self, event):
        """If a file or folder is changed."""
        if event.is_directory:
            return
        else:
            event_ext = os.path.splitext(event.src_path)[-1]\
                .lower().lstrip('.')
            if event_ext in self._exts:
                for ig in self._ignores:
                    if ig in event.src_path:
                        return
                # passed all tests
                self.run_compile()
        return


class RegularChangeHandler(BaseChangeHandler):
    """Class for reacting to modified files and doing a regular compile."""
    def __init__(self, command, exts, ignores):
        super(RegularChangeHandler, self).__init__(exts, ignores)
        self._cmd = command

    def run_compile(self):
        """Run a compilation."""
        subprocess.call(self._cmd, shell=True)


class DiffChangeHandler(BaseChangeHandler):
    """React to modified files while building latexdiffs."""
    def __init__(self, master_path, prev_commit, exts, ignores):
        super(DiffChangeHandler, self).__init__(exts, ignores)
        self._master = master_path
        self._prev_commit = prev_commit
        self._output_name = "{0}_diff".format(
                os.path.splitext(self._master)[0])
        # Hack the ignore list to include the output path
        self._ignores = list(ignores)
        self._ignores.append(self._output_name)

    def run_compile(self):
        """Run a latexdiff+compile."""
        git_diff_pipeline(self._output_name, self._master,
            self._prev_commit)
