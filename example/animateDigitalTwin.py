import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from t1dsim_ai.individual_model import DigitalTwin

# Load data and setup digital twin
df_simulation = pd.read_csv("example_model/data_example.csv")
df_simulation = df_simulation[~df_simulation.is_train]
myDigitalTwin = DigitalTwin(n_digitalTwin=4)  # T1DEXI-01-1047
df_simulation = myDigitalTwin.simulate(df_simulation.iloc[1 * 12 * 24 : 2 * 12 * 24])

# Setup the figure and subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
fig.suptitle('T1D Digital Twin Animation - Real-time Glucose Dynamics', fontsize=16, fontweight='bold')

# Color scheme
color_actual = "#000000"      # Black for actual
color_pop = "#009E73"         # Green for population
color_dt = "#0072B2"          # Blue for digital twin
color_insulin = "#FF6B6B"     # Red for insulin
color_carbs = "#FFA500"       # Orange for carbs
color_hr = "#32CD32"          # Lime green for heart rate
color_sleep = "#9370DB"       # Purple for sleep

# Initialize empty lines for animation
time = np.arange(len(df_simulation))
line_actual, = ax1.plot([], [], 'o-', color=color_actual, ms=4, lw=1, label='Actual CGM')
line_pop, = ax1.plot([], [], 'o-', color=color_pop, ms=3, lw=1, label='Population Model')
line_dt, = ax1.plot([], [], 'o-', color=color_dt, ms=3, lw=1, label='Digital Twin')

# Insulin and meal lines
line_insulin, = ax2.plot([], [], color=color_insulin, lw=2, label='Insulin [U/h]')
line_carbs, = ax2.plot([], [], 'o', color=color_carbs, ms=6, label='Meal Carbs [g]')
line_hr, = ax2.plot([], [], color=color_hr, lw=1, label='Heart Rate [BPM]')
line_sleep, = ax2.plot([], [], color=color_sleep, lw=1, label='Sleep Efficiency')

# Setup glucose plot
ax1.set_ylim(40, 380)
ax1.set_ylabel('CGM [mg/dL]', fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.axhspan(70, 180, facecolor='gray', alpha=0.1, label='Target Range')
ax1.axhline(y=70, color='red', alpha=0.5, linestyle='--', lw=1)
ax1.axhline(y=180, color='red', alpha=0.5, linestyle='--', lw=1)
ax1.axhline(y=250, color='orange', alpha=0.5, linestyle='--', lw=1)
ax1.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

# Setup bottom plot
ax2.set_ylim(-5, 70)
ax2.set_ylabel('Insulin/Carbs/HR', fontweight='bold')
ax2.set_xlabel('Time [hours]', fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

# Add text annotations
time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=12, 
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
glucose_text = ax1.text(0.02, 0.85, '', transform=ax1.transAxes, fontsize=10,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Animation parameters
animation_speed = 50  # milliseconds between frames
window_size = 48     # Show last 4 hours (48 * 5-minute intervals)

def init():
    """Initialize animation"""
    line_actual.set_data([], [])
    line_pop.set_data([], [])
    line_dt.set_data([], [])
    line_insulin.set_data([], [])
    line_carbs.set_data([], [])
    line_hr.set_data([], [])
    line_sleep.set_data([], [])
    time_text.set_text('')
    glucose_text.set_text('')
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, line_hr, line_sleep, time_text, glucose_text

def animate(frame):
    """Animation function called for each frame"""
    # Calculate window start and end
    start_idx = max(0, frame - window_size)
    end_idx = frame + 1
    
    # Get time window data
    time_window = time[start_idx:end_idx]
    
    # Update glucose lines
    line_actual.set_data(time_window, df_simulation.cgm_Actual.iloc[start_idx:end_idx])
    line_pop.set_data(time_window, df_simulation.cgm_NNPop.iloc[start_idx:end_idx])
    line_dt.set_data(time_window, df_simulation.cgm_NNDT.iloc[start_idx:end_idx])
    
    # Update insulin and other parameters
    line_insulin.set_data(time_window, df_simulation.input_insulin.iloc[start_idx:end_idx])
    
    # Get meal data for current window
    meal_mask = (df_simulation.input_meal_carbs != 0) & (df_simulation.index >= start_idx) & (df_simulation.index < end_idx)
    meal_times = df_simulation.index[meal_mask]
    meal_carbs = df_simulation.input_meal_carbs[meal_mask]
    line_carbs.set_data(meal_times, meal_carbs)
    
    # Update heart rate and sleep
    line_hr.set_data(time_window, df_simulation.heart_rate.iloc[start_idx:end_idx])
    line_sleep.set_data(time_window, df_simulation.sleep_efficiency.iloc[start_idx:end_idx] * 50)  # Scale for visibility
    
    # Update text annotations
    current_time_hours = frame / 12  # Convert to hours (5-minute intervals)
    current_glucose = df_simulation.cgm_Actual.iloc[frame] if frame < len(df_simulation) else 0
    
    time_text.set_text(f'Time: {current_time_hours:.1f} hours\nFrame: {frame}/{len(df_simulation)}')
    glucose_text.set_text(f'Current Glucose: {current_glucose:.0f} mg/dL')
    
    # Update x-axis limits for scrolling effect
    if frame >= window_size:
        ax1.set_xlim(frame - window_size, frame)
        ax2.set_xlim(frame - window_size, frame)
    else:
        ax1.set_xlim(0, window_size)
        ax2.set_xlim(0, window_size)
    
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, line_hr, line_sleep, time_text, glucose_text

# Create animation
print("Creating animation... This may take a moment...")
ani = FuncAnimation(fig, animate, init_func=init, frames=len(df_simulation), 
                   interval=animation_speed, blit=True, repeat=True)

# Add controls
plt.tight_layout()

# Show the animation
print("Animation ready! Close the window to stop.")
plt.show()

# Optionally save the animation (uncomment to save)
# print("Saving animation...")
# ani.save('img/digital_twin_animation.gif', writer='pillow', fps=20, dpi=100)
# print("Animation saved as 'img/digital_twin_animation.gif'") 