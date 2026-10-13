# VISUALIZATION 1 — COMPREHENSION SCORE

import matplotlib.pyplot as plt
import numpy as np

groups = ["Text only", "Bar graph", "Pictograph", "Line graph"]
mean = [3.71, 3.79, 4.25, 3.81]
sd = [1.63, 1.54, 1.40, 1.53]

fig, ax = plt.subplots(figsize=(8, 5))
y = np.arange(len(groups))

ax.barh(y, mean, xerr=sd, capsize=4)
ax.set_yticks(y, groups)
ax.invert_yaxis()
ax.set_xlim(0, 6)
ax.set_xlabel("Mean comprehension score (0–6)")
ax.set_title("Trial A: Mean comprehension score")
ax.grid(axis="x", alpha=0.25)

for i, value in enumerate(mean):
    ax.text(value + 0.05, i, f"{value:.2f}", va="center")

plt.tight_layout()
plt.show()


# VISUALIZATION 2 — DECISION INTENTION

import matplotlib.pyplot as plt
import numpy as np

groups = ["Text only", "Bar graph", "Pictograph", "Line graph"]
before = [66.0, 64.6, 62.7, 68.1]
after  = [72.8, 64.6, 79.1, 73.6]

x = np.arange(len(groups))
width = 0.36

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - width/2, before, width, label="Before")
ax.bar(x + width/2, after, width, label="After")

ax.set_xticks(x, groups, rotation=25, ha="right")
ax.set_ylim(0, 100)
ax.set_ylabel("Participants choosing antibiotics (%)")
ax.set_title("Trial A: Decision intention before vs after")
ax.legend()

for i, value in enumerate(before):
    ax.text(i - width/2, value + 2, f"{value:.1f}%", ha="center")
for i, value in enumerate(after):
    ax.text(i + width/2, value + 2, f"{value:.1f}%", ha="center")

plt.tight_layout()
plt.show()


# VISUALIZATION 3 — PRESENTATION PREFERENCE

import matplotlib.pyplot as plt

labels = ["Text only", "Bar graph", "Pictograph", "Line graph"]
counts = [124, 137, 58, 98]
total = sum(counts)
percent = [c / total * 100 for c in counts]

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(labels[::-1], percent[::-1])

ax.set_xlim(0, 40)
ax.set_xlabel("Participants choosing format first (%)")
ax.set_title("Trial A: Visual presentation preference")

for y, value in enumerate(percent[::-1]):
    ax.text(value + 0.5, y, f"{value:.1f}%", va="center")

plt.tight_layout()
plt.show()
