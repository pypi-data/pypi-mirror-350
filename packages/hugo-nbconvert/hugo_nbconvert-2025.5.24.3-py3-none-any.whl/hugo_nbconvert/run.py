from .glob_hugo_ipynb import must_find_hugo_root
import subprocess
from sodatools import CD, Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyEventHandler(FileSystemEventHandler):
    """Handles file system events, specifically Krita file changes."""

    def __init__(self, posts_path):
        super().__init__()
        self.posts_path = posts_path

    def on_modified(self, event):
        src_path = Path(event.src_path)
        if not event.is_directory:
            if src_path.suffix == ".ipynb":
                from .main import api_convert_main

                api_convert_main([src_path])


def run():
    root = must_find_hugo_root()
    print(f"using hugo root at {root}")

    # build a round first
    from .main import main

    main()

    # watch for ipynb changes
    post_root = root.joinpath("content")
    event_handler = MyEventHandler(post_root)
    observer = Observer()
    observer.schedule(event_handler, post_root, recursive=True)
    observer.start()

    try:
        with CD(root):
            try:
                subprocess.run("hugo serve -OD --baseURL=http://localhost", shell=True)
            except KeyboardInterrupt:
                raise
    finally:
        observer.stop()
        observer.join()
