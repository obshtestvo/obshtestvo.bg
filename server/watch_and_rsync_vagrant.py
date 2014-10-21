import sys
import time
import subprocess
from threading import Timer

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class RsyncEventHandler(PatternMatchingEventHandler):
    rsync_command = [
        'rsync',
        '--archive',
        '--verbose',
        '--exclude',
        '.git/',
        '--exclude',
        '.idea/',
        '--include',
        '*/',
        '--include',
        '/*/migrations/***',
        '--include',
        '/*/static/libs/***',
        '--exclude',
        '*',
    ]

    def __init__(self, from_path=None, to_path=None):
        super(RsyncEventHandler, self).__init__(patterns=['*/static/libs', '*/migrations/*'])
        self.rsync_command.append(from_path)
        self.rsync_command.append(to_path)
        self._debounce()

    def _debounce(self):
        if hasattr(self, 'timer'):
            self.timer.cancel()
        self.timer = Timer(0.5, self.rsync)
        self.timer.start()

    def rsync(self):
        print ' '.join(self.rsync_command)
        subprocess.Popen(self.rsync_command)

    def on_modified(self, event):
        self._debounce()

if __name__ == "__main__":
    from_path = sys.argv[1]
    to_path = sys.argv[2]
    observer = Observer()
    event_handler = RsyncEventHandler(from_path, to_path)
    observer.schedule(event_handler, from_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()