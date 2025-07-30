"""
Backend-detection helpers (kept private).
"""

from importlib import import_module, metadata
from types import ModuleType
from ._typing import Provider

_CANDIDATES: tuple[tuple[Provider, str], ...] = (
    ("aws", "awswrangler"),
    ("gcp", "pandas_gbq"),  # module import name
)


def detect() -> Provider:
    found = [name for name, probe in _CANDIDATES if _is_importable(probe)]
    if not found:
        raise RuntimeError(
            "No provider libraries detected.\n"
            " · pip install pytadata_entriz[aws]   # S3 / Glue / Redshift\n"
            " · pip install pytadata_entriz[gcp]   # BigQuery"
        )
    if len(found) > 1:
        raise RuntimeError(
            "Multiple providers detected "
            f"({', '.join(found)}).  Please pin one explicitly."
        )
    return found[0]


def load_module(preferred: Provider | None = None) -> ModuleType:
    """
    Return `providers.aws` or `providers.gcp`, importing it lazily.
    """
    prov = preferred if preferred and preferred != "auto" else detect()
    if prov not in ("aws", "gcp", "local"):  # pragma: no cover
        raise ValueError(f"Unknown provider: {prov!r}")
    elif prov in ("aws", "gcp"):
        raise NotImplementedError(f"Provider {prov!r} is not implemented yet.")
    return import_module(f".providers.{prov}", package=__package__)


# ──────────────────────────────────────────────────────────────────
def _is_importable(name: str) -> bool:
    try:
        import_module(name)
        return True
    except ModuleNotFoundError:
        return False


def has_pkg(name: str) -> bool:
    """Expose to tests."""
    try:
        metadata.version(name)
        return True
    except metadata.PackageNotFoundError:  # pragma: no cover
        return False
