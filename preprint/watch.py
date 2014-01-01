import logging
import os
import subprocess
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from cliff.command import Command


class Watch(Command):
    """Watch for changes and compile paper"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Watch, self).get_parser(prog_name)
        parser.add_argument('--exts',
            nargs='*',
            default=['tex', 'pdf', 'eps'],
            help="File extensions to look for")
        parser.add_argument('--cmd',
            default='make',
            help="Command to run on changes")
        return parser

    def take_action(self, parsed_args):
        self.log.debug('debugging')
        self.log.debug(str(parsed_args.exts))
        self.log.debug(self.app.options.master)
        ignore = (os.path.splitext(self.app.options.master)[0] + ".pdf",
                'build')
        self._watch(parsed_args.cmd, parsed_args.exts, ignore)

    def _watch(self, cmd, exts, ignore):
        handler = ChangeHandler(cmd, exts, ignore)
        observer = Observer()
        observer.schedule(handler, '.')
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class ChangeHandler(FileSystemEventHandler):
    """React to modified files."""
    def __init__(self, command, exts, ignores):
        super(ChangeHandler, self).__init__()
        self._cmd = command
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
                subprocess.call(self._cmd, shell=True)
        return
