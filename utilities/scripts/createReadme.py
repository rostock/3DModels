"""Generate per-category readmes and the repo-root readme from categories.yml.

Usage (anywhere inside the repo):
    python createReadme.py Abfallbehaelter           # one category
    python createReadme.py Ampeln Lampen Werbeanlagen # several categories
    python createReadme.py --all                      # every category
    python createReadme.py --root                     # only the root readme
    python createReadme.py --all --root               # both

Categories can be passed either by short alias (e.g. "Ausleger") or by the
on-disk directory name (e.g. "Beleuchtung_Ausleger"). Both forms are accepted.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import git
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "categories.yml"
VIEWER_URL_TEMPLATE = (
    "https://3dviewer.net/embed.html#model="
    "https://github.com/rostock/3DModels/blob/main/{directory}/glb/{model}.glb"
    "$camera=0,0,0$cameramode=perspective"
    "$envsettings=fishermans_bastion,on"
    "$backgroundcolor=200,200,200,255$defaultcolor=200,200,200"
    "$edgesettings=off,0,0,0,20"
)


def load_categories() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def repo_root() -> Path:
    return Path(
        git.Repo(".", search_parent_directories=True).git.rev_parse("--show-toplevel")
    )


def resolve_category(name: str, categories: dict) -> str:
    """Accept either the alias or the on-disk directory name; return the alias."""
    if name in categories:
        return name
    for alias, cfg in categories.items():
        if cfg["directory"] == name:
            return alias
    raise SystemExit(f"Unknown category: {name!r}. Known: {sorted(categories)}")


def build_category_readme(alias: str, cfg: dict, root: Path) -> None:
    directory = cfg["directory"]
    display_name = cfg["display_name"]
    has_glb = cfg.get("has_glb", False)
    intro = cfg.get("intro", "").rstrip()

    thumbs_dir = root / directory / "thumbs"
    thumbs = sorted(os.listdir(thumbs_dir))

    if has_glb:
        table = "## Modelle \n | Modellname | Preview | 3D-Modell | \n | --- | --- | --- |\n"
    else:
        table = "## Modelle \n | Modellname | Preview | \n | --- | --- | \n"

    for thumb in thumbs:
        model = thumb.replace(".jpg", "")
        image = os.path.join("thumbs", thumb)
        if has_glb:
            viewer = VIEWER_URL_TEMPLATE.format(directory=directory, model=model)
            table += f"| {model} |![Image]({image})| [Link zu Online 3D Viewer]({viewer}) |\n"
        else:
            table += f"| {model} |![Image]({image})| \n"

    text = f"# {display_name}\n{intro}\n\n{table}"
    text = text.replace("\\", "/")

    out = root / directory / "README.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)


def build_root_readme(categories: dict, root: Path) -> None:
    beleuchtung = []
    others = []
    for cfg in categories.values():
        directory = cfg["directory"]
        display_name = cfg["display_name"]
        link = f"{directory}/README.md"
        entry = (display_name, link)
        if directory.startswith("Beleuchtung_"):
            beleuchtung.append(entry)
        else:
            others.append(entry)
    beleuchtung.sort()
    others.sort()

    text = "# 3D Modelle \n Dieses Repository enthält .OBJ und .GLB Modelle für: \n"
    if beleuchtung:
        text += "- Beleuchtung\n"
        for name, link in beleuchtung:
            text += f"   - [{name}]({link}) \n"
    for name, link in others:
        text += f"- [{name}]({link}) \n"

    with open(root / "README.md", "w", encoding="utf-8") as f:
        f.write(text)


def parse_args(argv: list[str], categories: dict) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "categories", nargs="*", help="Category aliases or directory names"
    )
    parser.add_argument(
        "--all", action="store_true", help="Process every category in categories.yml"
    )
    parser.add_argument(
        "--root", action="store_true", help="(Re)generate the repo-root README.md"
    )
    args = parser.parse_args(argv)

    if not args.all and not args.root and not args.categories:
        parser.error("specify one or more categories, --all, or --root")
    if args.all and args.categories:
        parser.error("--all is mutually exclusive with positional categories")
    return args


def main() -> None:
    categories = load_categories()
    args = parse_args(sys.argv[1:], categories)
    root = repo_root()

    if args.all:
        selected = list(categories)
    else:
        selected = []
        seen = set()
        for raw in args.categories:
            alias = resolve_category(raw, categories)
            if alias not in seen:
                selected.append(alias)
                seen.add(alias)

    for alias in selected:
        print(f"Building {alias}/README.md")
        build_category_readme(alias, categories[alias], root)

    if args.root:
        print("Building root README.md")
        build_root_readme(categories, root)


if __name__ == "__main__":
    main()
