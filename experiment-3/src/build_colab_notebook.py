"""Create the upload-ready Colab/Kaggle copy of the validated experiment notebook.

The source notebook ``EXPERIMENT 3.ipynb`` is never modified.  This script
produces ``EXPERIMENT 3 - Statistical Visualization and EDA.ipynb`` which:

* keeps every cell, output, plot, report and viva answer of the original,
* ships the project code (``src/``) and the dataset inside the notebook so a
  fresh Google Colab / Kaggle runtime needs no manual file upload,
* never blocks on ``input()`` / ``files.upload()`` during *Runtime -> Run all*,
* writes plots and reports to ``/content``, ``/kaggle/working`` or the local
  project folder depending on where it runs.
"""

from __future__ import annotations

import base64
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "EXPERIMENT 3.ipynb"
TARGET = ROOT / "EXPERIMENT 3 - Statistical Visualization and EDA.ipynb"

ARCHIVE_MEMBERS = [
    "requirements.txt",
    "data/raw/penguins.csv",
    "outputs/reports/viva_questions.md",
]

CHUNK = 100


def build_archive() -> bytes:
    """Zip the modules the notebook imports plus the validated dataset."""
    members = list(ARCHIVE_MEMBERS)
    src_dir = ROOT / "src"
    for path in sorted(src_dir.glob("*.py")):
        members.append(f"src/{path.name}")

    buffer_path = TARGET.parent / "_eda_project_payload.zip"
    with zipfile.ZipFile(buffer_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for member in members:
            zf.write(ROOT / member.replace("/", "\\"), member)
    payload = buffer_path.read_bytes()
    buffer_path.unlink()
    return payload


def archive_cell(payload: bytes) -> dict:
    encoded = base64.b64encode(payload).decode("ascii")
    lines = [encoded[i:i + CHUNK] for i in range(0, len(encoded), CHUNK)]
    body = "\n".join(f'    "{line}",' for line in lines)
    header = (
        "# ============================================================\n"
        "# 0b. PROJECT ARCHIVE EMBEDDED IN THIS NOTEBOOK\n"
        "#     Restores src/ (analysis modules) and data/raw/penguins.csv on a\n"
        "#     fresh Google Colab / Kaggle runtime, so \"Runtime -> Run all\"\n"
        "#     works without uploading any extra file.\n"
        "# ============================================================\n"
        f"_EDA_PROJECT_ARCHIVE_ZIP_BYTES = {len(payload)}\n"
        "\n"
        'EDA_PROJECT_ARCHIVE_B64 = "".join([\n'
    )
    footer = (
        "\n"
        "])\n"
        "\n"
        "print(\n"
        "    f\"Embedded project archive ready: \"\n"
        "    f\"{_EDA_PROJECT_ARCHIVE_ZIP_BYTES / 1024:.1f} KB \"\n"
        "    f\"(used only when src/ or data/ are missing).\"\n"
        ")\n"
    )
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": "edaarch1",
        "metadata": {},
        "outputs": [],
        "source": (header + body + footer).splitlines(keepends=True),
    }


NEW_ROOT_CELL = '''\
# --- locate the project folder (works on any machine / Colab / Kaggle) ---
def find_project_root(start=None):
    start = Path(start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "src").is_dir() and (candidate / "data").is_dir():
            return candidate
    return start


def _extract_archive(archive: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(destination)


ROOT = find_project_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- fresh runtime (Google Colab / Kaggle)? restore the project files ------
if not (ROOT / "src").is_dir() or not (ROOT / "data" / "raw").is_dir():
    workspace = Path.cwd()

    # 1) archive embedded in this notebook - fully automatic
    if globals().get("EDA_PROJECT_ARCHIVE_B64"):
        import base64 as _b64

        embedded = workspace / "_eda_project_embedded.zip"
        embedded.write_bytes(_b64.b64decode(EDA_PROJECT_ARCHIVE_B64))
        _extract_archive(embedded, workspace)
        embedded.unlink(missing_ok=True)
        print("Project code and dataset restored from the embedded archive.")

    # 2) a ZIP already present in the working directory (Files pane / input dataset)
    if not (workspace / "src").is_dir():
        for candidate in sorted(workspace.glob("*.zip")):
            try:
                with zipfile.ZipFile(candidate) as zf:
                    names = zf.namelist()
            except zipfile.BadZipFile:
                continue
            if any(name.startswith("src/") for name in names):
                _extract_archive(candidate, workspace)
                print(f"Project restored from {candidate.name}")
                break

    # 3) last resort - interactive upload (only when nothing else worked)
    if not (workspace / "src").is_dir() and IS_COLAB:
        from google.colab import files  # type: ignore
        print("No project files found. Upload the project ZIP (eda_experiment3_outputs.zip)")
        print("or at least the dataset CSV (e.g. penguins.csv):")
        uploaded = files.upload()
        for name, content in uploaded.items():
            Path(name).write_bytes(content)
            if name.lower().endswith(".zip"):
                _extract_archive(Path(name), workspace)

    ROOT = find_project_root()
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

# --- create every output directory (idempotent) ---------------
for sub in ["data/raw", "data/processed", "outputs/plots", "outputs/reports", "outputs/logs"]:
    (ROOT / sub).mkdir(parents=True, exist_ok=True)

print("Project root  :", ROOT)
print("Dataset folder:", ROOT / "data" / "raw")
'''


def patch_download_cell(source: str) -> str:
    return source.replace(
        '''if IS_COLAB:
    from google.colab import files  # type: ignore
    print("\\nDownloading the ZIP archive ...")
    files.download(str(zip_path))''',
        '''if IS_COLAB:
    try:
        from google.colab import files  # type: ignore
        print("\\nDownloading the ZIP archive ...")
        files.download(str(zip_path))
    except Exception as exc:  # never let a download stop the run
        print("Automatic download skipped:", exc)
        print("The archive is also available at:", zip_path)''',
    )


def patch_individual_downloads_cell(source: str) -> str:
    old = '''if IS_COLAB:
    answer = input("Download any of these files individually? (y/n): ").strip().lower()
    if answer == "y":
        from google.colab import files  # type: ignore
        for target in targets:
            if target.exists():
                files.download(str(target))
else:'''
    new = '''if IS_COLAB:
    # A blocking input() would stop "Runtime -> Run all", so the choice is read
    # from an environment variable instead.  Opt in with:
    #     os.environ["EDA_DOWNLOAD_INDIVIDUAL"] = "y"
    if os.environ.get("EDA_DOWNLOAD_INDIVIDUAL", "n").strip().lower() == "y":
        from google.colab import files  # type: ignore
        for target in targets:
            if target.exists():
                files.download(str(target))
    else:
        print("\\nIndividual downloads are switched off (nothing blocks the run).")
        print("Every file above is saved under", ROOT / "outputs", "and", ROOT / "data")
else:'''
    if old not in source:
        raise SystemExit("individual-downloads cell not found - source changed")
    return source.replace(old, new)


def patch_how_to_run(source: str) -> str:
    return source.replace(
        """**How to run:** *Runtime -> Run all* (Google Colab) or open in Jupyter and run
top-to-bottom. The notebook detects Google Colab, Kaggle and local Python by
itself and needs no manual path changes.""",
        """**How to run:** upload this file to Google Colab (*File -> Upload notebook*)
and use *Runtime -> Run all*, or open it in Jupyter and run top-to-bottom. The
notebook carries its own `src/` modules and dataset, detects Google Colab,
Kaggle and local Python by itself and needs no manual path changes. Plots and
reports are written to `/content/outputs` (Colab), `/kaggle/working/outputs`
(Kaggle) or `<project>/outputs` (local).""",
    )


def patch_run_elsewhere(source: str) -> str:
    return source.replace(
        """**Google Colab** - upload `eda_experiment3_outputs.zip` (or this notebook plus
`data/raw/penguins.csv`) and use *Runtime -> Run all*. The notebook installs any
missing library, detects Colab, uploads a CSV when no dataset exists and
downloads the finished ZIP at the end.""",
        """**Google Colab** - upload only this notebook (*File -> Upload notebook*) and
use *Runtime -> Run all*. The notebook restores `src/` and the dataset from the
archive embedded in it, installs any missing library, detects Colab and offers
the finished ZIP at the end. No other file has to be uploaded.""",
    )


def main() -> None:
    notebook = json.loads(SOURCE.read_text(encoding="utf-8"))
    cells = notebook["cells"]

    def find(marker: str) -> dict:
        for cell in cells:
            if cell["cell_type"] == "code" and marker in "".join(cell["source"]):
                return cell
        raise SystemExit(f"cell not found: {marker!r}")

    def replace(marker: str, new_source: str) -> None:
        cell = find(marker)
        cell["source"] = new_source.splitlines(keepends=True)

    replace("# --- locate the project folder", NEW_ROOT_CELL)

    download_cell = find("# --- package plots, reports")
    patched = patch_download_cell("".join(download_cell["source"]))
    if patched == "".join(download_cell["source"]):
        raise SystemExit("download cell not patched - source changed")
    download_cell["source"] = patched.splitlines(keepends=True)

    individual_cell = find("# --- individual downloads / quick access")
    individual_cell["source"] = patch_individual_downloads_cell(
        "".join(individual_cell["source"])
    ).splitlines(keepends=True)

    patched_markdown = 0
    for cell in cells:
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"])
            if src.startswith("# EXPERIMENT 3 - Exploratory Data Analysis"):
                new = patch_how_to_run(src)
            elif "**Google Colab** - upload" in src:
                new = patch_run_elsewhere(src)
            else:
                continue
            if new != src:
                cell["source"] = new.splitlines(keepends=True)
                patched_markdown += 1
    if patched_markdown != 2:
        raise SystemExit(f"expected 2 markdown patches, made {patched_markdown}")

    cells.insert(2, archive_cell(build_archive()))

    # the validated Q&A report also becomes part of the notebook itself
    for index, cell in enumerate(cells):
        if cell["cell_type"] == "markdown" and "".join(cell["source"]).startswith(
            "## 18. Viva questions"
        ):
            viva = (ROOT / "outputs" / "reports" / "viva_questions.md").read_text(
                encoding="utf-8"
            )
            cells.insert(
                index + 1,
                {
                    "cell_type": "markdown",
                    "id": "edavivaqa",
                    "metadata": {},
                    "source": viva.splitlines(keepends=True),
                },
            )
            break
    else:
        raise SystemExit("viva section not found")

    notebook["metadata"]["colab"]["name"] = "EXPERIMENT 3 - Statistical Visualization and EDA"
    TARGET.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", TARGET, f"({TARGET.stat().st_size / 1e6:.2f} MB, {len(cells)} cells)")


if __name__ == "__main__":
    main()
