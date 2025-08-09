import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
from t1dsim_ai.individual_model import DigitalTwin

# Load data and setup digital twin
df_simulation = pd.read_csv("example_model/data_example.csv")
df_simulation = df_simulation[~df_simulation.is_train]

# Global variables for interactive control
current_digital_twin = 4
current_speed = 50
current_window = 48
animation_running = True
current_frame = 0

# Setup the figure with extra space for controls
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Interactive T1D Digital Twin - Real-time Control Panel', fontsize=16, fontweight='bold')

# Create subplots with different sizes
ax_main = plt.subplot2grid((4, 4), (0, 0), colspan=3, rowspan=3)  # Main plot
ax_control = plt.subplot2grid((4, 4), (3, 0), colspan=4, rowspan=1)  # Control panel
ax_glucose = plt.subplot2grid((4, 4), (0, 3), rowspan=2)  # Glucose status
ax_params = plt.subplot2grid((4, 4), (2, 3), rowspan=1)  # Parameter display

# Color scheme
color_actual = "#000000"
color_pop = "#009E73"
color_dt = "#0072B2"
color_insulin = "#FF6B6B"
color_carbs = "#FFA500"
color_hr = "#32CD32"
color_sleep = "#9370DB"

# Initialize empty lines for animation
time = np.arange(len(df_simulation))
line_actual, = ax_main.plot([], [], 'o-', color=color_actual, ms=4, lw=1, label='Actual CGM')
line_pop, = ax_main.plot([], [], 'o-', color=color_pop, ms=3, lw=1, label='Population Model')
line_dt, = ax_main.plot([], [], 'o-', color=color_dt, ms=3, lw=1, label='Digital Twin')

# Insulin and meal lines
line_insulin, = ax_main.plot([], [], color=color_insulin, lw=2, label='Insulin [U/h]')
line_carbs, = ax_main.plot([], [], 'o', color=color_carbs, ms=6, label='Meal Carbs [g]')
line_hr, = ax_main.plot([], [], color=color_hr, lw=1, label='Heart Rate [BPM]')
line_sleep, = ax_main.plot([], [], color=color_sleep, lw=1, label='Sleep Efficiency')

# Setup main glucose plot
ax_main.set_ylim(40, 380)
ax_main.set_ylabel('CGM [mg/dL]', fontweight='bold')
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

# Setup glucose status panel
ax_glucose.set_xlim(0, 1)
ax_glucose.set_ylim(0, 1)
ax_glucose.axis('off')

# Setup parameter panel
ax_params.set_xlim(0, 1)
ax_params.set_ylim(0, 1)
ax_params.axis('off')

# Add text annotations
time_text = ax_main.text(0.02, 0.95, '', transform=ax_main.transAxes, fontsize=12, 
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
glucose_text = ax_glucose.text(0.1, 0.8, 'Glucose Status', transform=ax_glucose.transAxes, 
                               fontsize=14, fontweight='bold')
status_text = ax_glucose.text(0.1, 0.6, '', transform=ax_glucose.transAxes, fontsize=12,
                              bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
param_text = ax_params.text(0.1, 0.8, 'Current Parameters', transform=ax_params.transAxes, 
                            fontsize=12, fontweight='bold')

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

# Function to update window size
def update_window(val):
    global current_window
    current_window = int(val)
    print(f"Window size: {current_window} frames ({current_window/12:.1f} hours)")

# Function to pause/resume animation
def toggle_animation(event):
    global animation_running
    animation_running = not animation_running
    if animation_running:
        pause_button.label.set_text('Pause')
        print("Animation resumed")
    else:
        pause_button.label.set_text('Resume')
        print("Animation paused")

# Function to reset animation
def reset_animation(event):
    global current_frame
    current_frame = 0
    print("Animation reset to beginning")

# Function to jump to specific time
def jump_to_time(text):
    global current_frame
    try:
        hours = float(text)
        current_frame = int(hours * 12)  # Convert hours to frames
        current_frame = max(0, min(current_frame, len(df_simulation)-1))
        print(f"Jumped to {hours} hours (frame {current_frame})")
    except ValueError:
        print("Invalid time format. Use decimal hours (e.g., 2.5)")

# Create sliders
ax_speed = plt.axes([0.15, 0.05, 0.2, 0.03])
ax_window = plt.axes([0.15, 0.02, 0.2, 0.03])
ax_dt = plt.axes([0.45, 0.05, 0.2, 0.03])

speed_slider = Slider(ax_speed, 'Speed (ms)', 10, 200, valinit=current_speed, valstep=10)
window_slider = Slider(ax_window, 'Window (hours)', 1, 12, valinit=current_window/12, valstep=0.5)
dt_slider = Slider(ax_dt, 'Digital Twin', 0, 4, valinit=current_digital_twin, valstep=1)

# Create buttons
ax_pause = plt.axes([0.7, 0.05, 0.08, 0.04])
ax_reset = plt.axes([0.8, 0.05, 0.08, 0.04])
ax_jump = plt.axes([0.9, 0.05, 0.08, 0.04])

pause_button = Button(ax_pause, 'Pause')
reset_button = Button(ax_reset, 'Reset')
jump_button = Button(ax_jump, 'Jump')

# Create text box for time jump
ax_textbox = plt.axes([0.7, 0.02, 0.2, 0.02])
time_textbox = TextBox(ax_textbox, 'Jump to (hours): ', initial='0.0')

# Connect sliders and buttons
speed_slider.on_changed(update_speed)
window_slider.on_changed(update_window)
dt_slider.on_changed(update_digital_twin)
pause_button.on_clicked(toggle_animation)
reset_button.on_clicked(reset_animation)
jump_button.on_clicked(lambda event: jump_to_time(time_textbox.text))

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
    line_hr.set_data([], [])
    line_sleep.set_data([], [])
    time_text.set_text('')
    status_text.set_text('')
    param_text.set_text('')
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, line_hr, line_sleep, time_text, status_text, param_text

def animate(frame):
    """Animation function called for each frame"""
    global current_frame, animation_running
    
    if not animation_running:
        return line_actual, line_pop, line_dt, line_insulin, line_carbs, line_hr, line_sleep, time_text, status_text, param_text
    
    current_frame = frame
    
    # Calculate window start and end
    start_idx = max(0, frame - current_window)
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
    line_sleep.set_data(time_window, df_simulation.sleep_efficiency.iloc[start_idx:end_idx] * 50)
    
    # Update text annotations
    current_time_hours = frame / 12
    current_glucose = df_simulation.cgm_Actual.iloc[frame] if frame < len(df_simulation) else 0
    current_insulin = df_simulation.input_insulin.iloc[frame] if frame < len(df_simulation) else 0
    current_hr = df_simulation.heart_rate.iloc[frame] if frame < len(df_simulation) else 0
    
    status, color, emoji = get_glucose_status(current_glucose)
    
    time_text.set_text(f'Time: {current_time_hours:.1f} hours\nFrame: {frame}/{len(df_simulation)}')
    status_text.set_text(f'{emoji} {status}\nGlucose: {current_glucose:.0f} mg/dL', color=color)
    param_text.set_text(f'Insulin: {current_insulin:.1f} U/h\nHeart Rate: {current_hr:.0f} BPM\nDigital Twin: {current_digital_twin}')
    
    # Update x-axis limits for scrolling effect
    if frame >= current_window:
        ax_main.set_xlim(frame - current_window, frame)
    else:
        ax_main.set_xlim(0, current_window)
    
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, line_hr, line_sleep, time_text, status_text, param_text

# Create animation
print("Creating interactive animation... This may take a moment...")
ani = FuncAnimation(fig, animate, init_func=init, frames=len(df_simulation), 
                   interval=current_speed, blit=True, repeat=True)

# Add controls
plt.tight_layout()

# Show the animation
print("Interactive animation ready!")
print("Controls:")
print("- Speed slider: Adjust animation speed")
print("- Window slider: Change time window size")
print("- Digital Twin slider: Switch between patients")
print("- Pause/Resume: Control animation")
print("- Reset: Go back to beginning")
print("- Jump: Enter time in hours to jump to")
plt.show() 