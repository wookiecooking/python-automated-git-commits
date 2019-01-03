import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from pprint import pprint
from git import *

path = sys.argv[1] if len(sys.argv) > 1 else '.'

g = Git(path)
repo = Repo(path)
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

class ChangeHandler(FileSystemEventHandler):

    # def on_any_event(self, event):
    #     if "./.git" not in event.src_path:
    #         if event.src_path != '.' and '.tmp' not in event.src_path:
    #             g.execute(["git", "add", "-A"])

    "When a file is deleted"
    def on_deleted(self, event):
        if ".git" not in event.src_path:
            if not event.is_directory:
                if event.src_path != '.' and '.tmp' not in event.src_path:
                    derp = g.execute(["git", "commit", "-am", '"deleted {0}"'.format(event.src_path)])
                    logging.info(derp)

    "When a file is modified"
    def on_modified(self, event):
        if ".git" not in event.src_path:
            if not event.is_directory:
                if event.src_path != '.' and '.tmp' not in event.src_path:
                    derp = g.execute(["git", "commit", "-am", '"modifed {0}"'.format(event.src_path)])
                    logging.info(derp)

    "When a file is moved"
    def on_moved(self, event):
        if ".git" not in event.src_path:
            if not event.is_directory:
                if event.src_path != '.' and '.tmp' not in event.src_path:
                    derp = g.execute(["git", "commit", "-am", '"moved  {0}"'.format(event.src_path[2:])])
                    logging.info(derp)
    "When a file is created"
    def on_created(self, event):
        if ".git" not in event.src_path:
            if event.src_path != '.' and '.tmp' not in event.src_path:
                derp = g.execute(["git", "add", "-A"])
                if not event.is_directory:
                    logging.info(derp)


def main():
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    main()