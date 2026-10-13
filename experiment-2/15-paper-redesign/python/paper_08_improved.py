# VisAhoi: Towards a library to generate and integrate visualization onboarding using high-level visualization grammars
# Educational reconstruction for M.E. CSE Data Visualization Exercise-2.
# The reconstruction is NOT a reproduction of the authors' research findings.
# Replace only with published numerical values when the source provides them.
import matplotlib.pyplot as plt
import numpy as np


import os
from pathlib import Path as _Path


def _visualizations_dir() -> _Path:
    """Where saved figures go: env override -> repo folder -> cwd fallback."""
    if os.environ.get("EX2_VIS_DIR"):
        out = _Path(os.environ["EX2_VIS_DIR"])
    else:
        try:
            out = _Path(__file__).resolve().parent.parent / "visualizations"
        except NameError:  # exec()'d inside a notebook cell: no __file__
            out = _Path.cwd() / "visualizations"
    out.mkdir(parents=True, exist_ok=True)
    return out


# Illustrative reconstruction data / structure:
steps=np.arange(1,6); anchor=[1,4,2,5,3]

# Plot:
fig,ax=plt.subplots(figsize=(9,5)); ax.plot(steps,anchor,"o-"); ax.set_xlabel("Onboarding step"); ax.set_ylabel("Illustrative anchor position")

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_08_improved.png", dpi=300, bbox_inches="tight")
plt.show()
