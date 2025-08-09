import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, CheckButtons
from t1dsim_ai.individual_model import DigitalTwin
from t1dsim_ai.create_scenarios import digitalTwin_scenario
import datetime

# Global variables for interactive control
current_digital_twin = 4
current_speed = 50
animation_running = True
current_scenario = None

# Setup the figure with extra space for controls
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Interactive T1D Digital Twin - Scenario Creator', fontsize=16, fontweight='bold')

# Create subplots with different sizes
ax_main = plt.subplot2grid((6, 4), (0, 0), colspan=3, rowspan=3)  # Main plot
ax_control = plt.subplot2grid((6, 4), (3, 0), colspan=4, rowspan=1)  # Control panel
ax_scenario = plt.subplot2grid((6, 4), (0, 3), rowspan=2)  # Scenario panel
ax_params = plt.subplot2grid((6, 4), (2, 3), rowspan=1)  # Parameter panel
ax_meals = plt.subplot2grid((6, 4), (4, 0), colspan=2, rowspan=2)  # Meal input panel
ax_insulin = plt.subplot2grid((6, 4), (4, 2), colspan=2, rowspan=2)  # Insulin input panel

# Color scheme
color_actual = "#000000"
color_pop = "#009E73"
color_dt = "#0072B2"
color_insulin = "#FF6B6B"
color_carbs = "#FFA500"
color_hr = "#32CD32"
color_sleep = "#9370DB"

# Initialize empty lines for animation
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

# Setup scenario panel
ax_scenario.set_xlim(0, 1)
ax_scenario.set_ylim(0, 1)
ax_scenario.axis('off')

# Setup parameter panel
ax_params.set_xlim(0, 1)
ax_params.set_ylim(0, 1)
ax_params.axis('off')

# Setup meal input panel
ax_meals.set_xlim(0, 1)
ax_meals.set_ylim(0, 1)
ax_meals.axis('off')

# Setup insulin input panel
ax_insulin.set_xlim(0, 1)
ax_insulin.set_ylim(0, 1)
ax_insulin.axis('off')

# Add text annotations
time_text = ax_main.text(0.02, 0.95, '', transform=ax_main.transAxes, fontsize=12, 
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
glucose_text = ax_main.text(0.02, 0.85, '', transform=ax_main.transAxes, fontsize=10,
                            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

scenario_text = ax_scenario.text(0.1, 0.8, 'Current Scenario', transform=ax_scenario.transAxes, 
                                 fontsize=14, fontweight='bold')
param_text = ax_params.text(0.1, 0.8, 'Parameters', transform=ax_params.transAxes, 
                            fontsize=12, fontweight='bold')

# Scenario parameters
scenario_params = {
    'init_cgm': 110,
    'basal_insulin': 1.0,
    'carb_ratio': 12,
    'meal_size': 75,
    'meal_time': 60,
    'heart_rate': 70,
    'sleep_duration': 8,
    'bedtime': 13 * 60
}

# Function to create new scenario
def create_scenario():
    global current_scenario
    current_scenario = digitalTwin_scenario(
        meal_size_array=[scenario_params['meal_size']],
        meal_time_fromStart_array=[scenario_params['meal_time']],
        init_cgm=scenario_params['init_cgm'],
        basal_insulin=scenario_params['basal_insulin'],
        carb_ratio=scenario_params['carb_ratio'],
        sim_time=5 * 60,  # 5 hours
        hr=scenario_params['heart_rate'],
        bedtime=scenario_params['bedtime'],
        sleep_duration=scenario_params['sleep_duration']
    )
    print("New scenario created!")

# Function to update digital twin
def update_digital_twin(val):
    global current_digital_twin
    current_digital_twin = int(val)
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

# Function to create new scenario
def create_new_scenario(event):
    create_scenario()
    print("Scenario updated!")

# Function to update initial CGM
def update_init_cgm(text):
    try:
        scenario_params['init_cgm'] = float(text)
        print(f"Initial CGM set to {scenario_params['init_cgm']} mg/dL")
    except ValueError:
        print("Invalid CGM value")

# Function to update basal insulin
def update_basal_insulin(text):
    try:
        scenario_params['basal_insulin'] = float(text)
        print(f"Basal insulin set to {scenario_params['basal_insulin']} U/h")
    except ValueError:
        print("Invalid insulin value")

# Function to update meal size
def update_meal_size(text):
    try:
        scenario_params['meal_size'] = float(text)
        print(f"Meal size set to {scenario_params['meal_size']} g")
    except ValueError:
        print("Invalid meal size")

# Function to update meal time
def update_meal_time(text):
    try:
        scenario_params['meal_time'] = float(text)
        print(f"Meal time set to {scenario_params['meal_time']} minutes")
    except ValueError:
        print("Invalid meal time")

# Create sliders
ax_speed = plt.axes([0.15, 0.05, 0.15, 0.03])
ax_dt = plt.axes([0.35, 0.05, 0.15, 0.03])

speed_slider = Slider(ax_speed, 'Speed (ms)', 10, 200, valinit=current_speed, valstep=10)
dt_slider = Slider(ax_dt, 'Digital Twin', 0, 4, valinit=current_digital_twin, valstep=1)

# Create buttons
ax_pause = plt.axes([0.55, 0.05, 0.08, 0.04])
ax_reset = plt.axes([0.65, 0.05, 0.08, 0.04])
ax_scenario_btn = plt.axes([0.75, 0.05, 0.12, 0.04])

pause_button = Button(ax_pause, 'Pause')
reset_button = Button(ax_reset, 'Reset')
scenario_button = Button(ax_scenario_btn, 'Create Scenario')

# Create text boxes for parameters
ax_cgm = plt.axes([0.15, 0.02, 0.12, 0.02])
ax_ins = plt.axes([0.30, 0.02, 0.12, 0.02])
ax_meal = plt.axes([0.45, 0.02, 0.12, 0.02])
ax_time = plt.axes([0.60, 0.02, 0.12, 0.02])

cgm_textbox = TextBox(ax_cgm, 'Init CGM: ', initial=str(scenario_params['init_cgm']))
insulin_textbox = TextBox(ax_ins, 'Basal Insulin: ', initial=str(scenario_params['basal_insulin']))
meal_textbox = TextBox(ax_meal, 'Meal (g): ', initial=str(scenario_params['meal_size']))
time_textbox = TextBox(ax_time, 'Meal Time (min): ', initial=str(scenario_params['meal_time']))

# Connect sliders and buttons
speed_slider.on_changed(update_speed)
dt_slider.on_changed(update_digital_twin)
pause_button.on_clicked(toggle_animation)
reset_button.on_clicked(reset_animation)
scenario_button.on_clicked(create_new_scenario)

# Connect text boxes
cgm_textbox.on_submit(update_init_cgm)
insulin_textbox.on_submit(update_basal_insulin)
meal_textbox.on_submit(update_meal_size)
time_textbox.on_submit(update_meal_time)

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
    global current_scenario
    # Create initial scenario
    if current_scenario is None:
        create_scenario()
    
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
    global animation_running, current_scenario
    
    if not animation_running or current_scenario is None:
        return line_actual, line_pop, line_dt, line_insulin, line_carbs, time_text, glucose_text
    
    # Simulate the scenario with current digital twin
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Calculate window start and end (show last 4 hours)
    window_size = 48  # 4 hours * 12 frames per hour
    start_idx = max(0, frame - window_size)
    end_idx = frame + 1
    
    # Get time window data
    time = np.arange(len(df_simulation))
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
    
    status, color = get_glucose_status(current_glucose)
    
    time_text.set_text(f'Time: {current_time_hours:.1f} hours | Frame: {frame}/{len(df_simulation)}')
    glucose_text.set_text(f'{status} | Glucose: {current_glucose:.0f} mg/dL | Insulin: {current_insulin:.1f} U/h')
    glucose_text.set_color(color)
    
    # Update scenario info
    scenario_text.set_text(f'Scenario:\nCGM: {scenario_params["init_cgm"]} mg/dL\nBasal: {scenario_params["basal_insulin"]} U/h\nMeal: {scenario_params["meal_size"]}g at {scenario_params["meal_time"]}min')
    param_text.set_text(f'Digital Twin: {current_digital_twin}\nSpeed: {current_speed}ms\nStatus: {"Running" if animation_running else "Paused"}')
    
    # Update x-axis limits for scrolling effect
    if frame >= window_size:
        ax_main.set_xlim(frame - window_size, frame)
    else:
        ax_main.set_xlim(0, window_size)
    
    return line_actual, line_pop, line_dt, line_insulin, line_carbs, time_text, glucose_text

# Create animation
print("Creating scenario-based interactive animation... This may take a moment...")
ani = FuncAnimation(fig, animate, init_func=init, frames=300,  # 5 hours * 60 minutes / 5-minute intervals
                   interval=current_speed, blit=True, repeat=True)

# Add controls
plt.tight_layout()

# Show the animation
print("Scenario-based interactive animation ready!")
print("Controls:")
print("- Speed slider: Adjust animation speed (10-200ms)")
print("- Digital Twin slider: Switch between patients (0-4)")
print("- Pause/Resume: Control animation playback")
print("- Reset: Go back to beginning")
print("- Create Scenario: Generate new scenario with current parameters")
print("- Text boxes: Modify initial CGM, basal insulin, meal size, and meal time")
plt.show() 