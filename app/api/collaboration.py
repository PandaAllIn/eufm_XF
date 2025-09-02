"""Collaboration API endpoints for serving source files."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from flask import Blueprint, jsonify, request


collaboration_bp = Blueprint("collaboration", __name__, url_prefix="/api/collaboration")

BASE_DIR = Path(__file__).resolve().parents[2]
ALLOWED_ROOTS: List[Path] = [BASE_DIR / "docs", BASE_DIR / "app"]
ALLOWED_EXTENSIONS = {".md", ".py", ".txt", ".json", ".yaml", ".yml"}


def build_tree(path: Path) -> Dict[str, object]:
    """Recursively build a file tree rooted at ``path``."""

    node: Dict[str, object] = {
        "name": path.name,
        "path": str(path.relative_to(BASE_DIR)),
        "type": "directory" if path.is_dir() else "file",
    }

    if path.is_dir():
        node["children"] = [
            build_tree(child) for child in sorted(path.iterdir(), key=lambda p: p.name)
        ]

    return node


@collaboration_bp.get("/files")
def list_files():
    """Return a file tree for the docs and app directories."""

    tree = [build_tree(root) for root in ALLOWED_ROOTS if root.exists()]
    return jsonify(tree)


def _is_within_allowed_dirs(path: Path) -> bool:
    for root in ALLOWED_ROOTS:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


@collaboration_bp.get("/file")
def get_file():
    """Return the contents of a single file if it is allowed."""

    rel_path = request.args.get("path", "")
    if not rel_path:
        return jsonify({"error": "path query parameter required"}), 400

    target = (BASE_DIR / rel_path).resolve()
    if not _is_within_allowed_dirs(target):
        return jsonify({"error": "path not allowed"}), 400
    if target.suffix.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "file type not allowed"}), 400
    if not target.exists() or not target.is_file():
        return jsonify({"error": "file not found"}), 404

    content = target.read_text(encoding="utf-8")
    return jsonify({"path": rel_path, "content": content})
