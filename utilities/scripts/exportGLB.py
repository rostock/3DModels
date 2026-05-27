"""Export .glb files for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/exportGLB.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/exportGLB.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger").

Categories with ``pipeline: verkehrszeichen`` are exported by importing each
fan-out .obj from <Cat>/obj/ and writing the result as .glb, so the
``exportOBJ_Verkehrszeichen.py`` + ``retextureOBJ_Verkehrszeichen.py`` steps
must have run first.
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
    PIPELINE_VERKEHRSZEICHEN,
    discover,
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


def export_from_blend(repo, cat: Category) -> None:
    """Open each .blend in <Cat>/blender/ and export it as .glb."""
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


def export_verkehrszeichen(repo, cat: Category) -> None:
    """Import each .obj from <Cat>/obj/ and export it as .glb.

    Textures are embedded in the GLB, so no external textures/ folder
    is copied next to the .glb files.
    """
    obj_dir = os.path.join(repo, cat.directory, "obj")
    glb_dir = os.path.join(repo, cat.directory, "glb")
    os.makedirs(glb_dir, exist_ok=True)

    for obj in os.listdir(obj_dir):
        if not obj.endswith(".obj"):
            continue
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.wm.obj_import(filepath=os.path.join(obj_dir, obj), forward_axis="Y")
        out_name = obj.replace(".obj", ".glb")
        bpy.ops.export_scene.gltf(
            export_format="GLB",
            filepath=os.path.join(glb_dir, out_name),
        )


EXPORTERS = {
    PIPELINE_STANDARD: export_from_blend,
    PIPELINE_VERKEHRSZEICHEN: export_verkehrszeichen,
}


def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    repo = repo_root()
    selected = parse_args(argv, discover(repo))

    for cat in selected:
        print(f"[exportGLB] {cat.alias} ({cat.pipeline})")
        EXPORTERS[cat.pipeline](str(repo), cat)


if __name__ == "__main__":
    main()
