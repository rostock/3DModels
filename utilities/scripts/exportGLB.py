"""Export .glb files for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/exportGLB.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/exportGLB.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger").
"""
import argparse
import os
import shutil
import sys

import bpy
import git

# alias -> on-disk directory name
CATEGORIES = {
    "Abfallbehaelter": "Abfallbehaelter",
    "Ampeln": "Ampeln",
    "Ausleger": "Beleuchtung_Ausleger",
    "Lampen": "Beleuchtung_Lampen",
    "Masten": "Beleuchtung_Masten",
    "Wandhalterung": "Beleuchtung_Wandhalterung",
    "Werbeanlagen": "Werbeanlagen",
}

# Accept either the alias or the full directory name as input.
ALIASES = {**CATEGORIES, **{v: v for v in CATEGORIES.values()}}


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="exportGLB.py",
        description="Export .glb for one or more model categories.",
    )
    parser.add_argument(
        "categories",
        nargs="*",
        help="One or more categories. Aliases: " + ", ".join(sorted(CATEGORIES)),
    )
    parser.add_argument("--all", action="store_true", help="Process every category.")
    args = parser.parse_args(argv)

    if args.all and args.categories:
        parser.error("--all cannot be combined with positional categories")
    if not args.all and not args.categories:
        parser.error("provide at least one category, or pass --all")

    if args.all:
        # Use CATEGORIES.values() so order matches definition order.
        return list(dict.fromkeys(CATEGORIES.values()))

    resolved = []
    for name in args.categories:
        if name not in ALIASES:
            parser.error(
                f"unknown category: {name!r}. Known: {', '.join(sorted(ALIASES))}"
            )
        directory = ALIASES[name]
        if directory not in resolved:
            resolved.append(directory)
    return resolved


def export_category(repo_root, category):
    path_blend = os.path.join(repo_root, category, "blender")
    path_glb = os.path.join(repo_root, category, "glb")
    os.makedirs(path_glb, exist_ok=True)

    for blendfile in os.listdir(path_blend):
        current_file = os.path.join(path_blend, blendfile)
        bpy.ops.wm.open_mainfile(filepath=current_file)
        out_name = blendfile.replace(".blend", ".glb")
        bpy.ops.export_scene.gltf(
            export_format="GLB",
            filepath=os.path.join(path_glb, out_name),
        )

    texture_folder = os.path.join(repo_root, category, "textures")
    if os.path.isdir(texture_folder):
        dest = os.path.join(path_glb, "textures/")
        os.makedirs(dest, exist_ok=True)
        for file in os.listdir(texture_folder):
            shutil.copy2(os.path.join(texture_folder, file), dest)


def main():
    # Blender forwards args after `--` to the script via sys.argv.
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    selected = parse_args(argv)
    repo_root = git.Repo(".", search_parent_directories=True).git.rev_parse(
        "--show-toplevel"
    )

    for category in selected:
        print(f"[exportGLB] {category}")
        export_category(repo_root, category)


if __name__ == "__main__":
    main()
