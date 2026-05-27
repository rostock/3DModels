"""Discover per-category configuration from <Cat>/category.yml files.

Each top-level repo directory that contains a ``category.yml`` is treated
as a model category. New categories therefore appear in the pipeline
without touching any script — drop the directory + ``category.yml`` into
the repo root and the next workflow run picks it up.

Schema (all fields except ``alias`` are optional):

    alias:         CLI short name. Defaults to the directory name.
    display_name:  H1 title in the per-category README. Defaults to alias.
    pipeline:      "standard" | "verkehrszeichen". Defaults to "standard".
    triangulate:   Whether exportOBJ should triangulate. Defaults to False.
    intro:         Markdown intro for the per-category README.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import git
import yaml

CONFIG_FILENAME = "category.yml"

PIPELINE_STANDARD = "standard"
PIPELINE_VERKEHRSZEICHEN = "verkehrszeichen"
KNOWN_PIPELINES = {PIPELINE_STANDARD, PIPELINE_VERKEHRSZEICHEN}


@dataclass(frozen=True)
class Category:
    alias: str
    directory: str
    display_name: str
    pipeline: str
    triangulate: bool
    intro: str


def repo_root() -> Path:
    return Path(
        git.Repo(".", search_parent_directories=True).git.rev_parse("--show-toplevel")
    )


def _load(cfg_path: Path, directory: str) -> Category:
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    pipeline = data.get("pipeline", PIPELINE_STANDARD)
    if pipeline not in KNOWN_PIPELINES:
        raise ValueError(
            f"{cfg_path}: unknown pipeline {pipeline!r}; "
            f"expected one of {sorted(KNOWN_PIPELINES)}"
        )

    alias = data.get("alias") or directory
    return Category(
        alias=alias,
        directory=directory,
        display_name=data.get("display_name") or alias,
        pipeline=pipeline,
        triangulate=bool(data.get("triangulate", False)),
        intro=(data.get("intro") or "").rstrip(),
    )


def discover(root: Path | None = None) -> dict[str, Category]:
    """Return ``alias -> Category`` for every directory containing category.yml.

    Sorted alphabetically by directory name.
    """
    if root is None:
        root = repo_root()
    found: dict[str, Category] = {}
    for entry in sorted(os.listdir(root)):
        cfg_path = root / entry / CONFIG_FILENAME
        if not cfg_path.is_file():
            continue
        category = _load(cfg_path, entry)
        if category.alias in found:
            other = found[category.alias].directory
            raise ValueError(
                f"Duplicate category alias {category.alias!r}: "
                f"{other} and {category.directory}"
            )
        found[category.alias] = category
    return found


def resolve(name: str, categories: dict[str, Category]) -> Category:
    """Accept either an alias or the on-disk directory name."""
    if name in categories:
        return categories[name]
    for cat in categories.values():
        if cat.directory == name:
            return cat
    raise KeyError(name)


def filter_pipeline(
    categories: dict[str, Category], pipeline: str
) -> dict[str, Category]:
    return {alias: cat for alias, cat in categories.items() if cat.pipeline == pipeline}
