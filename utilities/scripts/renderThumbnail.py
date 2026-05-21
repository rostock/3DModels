"""Render 250x250 Cycles JPEG thumbnails for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/renderThumbnail.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/renderThumbnail.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger").

Verkehrszeichen is a special case: its thumbnails are rendered by importing
each fan-out .obj from Verkehrszeichen/obj/ into utilities/default.blend,
so it requires `exportOBJ_Verkehrszeichen.py` + `retextureOBJ_Verkehrszeichen.py`
to have run first.
"""
import argparse
import os
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
    "Verkehrszeichen": "Verkehrszeichen",
    "Werbeanlagen": "Werbeanlagen",
}

ALIASES = {**CATEGORIES, **{v: v for v in CATEGORIES.values()}}

RESOLUTION = 250
CYCLES_SAMPLES = 64


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="renderThumbnail.py",
        description="Render thumbnails for one or more model categories.",
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


def configure_render(output_path):
    bpy.context.scene.render.image_settings.file_format = "JPEG"
    bpy.context.scene.render.filepath = output_path
    scene = bpy.data.scenes["Scene"]
    scene.render.engine = "CYCLES"
    scene.cycles.samples = CYCLES_SAMPLES
    scene.render.resolution_x = RESOLUTION
    scene.render.resolution_y = RESOLUTION


def render_from_blend(repo_root, category):
    """Open each .blend in <category>/blender/ and render its current scene."""
    path_blend = os.path.join(repo_root, category, "blender")
    out_dir = os.path.join(repo_root, category, "thumbs")
    os.makedirs(out_dir, exist_ok=True)

    for blendfile in os.listdir(path_blend):
        current_file = os.path.join(path_blend, blendfile)
        bpy.ops.wm.open_mainfile(filepath=current_file)
        out_name = blendfile.replace(".blend", ".jpg").replace(" ", "_")
        configure_render(os.path.join(out_dir, out_name))
        bpy.ops.render.render(use_viewport=True, write_still=True)


def render_verkehrszeichen(repo_root):
    """Import each .obj from Verkehrszeichen/obj/ into utilities/default.blend and render."""
    category = "Verkehrszeichen"
    obj_dir = os.path.join(repo_root, category, "obj")
    out_dir = os.path.join(repo_root, category, "thumbs")
    os.makedirs(out_dir, exist_ok=True)
    default_blend = os.path.join(repo_root, "utilities", "default.blend")

    for obj in os.listdir(obj_dir):
        if not obj.endswith(".obj"):
            continue
        bpy.ops.wm.open_mainfile(filepath=default_blend)
        bpy.ops.wm.obj_import(
            filepath=os.path.join(obj_dir, obj), forward_axis="Y"
        )
        # Frame the imported object, then zoom in slightly.
        bpy.ops.view3d.camera_to_view_selected()
        bpy.data.cameras["Camera"].lens = 100
        configure_render(os.path.join(out_dir, obj.replace(".obj", ".jpg")))
        bpy.ops.render.render(use_viewport=True, write_still=True)


def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    selected = parse_args(argv)
    repo_root = git.Repo(".", search_parent_directories=True).git.rev_parse(
        "--show-toplevel"
    )

    for category in selected:
        print(f"[renderThumbnail] {category}")
        if category == "Verkehrszeichen":
            render_verkehrszeichen(repo_root)
        else:
            render_from_blend(repo_root, category)


if __name__ == "__main__":
    main()
