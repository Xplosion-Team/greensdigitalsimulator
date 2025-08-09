import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
from t1dsim_ai.individual_model import DigitalTwin

# Load data and setup digital twin
df_simulation = pd.read_csv("example_model/data_example.csv")
df_simulation = df_simulation[~df_simulation.is_train]

# Global variables for interactive control
current_digital_twin = 4
current_speed = 50
animation_running = True

# Setup the figure with space for controls
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Simple Interactive T1D Digital Twin', fontsize=16, fontweight='bold')

# Create subplots
ax_main = plt.subplot2grid((5, 1), (0, 0), rowspan=4)  # Main plot
ax_control = plt.subplot2grid((5, 1), (4, 0), rowspan=1)  # Control panel

# Color scheme
color_actual = "#000000"
color_pop = "#009E73"
color_dt = "#0072B2"
color_insulin = "#FF6B6B"
color_carbs = "#FFA500"

# Initialize empty lines for animation
time = np.arange(len(df_simulation))
line_actual, = ax_main.plot([], [], 'o-', color=color_actual, ms=4, lw=1, label='Actual CGM')
line_pop, = ax_main.plot([], [], 'o-', color=color_pop, ms=3, lw=1, label='Population Model')
line_dt, = ax_main.plot([], [], 'o-', color=color_dt, ms=3, lw=1, label='Digital Twin')
line_insulin, = ax_main.plot([], [], color=color_insulin, lw=2, label='Insulin [U/h]')
line_carbs, = ax_main.plot([], [], 'o', color=color_carbs, ms=6, label='Meal Carbs [g]')

# Setup main glucose plot
ax_main.set_ylim(40, 380)
ax_main.set_ylabel('CGM [mg/dL]', fontweight='bold')
ax_main.set_xlabel('Time [hours]', fontweight='bold')
ax_main.grid(True, alpha=0.3)
ax_main.axhspan(70, 180, facecolor='gray', alpha=0.1, label='Target Range')
ax_main.axhline(y=70, color='red', alpha=0.5, linestyle='--', lw=1)
ax_main.axhline(y=180, color='red', alpha=0.5, linestyle='--', lw=1)
ax_main.axhline(y=250, color='orange', alpha=0.5, linestyle='--', lw=1)
ax_main.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)

# Setup control panel
ax_control.set_xlim(0, 10)
ax_control.set_ylim(0, 10)
ax_control.axis('off')

# Add text annotations
time_text = ax_main.text(0.02, 0.95, '', transform=ax_main.transAxes, fontsize=12, 
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
glucose_text = ax_main.text(0.02, 0.85, '', transform=ax_main.transAxes, fontsize=10,
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Function to update digital twin
def update_digital_twin(val):
    global current_digital_twin, df_simulation
    current_digital_twin = int(val)
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(df_simulation.iloc[1 * 12 * 24 : 2 * 12 * 24])
    print(f"Switched to Digital Twin {current_digital_twin}")

# Function to update animation speed
def update_speed(val):
    global current_speed
    current_speed = int(val)
    print(f"Animation speed: {current_speed}ms")

# Function to pause/resume animation
def toggle_animation(event):
    global animation_running
    animation_running = not animation_running
    if animation_running:
        pause_button.label.set_text('⏸️ Pause')
        print("Animation resumed")
    else:
        pause_button.label.set_text('▶️ Resume')
        print("Animation paused")

# Function to reset animation
def reset_animation(event):
    global current_frame
    current_frame = 0
    print("Animation reset to beginning")

# Create sliders
ax_speed = plt.axes([0.15, 0.05, 0.2, 0.03])
ax_dt = plt.axes([0.45, 0.05, 0.2, 0.03])

speed_slider = Slider(ax_speed, 'Speed (ms)', 10, 200, valinit=current_speed, valstep=10)
dt_slider = Slider(ax_dt, 'Digital Twin', 0, 4, valinit=current_digital_twin, valstep=1)

# Create buttons
ax_pause = plt.axes([0.7, 0.05, 0.08, 0.04])
ax_reset = plt.axes([0.8, 0.05, 0.08, 0.04])

pause_button = Button(ax_pause, '⏸️ Pause')
reset_button = Button(ax_reset, '🔄 Reset')

# Connect sliders and buttons
speed_slider.on_changed(update_speed)
dt_slider.on_changed(update_digital_twin)
pause_button.on_clicked(toggle_animation)
reset_button.on_clicked(reset_animation)

def get_glucose_status(glucose_value):
    """Get glucose status based on value"""
    if glucose_value < 70:
        return "HYPOGLYCEMIA", "red", "⚠️"
    elif glucose_value <= 180:
        return "NORMAL", "green", "✅"
    elif glucose_value <= 250:
        return "HIGH", "orange", "⚠️"
    else:
        return "VERY HIGH", "red", "🚨"

def init():
    """Initialize animation"""
    line_actual.set_data([], [])
    line_pop.set_data([], [])
    line_dt.set_data([], [])
    line_insulin.set_data([], [])
    line_carbs.set_data([], [])
    time_text.set_text('')
    glucose_text.set_text('')
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, time_text, glucose_text

def animate(frame):
    """Animation function called for each frame"""
    global animation_running
    
    if not animation_running:
        return line_actual, line_pop, line_dt, line_insulin, line_carbs, time_text, glucose_text
    
    # Calculate window start and end (show last 4 hours)
    window_size = 48  # 4 hours * 12 frames per hour
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
    
    # Update text annotations
    current_time_hours = frame / 12
    current_glucose = df_simulation.cgm_Actual.iloc[frame] if frame < len(df_simulation) else 0
    current_insulin = df_simulation.input_insulin.iloc[frame] if frame < len(df_simulation) else 0
    
    status, color, emoji = get_glucose_status(current_glucose)
    
    time_text.set_text(f'Time: {current_time_hours:.1f} hours | Frame: {frame}/{len(df_simulation)}')
    glucose_text.set_text(f'{emoji} {status} | Glucose: {current_glucose:.0f} mg/dL | Insulin: {current_insulin:.1f} U/h', color=color)
    
    # Update x-axis limits for scrolling effect
    if frame >= window_size:
        ax_main.set_xlim(frame - window_size, frame)
    else:
        ax_main.set_xlim(0, window_size)
    
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, time_text, glucose_text

# Create animation
print("Creating simple interactive animation... This may take a moment...")
ani = FuncAnimation(fig, animate, init_func=init, frames=len(df_simulation), 
                   interval=current_speed, blit=True, repeat=True)

# Add controls
plt.tight_layout()

# Show the animation
print("Simple interactive animation ready!")
print("Controls:")
print("- Speed slider: Adjust animation speed (10-200ms)")
print("- Digital Twin slider: Switch between patients (0-4)")
print("- Pause/Resume: Control animation playback")
print("- Reset: Go back to beginning")
plt.show() 