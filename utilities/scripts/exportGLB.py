"""Export .glb files for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/exportGLB.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/exportGLB.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger"). Only categories with
``pipeline: standard`` in their category.yml are handled here.
"""
import argparse
import os
import shutil
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from categories import (  # noqa: E402
    Category,
    PIPELINE_STANDARD,
    discover,
    filter_pipeline,
    repo_root,
    resolve,
)


def parse_args(argv, categories):
    parser = argparse.ArgumentParser(
        prog="exportGLB.py",
        description="Export .glb for one or more model categories.",
    )
    parser.add_argument(
        "categories",
        nargs="*",
        help="One or more categories. Aliases: " + ", ".join(sorted(categories)),
    )
    parser.add_argument("--all", action="store_true", help="Process every category.")
    args = parser.parse_args(argv)

    if args.all and args.categories:
        parser.error("--all cannot be combined with positional categories")
    if not args.all and not args.categories:
        parser.error("provide at least one category, or pass --all")

    if args.all:
        return list(categories.values())

    resolved: list[Category] = []
    seen: set[str] = set()
    for name in args.categories:
        try:
            cat = resolve(name, categories)
        except KeyError:
            parser.error(
                f"unknown category: {name!r}. Known: {', '.join(sorted(categories))}"
            )
        if cat.alias not in seen:
            resolved.append(cat)
            seen.add(cat.alias)
    return resolved


def export_category(repo, cat: Category) -> None:
    path_blend = os.path.join(repo, cat.directory, "blender")
    path_glb = os.path.join(repo, cat.directory, "glb")
    os.makedirs(path_glb, exist_ok=True)

    for blendfile in os.listdir(path_blend):
        current_file = os.path.join(path_blend, blendfile)
        bpy.ops.wm.open_mainfile(filepath=current_file)
        out_name = blendfile.replace(".blend", ".glb")
        bpy.ops.export_scene.gltf(
            export_format="GLB",
            filepath=os.path.join(path_glb, out_name),
        )

    texture_folder = os.path.join(repo, cat.directory, "textures")
    if os.path.isdir(texture_folder):
        dest = os.path.join(path_glb, "textures/")
        os.makedirs(dest, exist_ok=True)
        for file in os.listdir(texture_folder):
            shutil.copy2(os.path.join(texture_folder, file), dest)


def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    repo = repo_root()
    standard = filter_pipeline(discover(repo), PIPELINE_STANDARD)
    selected = parse_args(argv, standard)

    for cat in selected:
        print(f"[exportGLB] {cat.alias}")
        export_category(str(repo), cat)


if __name__ == "__main__":
    main()
