import argparse
from pathlib import Path
import os
import glob
import shutil
import json


def convert_to_dir(file: Path):
    if file.stem == "index":
        print(f"{file} is already in dir structure.")
        return
    dir_name = file.stem
    dir_path = file.parent.joinpath(dir_name)
    try:
        dir_path.mkdir(exist_ok=False)
    except OSError:
        print(f"dir {dir_path} already exits.")
        return -2

    new_path = dir_path.joinpath("index" + file.suffix)
    shutil.move(file, new_path)


def have_front_matter(file: Path):
    if file.suffix == ".ipynb":
        import json

        c: dict = json.loads(file.read_text(encoding="utf8"))
        if "cells" not in c.keys():
            return False
        if len(c["cells"]) == 0:
            return False
        if c["cells"][0]["cell_type"] != "markdown":
            return False

        if "source" not in c["cells"][0].keys():
            return False
        first_cell_content = c["cells"][0]["source"]
        if not isinstance(first_cell_content, list) or len(first_cell_content) == 0:
            return False
        if first_cell_content[0] != "---\n" and first_cell_content[0] != "+++\n":
            return False

        return True


def fix_file(file: Path):
    if file.suffix == ".md":
        content = file.read_text(encoding="utf8")
        first_line = content.split("\n")[0]
        # check if already have front matter
        if first_line == "---" or first_line == "+++":
            return
        from .resource import content_md
        from .tools import get_title_from_path
        from .date import get_oldest_git_date

        title = get_title_from_path(file)
        date = get_oldest_git_date(file)

        content1 = content_md.replace("{date}", date).replace("{title}", title)
        file.write_text(content1 + content)

    if file.suffix == ".ipynb":
        if have_front_matter(file):
            return

        from .tools import get_title_from_path
        from .date import get_oldest_git_date

        title = get_title_from_path(file)
        date = get_oldest_git_date(file)
        from .resource import content_json

        content1 = content_json.replace("{date}", date).replace("{title}", title)
        content_obj = json.loads(content1)
        file_obj = json.loads(file.read_text(encoding="utf8"))
        file_obj["cells"].insert(0, content_obj)
        file.write_text(encoding="utf8", data=json.dumps(file_obj, indent=2))


def fix_file_glob(glob_str: str):
    base_dir = Path(os.getcwd())
    files = glob.glob(glob_str, root_dir=base_dir, recursive=True)
    for file in files:
        file_path = base_dir.joinpath(file)
        fix_file(file_path)


def convert_to_dir_glob(glob_str: str):
    base_dir = Path(os.getcwd())
    files = glob.glob(glob_str, root_dir=base_dir, recursive=True)
    for file in files:
        file_path = base_dir.joinpath(file)
        convert_to_dir(file_path)


def get_args():
    parser = argparse.ArgumentParser(
        usage="""
a tool to add front matter to ipynb/md files.

> hugo_fix ./content/*.ipynb
        convert ipynb to dir structure and add front matter.
> hugo_fix ./docs/*.md
        add front matter to markdown files (extracting datetime from git).
> hugo_fix --to-dir/-d ./docs/aaa.md | hugo_todir ./docs/aaa.md | hugo_todir ./docs/aaa.ipynb
        convert the file to dir structure.
"""
    )

    parser.add_argument("target_file", type=str, help="file path")
    parser.add_argument(
        "--to-dir",
        "-d",
        action="store_true",
        default=False,
        help="convert the file to directory",
    )

    args = parser.parse_args()
    return args


## entry points


def to_dir_main():
    args = get_args()
    args.to_dir = True
    main(args)


def fix_main():
    args = get_args()
    main(args)


# main proc
def main(args):
    if args.to_dir:
        fix_file_glob(args.target_file)
        convert_to_dir_glob(args.target_file)
    else:
        fix_file_glob(args.target_file)
