# Optional: expose package version from metadata
try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("pyeva3dm")
    except PackageNotFoundError:
        __version__ = "0.0.0"
except Exception:  # py<3.8 fallback if you care
    __version__ = "0.0.0"

# Re-export the public API
from .stats import calculate_stats
__all__ = [
    "calculate_stats"
]
