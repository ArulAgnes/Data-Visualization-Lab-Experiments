"""Shared plotting helpers used by both the notebook and the CLI runner.

Every figure produced by the experiment is:

* displayed (notebook) or closed (script mode),
* saved as a high-resolution (300 dpi) PNG inside ``outputs/plots``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from .data_loader import ensure_output_dirs, find_project_root, outputs_dir

DEFAULT_DPI = 300
PLOT_DIR_NAME = Path("outputs") / "plots"


def apply_style() -> None:
    """Apply one consistent, readable style to every figure."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "savefig.dpi": DEFAULT_DPI,
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
            "axes.grid": True,
            "grid.alpha": 0.3,
        }
    )


def new_figure(figsize: tuple = (8, 5)):
    """Create a fresh figure with the shared style applied."""
    apply_style()
    return plt.figure(figsize=figsize)


def subplots(nrows: int = 1, ncols: int = 1, figsize: Optional[tuple] = None):
    """``plt.subplots`` wrapper that first applies the shared style."""
    apply_style()
    if figsize is None:
        figsize = (5 * ncols, 4 * nrows)
    return plt.subplots(nrows, ncols, figsize=figsize)


def save_figure(
    fig,
    name: str,
    root: Optional[Path] = None,
    subfolder: str = "plots",
    dpi: int = DEFAULT_DPI,
) -> Path:
    """Save ``fig`` as ``outputs/<subfolder>/<name>.png`` and return the path.

    The function is idempotent: re-running the experiment overwrites the old
    file instead of creating duplicates.
    """
    root = Path(root) if root is not None else find_project_root()
    target_dir = outputs_dir(root) / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)
    if not name.lower().endswith(".png"):
        name = f"{name}.png"
    path = target_dir / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    return path


def finish(fig=None, save_path: Optional[Path] = None, show: bool = True) -> Optional[Path]:
    """Convenience wrapper: save (if asked), display, then close the figure.

    ``show=False`` is used by the command line runner so that no GUI window
    is opened when the script runs on a server.
    """
    if fig is None:
        fig = plt.gcf()
    fig.tight_layout()
    if save_path is not None:
        fig.savefig(save_path, dpi=DEFAULT_DPI, bbox_inches="tight", facecolor="white")
    if show:
        try:
            plt.show()
        except Exception:  # pragma: no cover - headless environments
            pass
    else:
        plt.close(fig)
    return save_path
