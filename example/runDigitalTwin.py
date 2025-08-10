import pandas as pd

from t1dsim_ai.individual_model import DigitalTwin

import numpy as np
import matplotlib.pyplot as plt

df_simulation = pd.read_csv("example_model/data_example.csv")
df_simulation = df_simulation[~df_simulation.is_train]

# MODIFY THIS: Choose different digital twin model
# 0 = T1DEXI-01-0102, 1 = T1DEXI-01-0692, 2 = T1DEXI-01-0794, 3 = T1DEXI-01-0880, 4 = T1DEXI-01-1047
myDigitalTwin = DigitalTwin(n_digitalTwin=4)

# MODIFY THIS: Change simulation time window
# Current: Day 1 to Day 2 (1 * 12 * 24 : 2 * 12 * 24)
# Try: Day 0 to Day 1 (0 * 12 * 24 : 1 * 12 * 24)
# Try: Full 3 days (0 * 12 * 24 : 3 * 12 * 24)
df_simulation = myDigitalTwin.simulate(df_simulation.iloc[1 * 12 * 24 : 2 * 12 * 24])

# Visualization

# MODIFY THESE: Change plot colors
color_AIDT = "#0072B2"    # Blue for digital twin
color_AIPop = "#009E73"   # Green for population model

# MODIFY THIS: Change figure size (width, height)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

time = np.arange(len(df_simulation))

ax1.plot(time, df_simulation.cgm_Actual, ms=5, c="k")
ax1.plot(time, df_simulation.cgm_NNPop, ".", ms=5, c=color_AIPop)
ax1.plot(time, df_simulation.cgm_NNDT, ".", ms=5, c=color_AIDT)

ax1.plot(-1, -1, "o", ms=5, c="k", label="Actual")
ax1.plot(-1, -1, "o", ms=5, c=color_AIPop, label="NN-based population")
ax1.plot(-1, -1, "o", ms=5, c=color_AIDT, label="NN-based digital twin")

# MODIFY THIS: Change glucose target zone (mg/dL)
ax1.axhspan(70, 180, facecolor="gray", alpha=0.1)

# MODIFY THESE: Change glucose threshold lines
for y in [70, 180, 250]:
    ax1.axhline(y, color="k", alpha=0.2, lw=0.3)

ax1.legend(loc=9, ncol=3, frameon=False)

# MODIFY THIS: Change glucose display range
ax1.set_ylim(40, 380)
ax1.set_ylabel("CGM [mg/dL]")
for location in ["left", "right", "top", "bottom"]:
    ax1.spines[location].set_linewidth(0.1)

ax2.plot(time, df_simulation.input_insulin, c="k", lw=0.7)
ax2.set_ylim(-1, 65)

ax2.set_ylabel("Insulin [U/h]")
for location in ["left", "right", "top", "bottom"]:
    ax2.spines[location].set_linewidth(0.1)
ax2.spines["top"].set_linewidth(0.5)
ax2_carbs = ax2.twinx()
color = "tab:red"
ax2_carbs.plot(
    df_simulation.loc[df_simulation.input_meal_carbs != 0].index,
    df_simulation.loc[df_simulation.input_meal_carbs != 0, "input_meal_carbs"],
    "o",
    color=color,
)
ax2_carbs.set_ylim(-1, 65)

ax2_carbs.set_ylabel("Meal carbs [g]", color=color)
ax2_carbs.tick_params(axis="y", labelcolor=color)
ax2_carbs.spines["right"].set_position(("axes", 0))
for location in ["left", "right", "top", "bottom"]:
    ax2_carbs.spines[location].set_linewidth(0)
ax2_hr = ax2.twinx()
color = "tab:green"
ax2_hr.plot(time, df_simulation.heart_rate, lw=0.5, color=color)
ax2_hr.set_ylim(-1.4, 147)

ax2_hr.set_ylabel("Heart rate [BPM]", color=color)
ax2_hr.tick_params(axis="y", labelcolor=color)
for location in ["left", "right", "top", "bottom"]:
    ax2_hr.spines[location].set_linewidth(0)
ax2_pa = ax2.twinx()
color = "tab:purple"
ax2_pa.plot(time, df_simulation.sleep_efficiency, lw=1, color=color)
ax2_pa.set_ylim(-0.01, 1.05)
for location in ["left", "right", "top", "bottom"]:
    ax2_pa.spines[location].set_linewidth(0)

ax2_pa.set_ylabel("Sleep efficiency", color=color, labelpad=-20)
ax2_pa.tick_params(axis="y", labelcolor=color)
ax2_pa.set_yticks([0, 1], [0, 1])
ax2_pa.tick_params(axis="y", direction="in", pad=-15)


ax2.set_xticks(np.arange(0, 1 * 12 * 24 + 1, 12 * 12), np.arange(0, 1.1, 0.5))
ax2.set_xlabel("Simulation time [day]")
ax2.set_xlim(-12 * 3, 1 * 12 * 24 + 12 * 2)

plt.subplots_adjust(hspace=0)

# UNCOMMENT THIS to display plot instead of saving
# plt.show()

# MODIFY THIS: Change output filename and quality
plt.savefig(
    "img/example_digitaltwin" + str(myDigitalTwin.n_digitalTwin) + ".png",
    dpi=500,  # Change DPI for different quality (300, 600, etc.)
    bbox_inches="tight",
)
