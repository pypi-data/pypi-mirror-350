from pathlib import Path


def get_title_from_path(p: Path) -> str:
    last_path = p.stem
    name2 = last_path.split("-")
    title = " ".join(map(str.title, name2))
    return title


def get_title_from_stem(stem_name: str) -> str:
    name2 = stem_name.split("-")
    title = " ".join(map(str.title, name2))
    return title
