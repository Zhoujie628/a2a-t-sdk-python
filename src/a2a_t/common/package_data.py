from __future__ import annotations

import sysconfig
from pathlib import Path


def resolve_package_data_dir(*, module_file: str | Path, source_package_data_parent_depth: int) -> Path:
    """Resolve the package data root for source checkouts and installed wheels."""
    module_path = Path(module_file).resolve()
    source_package_data_dir = module_path.parents[source_package_data_parent_depth] / "package_data"
    if source_package_data_dir.exists():
        return source_package_data_dir
    return Path(sysconfig.get_path("data")).resolve()
