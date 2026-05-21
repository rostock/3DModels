"""Export .obj/.mtl files for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/exportOBJ.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/exportOBJ.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger").

Note: Verkehrszeichen has its own pipeline (exportOBJ_Verkehrszeichen.py +
retextureOBJ_Verkehrszeichen.py) and is intentionally not handled here.
"""
import argparse
import os
import shutil
import sys

import bpy
import git

# alias -> {directory, triangulate}
# triangulate mirrors the historical per-category behaviour of the old
# exportOBJ_<Cat>.py scripts.
CATEGORIES = {
    "Abfallbehaelter": {"directory": "Abfallbehaelter", "triangulate": False},
    "Ampeln": {"directory": "Ampeln", "triangulate": True},
    "Ausleger": {"directory": "Beleuchtung_Ausleger", "triangulate": False},
    "Lampen": {"directory": "Beleuchtung_Lampen", "triangulate": False},
    "Masten": {"directory": "Beleuchtung_Masten", "triangulate": False},
    "Wandhalterung": {"directory": "Beleuchtung_Wandhalterung", "triangulate": True},
    "Werbeanlagen": {"directory": "Werbeanlagen", "triangulate": True},
}

# Accept either the alias or the full directory name as input.
ALIASES = {
    **{alias: alias for alias in CATEGORIES},
    **{cfg["directory"]: alias for alias, cfg in CATEGORIES.items()},
}


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="exportOBJ.py",
        description="Export .obj for one or more model categories.",
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
        return list(CATEGORIES.keys())

    resolved = []
    for name in args.categories:
        if name not in ALIASES:
            parser.error(
                f"unknown category: {name!r}. Known: {', '.join(sorted(ALIASES))}"
            )
        alias = ALIASES[name]
        if alias not in resolved:
            resolved.append(alias)
    return resolved


def export_category(repo_root, alias):
    cfg = CATEGORIES[alias]
    directory = cfg["directory"]
    triangulate = cfg["triangulate"]

    path_blend = os.path.join(repo_root, directory, "blender")
    path_obj = os.path.join(repo_root, directory, "obj")
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
            export_triangulated_mesh=triangulate,
            path_mode="RELATIVE",
        )

    texture_folder = os.path.join(repo_root, directory, "textures")
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
    # Blender forwards args after `--` to the script via sys.argv.
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    selected = parse_args(argv)
    repo_root = git.Repo(".", search_parent_directories=True).git.rev_parse(
        "--show-toplevel"
    )

    for alias in selected:
        print(f"[exportOBJ] {alias}")
        export_category(repo_root, alias)


if __name__ == "__main__":
    main()
