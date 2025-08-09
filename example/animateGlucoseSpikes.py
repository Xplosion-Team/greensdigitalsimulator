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

# Setup the figure
fig, ax = plt.subplots(figsize=(16, 10))
fig.suptitle('T1D Glucose Spikes Animation - Real-time CGM Dynamics', fontsize=18, fontweight='bold')

# Color scheme
color_actual = "#000000"      # Black for actual
color_pop = "#009E73"         # Green for population
color_dt = "#0072B2"          # Blue for digital twin

# Initialize empty lines for animation
time = np.arange(len(df_simulation))
line_actual, = ax.plot([], [], 'o-', color=color_actual, ms=6, lw=2, label='Actual CGM', alpha=0.8)
line_pop, = ax.plot([], [], 'o-', color=color_pop, ms=4, lw=2, label='Population Model', alpha=0.7)
line_dt, = ax.plot([], [], 'o-', color=color_dt, ms=4, lw=2, label='Digital Twin', alpha=0.7)

# Setup glucose plot with enhanced styling
ax.set_ylim(40, 380)
ax.set_ylabel('CGM [mg/dL]', fontsize=14, fontweight='bold')
ax.set_xlabel('Time [hours]', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')

# Add glucose zones with enhanced styling
ax.axhspan(70, 180, facecolor='lightgreen', alpha=0.3, label='Target Range (70-180 mg/dL)')
ax.axhspan(180, 250, facecolor='orange', alpha=0.2, label='High Range (180-250 mg/dL)')
ax.axhspan(250, 380, facecolor='red', alpha=0.2, label='Very High (>250 mg/dL)')
ax.axhspan(40, 70, facecolor='yellow', alpha=0.2, label='Low Range (40-70 mg/dL)')

# Add threshold lines
ax.axhline(y=70, color='red', alpha=0.7, linestyle='--', lw=2, label='Hypoglycemia Threshold')
ax.axhline(y=180, color='orange', alpha=0.7, linestyle='--', lw=2, label='Hyperglycemia Threshold')
ax.axhline(y=250, color='red', alpha=0.7, linestyle='--', lw=2, label='Severe Hyperglycemia')

# Add legend
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, fontsize=12)

# Add text annotations
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=14, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
glucose_text = ax.text(0.02, 0.85, '', transform=ax.transAxes, fontsize=12,
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))
status_text = ax.text(0.02, 0.75, '', transform=ax.transAxes, fontsize=12,
                      bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))

# Animation parameters
animation_speed = 30  # milliseconds between frames (faster for dramatic effect)
window_size = 72     # Show last 6 hours (72 * 5-minute intervals)

def get_glucose_status(glucose_value):
    """Get glucose status based on value"""
    if glucose_value < 70:
        return "HYPOGLYCEMIA", "red"
    elif glucose_value <= 180:
        return "NORMAL", "green"
    elif glucose_value <= 250:
        return "HIGH", "orange"
    else:
        return "VERY HIGH", "red"

def init():
    """Initialize animation"""
    line_actual.set_data([], [])
    line_pop.set_data([], [])
    line_dt.set_data([], [])
    time_text.set_text('')
    glucose_text.set_text('')
    status_text.set_text('')
    return line_actual, line_pop, line_dt, time_text, glucose_text, status_text

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
    
    # Update text annotations
    current_time_hours = frame / 12  # Convert to hours (5-minute intervals)
    current_glucose = df_simulation.cgm_Actual.iloc[frame] if frame < len(df_simulation) else 0
    current_pop = df_simulation.cgm_NNPop.iloc[frame] if frame < len(df_simulation) else 0
    current_dt = df_simulation.cgm_NNDT.iloc[frame] if frame < len(df_simulation) else 0
    
    status, color = get_glucose_status(current_glucose)
    
    time_text.set_text(f'Time: {current_time_hours:.1f} hours\nFrame: {frame}/{len(df_simulation)}')
    glucose_text.set_text(f'Actual: {current_glucose:.0f} mg/dL\nPopulation: {current_pop:.0f} mg/dL\nDigital Twin: {current_dt:.0f} mg/dL')
    status_text.set_text(f'Status: {status}', color=color)
    
    # Update x-axis limits for scrolling effect
    if frame >= window_size:
        ax.set_xlim(frame - window_size, frame)
    else:
        ax.set_xlim(0, window_size)
    
    # Add dramatic effect for spikes
    if current_glucose > 250:
        ax.set_facecolor('lightcoral')
    elif current_glucose < 70:
        ax.set_facecolor('lightyellow')
    else:
        ax.set_facecolor('white')
    
    return line_actual, line_pop, line_dt, time_text, glucose_text, status_text

# Create animation
print("Creating glucose spikes animation... This may take a moment...")
ani = FuncAnimation(fig, animate, init_func=init, frames=len(df_simulation), 
                   interval=animation_speed, blit=True, repeat=True)

# Add controls
plt.tight_layout()

# Show the animation
print("Animation ready! Close the window to stop.")
print("Watch for dramatic color changes during glucose spikes!")
plt.show()

# Optionally save the animation (uncomment to save)
# print("Saving animation...")
# ani.save('img/glucose_spikes_animation.gif', writer='pillow', fps=30, dpi=100)
# print("Animation saved as 'img/glucose_spikes_animation.gif'") 