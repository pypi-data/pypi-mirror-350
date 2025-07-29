import glob
from pathlib import Path
import os


def must_find_hugo_root() -> Path:
    cwd = Path(os.getcwd())
    files = glob.glob("**/hugo.yaml", recursive=True, root_dir=cwd)
    if len(files) == 0:
        files = glob.glob("**/hugo.toml", recursive=True, root_dir=cwd)
        if len(files) == 0:
            print("cannot find a hugo site")
            exit(-1)
        else:
            from hugo_nbconvert.global_config import config

            config.set_toml()
    hugo_basedir = cwd.joinpath(files[0]).parent
    return hugo_basedir


def get_files() -> list[Path]:
    hugo_basedir = must_find_hugo_root()

    hugo_ipynbs = glob.glob("**/*.ipynb", recursive=True, root_dir=hugo_basedir)

    hugo_ipynbs = list(
        map(
            hugo_basedir.joinpath,
            filter(lambda x: not x.startswith("public"), hugo_ipynbs),
        )
    )
    return hugo_ipynbs
