"""Render 250x250 Cycles JPEG thumbnails for one or more model categories.

Usage (inside Blender):
    blender --background --python utilities/scripts/renderThumbnail.py -- <category> [<category> ...]
    blender --background --python utilities/scripts/renderThumbnail.py -- --all

Categories may be passed either as the alias (e.g. "Ausleger") or as the
on-disk directory name (e.g. "Beleuchtung_Ausleger").

Categories with ``pipeline: verkehrszeichen`` are rendered by importing each
fan-out .obj from <Cat>/obj/ into utilities/default.blend, so the
``exportOBJ_Verkehrszeichen.py`` + ``retextureOBJ_Verkehrszeichen.py`` steps
must have run first.
"""
import argparse
import os
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

RESOLUTION = 250
CYCLES_SAMPLES = 64


def parse_args(argv, categories):
    parser = argparse.ArgumentParser(
        prog="renderThumbnail.py",
        description="Render thumbnails for one or more model categories.",
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


def configure_render(output_path):
    bpy.context.scene.render.image_settings.file_format = "JPEG"
    bpy.context.scene.render.filepath = output_path
    scene = bpy.data.scenes["Scene"]
    scene.render.engine = "CYCLES"
    scene.cycles.samples = CYCLES_SAMPLES
    scene.render.resolution_x = RESOLUTION
    scene.render.resolution_y = RESOLUTION


def render_from_blend(repo, cat: Category) -> None:
    """Open each .blend in <Cat>/blender/ and render its current scene."""
    path_blend = os.path.join(repo, cat.directory, "blender")
    out_dir = os.path.join(repo, cat.directory, "thumbs")
    os.makedirs(out_dir, exist_ok=True)

    for blendfile in os.listdir(path_blend):
        current_file = os.path.join(path_blend, blendfile)
        bpy.ops.wm.open_mainfile(filepath=current_file)
        out_name = blendfile.replace(".blend", ".jpg").replace(" ", "_")
        configure_render(os.path.join(out_dir, out_name))
        bpy.ops.render.render(use_viewport=True, write_still=True)


def render_verkehrszeichen(repo, cat: Category) -> None:
    """Import each .obj from <Cat>/obj/ into utilities/default.blend and render."""
    obj_dir = os.path.join(repo, cat.directory, "obj")
    out_dir = os.path.join(repo, cat.directory, "thumbs")
    os.makedirs(out_dir, exist_ok=True)
    default_blend = os.path.join(repo, "utilities", "default.blend")

    for obj in os.listdir(obj_dir):
        if not obj.endswith(".obj"):
            continue
        bpy.ops.wm.open_mainfile(filepath=default_blend)
        bpy.ops.wm.obj_import(filepath=os.path.join(obj_dir, obj), forward_axis="Y")
        bpy.ops.view3d.camera_to_view_selected()
        bpy.data.cameras["Camera"].lens = 100
        configure_render(os.path.join(out_dir, obj.replace(".obj", ".jpg")))
        bpy.ops.render.render(use_viewport=True, write_still=True)


RENDERERS = {
    PIPELINE_STANDARD: render_from_blend,
    PIPELINE_VERKEHRSZEICHEN: render_verkehrszeichen,
}


def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = sys.argv[1:]

    repo = repo_root()
    selected = parse_args(argv, discover(repo))

    for cat in selected:
        print(f"[renderThumbnail] {cat.alias} ({cat.pipeline})")
        RENDERERS[cat.pipeline](str(repo), cat)


if __name__ == "__main__":
    main()
