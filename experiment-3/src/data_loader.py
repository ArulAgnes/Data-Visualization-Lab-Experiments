"""Dataset loading, environment detection and path handling.

The loader works in four environments without hard-coding any machine
specific path:

* local development  -> ``data/raw/<file>.csv`` (relative to the project root)
* Google Colab        -> ``files.upload()`` or an explicit Google Drive path
* Kaggle notebooks    -> ``/kaggle/input/<slug>/...`` and ``/kaggle/working``
* command line        -> ``python src/run_eda.py --data path/to/file.csv``

Secrets (Kaggle API tokens) are only *detected*, never printed.
"""

from __future__ import annotations

import logging
import os
import platform
import sys
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd
from pandas.errors import EmptyDataError

LOGGER = logging.getLogger(__name__)

DEFAULT_DATASET = Path("data") / "raw" / "penguins.csv"
KAGGLE_INPUT_ROOT = Path("/kaggle/input")
KAGGLE_WORKING_ROOT = Path("/kaggle/working")
DATA_ENV_VAR = "EDA_DATASET_PATH"
KAGGLE_SLUG_ENV_VAR = "EDA_KAGGLE_DATASET"


# --------------------------------------------------------------------------- #
# Environment detection
# --------------------------------------------------------------------------- #
def is_colab() -> bool:
    """Return ``True`` when running inside Google Colab."""
    try:
        import google.colab  # type: ignore  # noqa: F401

        return True
    except Exception:
        return False


def is_kaggle() -> bool:
    """Return ``True`` when running inside a Kaggle notebook/kernel."""
    return Path("/kaggle/input").exists() or os.environ.get("KAGGLE_KERNEL_RUN_TYPE") is not None


def describe_environment() -> dict:
    """Collect information about the current execution environment."""
    info = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "working_directory": str(Path.cwd()),
        "google_colab": is_colab(),
        "kaggle": is_kaggle(),
        "libraries": {},
    }
    for name in ("pandas", "numpy", "matplotlib", "seaborn", "scipy", "sklearn"):
        try:
            module = __import__(name)
            info["libraries"][name] = getattr(module, "__version__", "unknown")
        except Exception as exc:  # pragma: no cover - defensive
            info["libraries"][name] = f"not available ({exc.__class__.__name__})"
    return info


def kaggle_credentials_available() -> bool:
    """Check Kaggle credentials without ever displaying their content.

    Looks for ``~/.kaggle/kaggle.json`` or the ``KAGGLE_USERNAME`` /
    ``KAGGLE_KEY`` environment variables. Only a boolean is returned.
    """
    cred_file = Path.home() / ".kaggle" / "kaggle.json"
    if cred_file.is_file():
        return True
    return bool(os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"))


# --------------------------------------------------------------------------- #
# Project paths
# --------------------------------------------------------------------------- #
def find_project_root(start: Optional[Path] = None) -> Path:
    """Walk upwards until a folder containing both ``src/`` and ``data/`` is found.

    Falls back to the current working directory so the code never breaks in
    environments (Colab / Kaggle) where the classic layout was not created.
    """
    start = Path(start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "src").is_dir() and (candidate / "data").is_dir():
            return candidate
    return start


_OUTPUTS_DIRNAME = "outputs"


def set_outputs_dirname(name: str) -> None:
    """Choose the folder (relative to the project root) that holds all artefacts.

    Used by ``src/run_eda.py --output <folder>``; defaults to ``outputs``.
    An absolute path is used as-is.
    """
    global _OUTPUTS_DIRNAME
    _OUTPUTS_DIRNAME = str(name) or "outputs"


def outputs_dir(root: Path) -> Path:
    """``<project root>/<outputs folder>`` - honouring :func:`set_outputs_dirname`."""
    candidate = Path(_OUTPUTS_DIRNAME)
    return candidate if candidate.is_absolute() else Path(root) / candidate


def ensure_output_dirs(root: Optional[Path] = None) -> dict:
    """Create (idempotently) every output directory used by the experiment."""
    root = Path(root) if root is not None else find_project_root()
    plots_root = outputs_dir(root)
    dirs = {
        "root": root,
        "data_raw": root / "data" / "raw",
        "data_processed": root / "data" / "processed",
        "plots": plots_root / "plots",
        "reports": plots_root / "reports",
        "logs": plots_root / "logs",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


# --------------------------------------------------------------------------- #
# Dataset discovery
# --------------------------------------------------------------------------- #
def find_kaggle_input(slug: Optional[str] = None) -> Optional[Path]:
    """Locate a CSV inside ``/kaggle/input``.

    ``slug`` may be supplied through ``--kaggle-dataset`` or the
    ``EDA_KAGGLE_DATASET`` environment variable (e.g. ``owner/dataset-name``).
    When no slug is given, the first mounted CSV is used.
    """
    if not KAGGLE_INPUT_ROOT.exists():
        return None
    slug = slug or os.environ.get(KAGGLE_SLUG_ENV_VAR)
    search_roots: list[Path] = []
    if slug:
        # accept both "owner/slug" and "slug"
        folder = slug.split("/")[-1]
        candidate = KAGGLE_INPUT_ROOT / folder
        if candidate.is_dir():
            search_roots.append(candidate)
        else:
            LOGGER.warning("Kaggle input folder for slug '%s' not found.", slug)
    search_roots.append(KAGGLE_INPUT_ROOT)

    for search_root in search_roots:
        csv_files = sorted(p for p in search_root.rglob("*.csv") if p.is_file())
        if csv_files:
            return csv_files[0]
    return None


def _upload_csv_via_colab() -> Optional[Path]:
    """Ask the Colab user to upload a CSV (only when nothing else is configured)."""
    try:
        from google.colab import files  # type: ignore
    except Exception:
        LOGGER.warning("google.colab is unavailable - cannot upload a file.")
        return None
    print("No dataset path configured. Please upload a CSV file (e.g. penguins.csv):")
    uploaded = files.upload()
    if not uploaded:
        return None
    target_dir = ensure_output_dirs()["data_raw"]
    for name in uploaded:
        target = target_dir / name
        target.write_bytes(uploaded[name])
        print(f"Saved uploaded file to {target}")
        return target
    return None


def resolve_dataset_path(
    path: Optional[str | Path] = None,
    root: Optional[Path] = None,
    allow_upload: bool = True,
) -> Path:
    """Resolve the dataset path using the documented precedence order.

    1. explicit ``path`` argument (``--data`` on the command line)
    2. ``EDA_DATASET_PATH`` environment variable
    3. default project file ``data/raw/penguins.csv``
    4. mounted Kaggle input (``/kaggle/input``)
    5. Google Colab interactive upload (only if nothing else worked)

    Raises ``FileNotFoundError`` with a helpful message when no dataset
    can be resolved.
    """
    root = Path(root) if root is not None else find_project_root()

    if path:
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            candidate = (root / candidate) if not candidate.exists() else candidate
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(
            f"Dataset not found: '{path}'.\n"
            "Supply an existing CSV file, e.g.\n"
            "    python src/run_eda.py --data data/raw/penguins.csv"
        )

    env_path = os.environ.get(DATA_ENV_VAR)
    if env_path:
        candidate = Path(env_path).expanduser()
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(
            f"Environment variable {DATA_ENV_VAR} points to '{env_path}', which does not exist."
        )

    default_path = root / DEFAULT_DATASET
    if default_path.is_file():
        return default_path

    kaggle_path = find_kaggle_input()
    if kaggle_path is not None:
        LOGGER.info("Using Kaggle input dataset: %s", kaggle_path)
        return kaggle_path

    if allow_upload and is_colab():
        uploaded = _upload_csv_via_colab()
        if uploaded is not None:
            return uploaded

    raise FileNotFoundError(
        "No dataset found.\n"
        "Ways to provide one:\n"
        f"  1. Place a CSV at '{DEFAULT_DATASET}' relative to the project root\n"
        f"  2. Run with  --data <path-to-csv>\n"
        f"  3. Set the {DATA_ENV_VAR} environment variable\n"
        "  4. In Colab, let the notebook upload a CSV through google.colab.files\n"
        "  5. In Kaggle, mount a dataset under /kaggle/input/"
    )


def load_dataset(
    path: Optional[str | Path] = None,
    root: Optional[Path] = None,
    allow_upload: bool = True,
    **read_csv_kwargs,
) -> pd.DataFrame:
    """Load a CSV dataset and validate that it is usable.

    Raises ``FileNotFoundError`` when the file is missing and ``ValueError``
    when the file contains no data or no columns.
    """
    resolved = resolve_dataset_path(path, root=root, allow_upload=allow_upload)
    LOGGER.info("Loading dataset from %s", resolved)
    try:
        df = pd.read_csv(resolved, **read_csv_kwargs)
    except EmptyDataError as exc:  # pragma: no cover - pandas specific
        raise ValueError(f"The file '{resolved}' contains no columns/data.") from exc

    if df.shape[1] == 0:
        raise ValueError(f"The file '{resolved}' contains no columns.")
    if df.shape[0] == 0:
        raise ValueError(
            f"The file '{resolved}' contains headers but 0 data rows. "
            "Provide a dataset with at least one observation."
        )
    df.attrs["source_path"] = str(resolved)
    return df


def first_csv(folder: Path) -> Optional[Path]:
    """Return the first CSV file inside ``folder`` (used by tests/utilities)."""
    if not folder.exists():
        return None
    files = sorted(p for p in folder.glob("*.csv") if p.is_file())
    return files[0] if files else None


def list_columns(df: pd.DataFrame) -> dict:
    """Split column names into numerical and categorical lists."""
    numeric = list(df.select_dtypes(include="number").columns)
    categorical = [c for c in df.columns if c not in numeric]
    return {"numerical": numeric, "categorical": categorical}


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for every column."""
    total = len(df)
    table = pd.DataFrame(
        {
            "missing_count": df.isna().sum(),
            "missing_percent": (df.isna().sum() / max(total, 1) * 100).round(2),
            "dtype": df.dtypes.astype(str),
            "unique_values": df.nunique(dropna=True),
        }
    )
    return table.sort_values("missing_count", ascending=False)


def initial_inspection(df: pd.DataFrame) -> dict:
    """Return the standard 'first look' information about a dataset."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_total": int(df.isna().sum().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 3),
    }
