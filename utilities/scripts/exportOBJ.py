"""Export .obj/.mtl files for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/exportOBJ.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/exportOBJ.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger"). Only categories with
``pipeline: standard`` in their category.yml are handled here — the
Verkehrszeichen pipeline runs through its own dedicated scripts.
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
        prog="exportOBJ.py",
        description="Export .obj for one or more model categories.",
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
    path_obj = os.path.join(repo, cat.directory, "obj")
    os.makedirs(path_obj, exist_ok=True)

    for blendfile in os.listdir(path_blend):
        current_file = os.path.join(path_blend, blendfile)
        bpy.ops.wm.open_mainfile(filepath=current_file)
        out_name = blendfile.replace(".blend", ".obj")
        bpy.ops.wm.obj_export(
            filepath=os.path.join(path_obj, out_name),
            forward_axis="NEGATIVE_Y",
            up_axis="Z",
            export_materials=True,
            export_triangulated_mesh=cat.triangulate,
            path_mode="RELATIVE",
        )

    texture_folder = os.path.join(repo, cat.directory, "textures")
    if os.path.isdir(texture_folder):
        dest = os.path.join(path_obj, "textures/")
        os.makedirs(dest, exist_ok=True)
        for file in os.listdir(texture_folder):
            shutil.copy2(os.path.join(texture_folder, file), dest)

    # The default RELATIVE path_mode emits "../../textures/..." references
    # because Blender resolves them relative to the .blend file, which sits in
    # <Cat>/blender/. After we copy textures into <Cat>/obj/textures/, the
    # correct relative path from <Cat>/obj/ is just "../".
    for filename in os.listdir(path_obj):
        if not filename.endswith(".mtl"):
            continue
        mtl_path = os.path.join(path_obj, filename)
        with open(mtl_path, "rt") as f:
            data = f.read()
        data = data.replace("../../", "../")
        with open(mtl_path, "wt") as f:
            f.write(data)


def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    repo = repo_root()
    standard = filter_pipeline(discover(repo), PIPELINE_STANDARD)
    selected = parse_args(argv, standard)

    for cat in selected:
        print(f"[exportOBJ] {cat.alias}")
        export_category(str(repo), cat)


if __name__ == "__main__":
    main()
