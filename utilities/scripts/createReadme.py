"""Generate per-category READMEs and the repo-root README from category.yml files.

Usage (anywhere inside the repo):
    python createReadme.py Abfallbehaelter            # one category
    python createReadme.py Ampeln Lampen Werbeanlagen # several categories
    python createReadme.py --all                      # every category
    python createReadme.py --root                     # only the root README
    python createReadme.py --all --root               # both

Categories can be passed either by short alias (e.g. "Ausleger") or by the
on-disk directory name (e.g. "Beleuchtung_Ausleger"). Both forms are accepted.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from categories import Category, discover, repo_root, resolve  # noqa: E402

VIEWER_URL_TEMPLATE = (
    "https://3dviewer.net/embed.html#model="
    "https://github.com/rostock/3DModels/blob/main/{directory}/glb/{model}.glb"
    "$camera=0,0,0$cameramode=perspective"
    "$envsettings=fishermans_bastion,on"
    "$backgroundcolor=200,200,200,255$defaultcolor=200,200,200"
    "$edgesettings=off,0,0,0,20"
)


def build_category_readme(cat: Category, root: Path) -> None:
    thumbs_dir = root / cat.directory / "thumbs"
    thumbs = sorted(os.listdir(thumbs_dir))

    if cat.has_glb:
        table = "## Modelle \n | Modellname | Preview | 3D-Modell | \n | --- | --- | --- |\n"
    else:
        table = "## Modelle \n | Modellname | Preview | \n | --- | --- | \n"

    for thumb in thumbs:
        model = thumb.replace(".jpg", "")
        image = os.path.join("thumbs", thumb)
        if cat.has_glb:
            viewer = VIEWER_URL_TEMPLATE.format(directory=cat.directory, model=model)
            table += (
                f"| {model} |![Image]({image})|"
                f" [Link zu Online 3D Viewer]({viewer}) |\n"
            )
        else:
            table += f"| {model} |![Image]({image})| \n"

    text = f"# {cat.display_name}\n{cat.intro}\n\n{table}"
    text = text.replace("\\", "/")

    out = root / cat.directory / "README.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)


def build_root_readme(categories: dict[str, Category], root: Path) -> None:
    beleuchtung: list[tuple[str, str]] = []
    others: list[tuple[str, str]] = []
    for cat in categories.values():
        link = f"{cat.directory}/README.md"
        entry = (cat.display_name, link)
        if cat.directory.startswith("Beleuchtung_"):
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


def parse_args(argv: list[str], categories: dict[str, Category]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "categories", nargs="*", help="Category aliases or directory names"
    )
    parser.add_argument(
        "--all", action="store_true", help="Process every discovered category"
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
    root = repo_root()
    categories = discover(root)
    args = parse_args(sys.argv[1:], categories)

    if args.all:
        selected = list(categories.values())
    else:
        selected = []
        seen: set[str] = set()
        for raw in args.categories:
            try:
                cat = resolve(raw, categories)
            except KeyError:
                raise SystemExit(
                    f"Unknown category: {raw!r}. Known: {sorted(categories)}"
                )
            if cat.alias not in seen:
                selected.append(cat)
                seen.add(cat.alias)

    for cat in selected:
        print(f"Building {cat.directory}/README.md")
        build_category_readme(cat, root)

    if args.root:
        print("Building root README.md")
        build_root_readme(categories, root)


if __name__ == "__main__":
    main()
