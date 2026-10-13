# Evaluating user cognition of network diagrams
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
edges=[(0,1),(1,2),(2,3),(0,3),(0,2)]; pos={0:(0,0),1:(0,1),2:(1,1),3:(1,0)}

# Plot:
fig,ax=plt.subplots(figsize=(7,6))
for a,b in edges: ax.plot([pos[a][0],pos[b][0]],[pos[a][1],pos[b][1]],lw=1.8)
for n,(x,y) in pos.items(): ax.scatter(x,y,s=700); ax.text(x,y,str(n),ha="center",va="center")
ax.axis("off")

plt.tight_layout()
plt.savefig(_visualizations_dir() / "paper_12_improved.png", dpi=300, bbox_inches="tight")
plt.show()
