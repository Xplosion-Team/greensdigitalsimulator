from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from t1dsim_ai.individual_model import DigitalTwin
import json
import time

app = Flask(__name__)

# Global variables
current_digital_twin = 4
current_scenario = None
animation_frame = 0
animation_data = None

# Scenario parameters
scenario_params = {
    'init_cgm': 110,
    'basal_insulin': 1.0,
    'carb_ratio': 12,
    'meal_size': 75,
    'meal_time': 60,
    'heart_rate': 70
}

def create_simple_scenario():
    """Create a simple scenario DataFrame"""
    global current_scenario
    
    # Create a simple scenario DataFrame
    sim_time = 5 * 60  # 5 hours
    n_points = sim_time // 5  # 5-minute intervals
    
    # Create time array
    base_date = datetime(2024, 8, 15, 8, 0, 0)  # Start at 8 AM
    time_range = pd.date_range(base_date, periods=n_points, freq='5 min')
    
    # Create scenario DataFrame
    current_scenario = pd.DataFrame()
    current_scenario['time'] = time_range
    
    # Initialize all columns to 0
    current_scenario['output_cgm'] = 0.0
    current_scenario['input_insulin'] = scenario_params['basal_insulin']
    current_scenario['input_meal_carbs'] = 0.0
    current_scenario['heart_rate'] = scenario_params['heart_rate']
    current_scenario['sleep_efficiency'] = 0.0
    current_scenario['feat_hour_of_day_cos'] = np.cos(2 * np.pi * current_scenario['time'].dt.hour / 24)
    current_scenario['feat_hour_of_day_sin'] = np.sin(2 * np.pi * current_scenario['time'].dt.hour / 24)
    current_scenario['feat_is_weekend'] = 0.0
    current_scenario['heart_rate_WRTbaseline'] = 0.0
    
    # Set initial CGM
    current_scenario.loc[0, 'output_cgm'] = scenario_params['init_cgm']
    
    # Add meal at specified time
    meal_idx = scenario_params['meal_time'] // 5
    if meal_idx < len(current_scenario):
        current_scenario.loc[meal_idx, 'input_meal_carbs'] = scenario_params['meal_size']
        # Add bolus insulin for meal
        bolus_insulin = scenario_params['meal_size'] / scenario_params['carb_ratio']
        current_scenario.loc[meal_idx, 'input_insulin'] = scenario_params['basal_insulin'] + bolus_insulin
    
    # Add sleep period (10 PM to 6 AM)
    sleep_start = 14 * 12  # 10 PM (14 hours from 8 AM)
    sleep_end = 22 * 12    # 6 AM (22 hours from 8 AM)
    if sleep_start < len(current_scenario):
        end_idx = min(sleep_end, len(current_scenario))
        current_scenario.loc[sleep_start:end_idx, 'sleep_efficiency'] = 1.0
        current_scenario.loc[sleep_start:end_idx, 'heart_rate'] = scenario_params['heart_rate'] - 10
    
    return current_scenario

def generate_plot(frame=None):
    """Generate the simulation plot with optional animation frame"""
    global current_scenario, current_digital_twin, animation_data
    
    if current_scenario is None:
        current_scenario = create_simple_scenario()
    
    # Simulate the scenario with current digital twin
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Store animation data for frame-by-frame access
    animation_data = {
        'time_hours': np.arange(len(df_simulation)) / 12,
        'cgm_actual': df_simulation.cgm_Actual.values,
        'cgm_pop': df_simulation.cgm_NNPop.values,
        'cgm_dt': df_simulation.cgm_NNDT.values,
        'insulin': df_simulation.input_insulin.values,
        'meal_mask': df_simulation.input_meal_carbs != 0
    }
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
    
    # Color scheme - Diverse palette for better distinction
    color_actual = "#8B4513"  # Dark Reddish Brown (from palette)
    color_pop = "#20B2AA"     # Medium Green/Teal (from palette)
    color_dt = "#006400"      # Dark Teal/Green (from palette)
    color_insulin = "#FF6347" # Vibrant Orange-Red (from palette)
    color_carbs = "#F0E68C"   # Light Yellow/Cream (from palette)
    
    # Time array for x-axis
    time_hours = animation_data['time_hours']
    
    # Determine data range for animation
    if frame is not None and frame < len(time_hours):
        end_idx = frame + 1
        time_hours_plot = time_hours[:end_idx]
        cgm_actual_plot = animation_data['cgm_actual'][:end_idx]
        cgm_pop_plot = animation_data['cgm_pop'][:end_idx]
        cgm_dt_plot = animation_data['cgm_dt'][:end_idx]
        insulin_plot = animation_data['insulin'][:end_idx]
        meal_mask_plot = animation_data['meal_mask'][:end_idx]
    else:
        time_hours_plot = time_hours
        cgm_actual_plot = animation_data['cgm_actual']
        cgm_pop_plot = animation_data['cgm_pop']
        cgm_dt_plot = animation_data['cgm_dt']
        insulin_plot = animation_data['insulin']
        meal_mask_plot = animation_data['meal_mask']
    
    # Plot glucose data
    ax1.plot(time_hours_plot, cgm_actual_plot, 'o-', color=color_actual, ms=3, lw=1, label='Actual CGM')
    ax1.plot(time_hours_plot, cgm_pop_plot, 'o-', color=color_pop, ms=2, lw=1, label='Population Model')
    ax1.plot(time_hours_plot, cgm_dt_plot, 'o-', color=color_dt, ms=2, lw=1, label='Digital Twin')
    
    # Add meal markers
    if meal_mask_plot.any():
        meal_times = time_hours_plot[meal_mask_plot]
        # Get meal carbs for the current window only
        meal_carbs = df_simulation.input_meal_carbs.iloc[:len(meal_mask_plot)][meal_mask_plot]
        ax1.scatter(meal_times, [350] * len(meal_times), c=color_carbs, s=100, marker='^', label='Meals')
        for i, (t, carbs) in enumerate(zip(meal_times, meal_carbs)):
            ax1.annotate(f'{carbs}g', (t, 350), xytext=(0, 10), textcoords='offset points', 
                        ha='center', fontsize=8, fontweight='bold')
    
    # Setup glucose plot
    ax1.set_ylim(40, 380)
    ax1.set_ylabel('CGM [mg/dL]', fontweight='bold')
    ax1.grid(True, alpha=0.3, color='#E0E0E0')  # Light gray grid
    ax1.axhspan(70, 180, facecolor='#20B2AA', alpha=0.2, label='Target Range')  # Teal target range
    ax1.axhline(y=70, color='#FF6347', alpha=0.7, linestyle='--', lw=2)  # Orange-red warning line
    ax1.axhline(y=180, color='#FF6347', alpha=0.7, linestyle='--', lw=2)  # Orange-red warning line
    ax1.axhline(y=250, color='#F0E68C', alpha=0.7, linestyle='--', lw=2)  # Cream high line
    ax1.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax1.set_facecolor('#FAFAFA')  # Light gray background
    
    # Plot insulin data
    ax2.plot(time_hours_plot, insulin_plot, color=color_insulin, lw=2, label='Insulin [U/h]')
    ax2.set_ylabel('Insulin [U/h]', fontweight='bold')
    ax2.set_xlabel('Time [hours]', fontweight='bold')
    ax2.grid(True, alpha=0.3, color='#E0E0E0')  # Light gray grid
    ax2.legend()
    ax2.set_facecolor('#FAFAFA')  # Light gray background
    
    # Add scenario info
    scenario_text = f'Scenario: CGM={scenario_params["init_cgm"]} mg/dL, Basal={scenario_params["basal_insulin"]} U/h, Meal={scenario_params["meal_size"]}g at {scenario_params["meal_time"]}min'
    fig.suptitle(f'Greens Health Simulator - Patient {current_digital_twin}\n{scenario_text}', 
                 fontsize=14, fontweight='bold', color='#8B4513')  # Dark Reddish Brown title
    
    # Set figure background
    fig.patch.set_facecolor('#FAFAFA')  # Light gray background
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/')
def index():
    """Main page"""
    plot_url = generate_plot()
    return render_template('index.html', plot_url=plot_url, params=scenario_params, digital_twin=current_digital_twin)

@app.route('/update_scenario', methods=['POST'])
def update_scenario():
    """Update scenario parameters"""
    global scenario_params, current_scenario
    
    data = request.get_json()
    
    # Update parameters
    if 'init_cgm' in data:
        scenario_params['init_cgm'] = float(data['init_cgm'])
    if 'basal_insulin' in data:
        scenario_params['basal_insulin'] = float(data['basal_insulin'])
    if 'meal_size' in data:
        scenario_params['meal_size'] = float(data['meal_size'])
    if 'meal_time' in data:
        scenario_params['meal_time'] = float(data['meal_time'])
    if 'digital_twin' in data:
        global current_digital_twin
        current_digital_twin = int(data['digital_twin'])
    
    # Create new scenario
    current_scenario = None
    plot_url = generate_plot()
    
    return jsonify({
        'plot_url': plot_url,
        'params': scenario_params,
        'digital_twin': current_digital_twin
    })

@app.route('/get_stats')
def get_stats():
    """Get simulation statistics"""
    global current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = create_simple_scenario()
    
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Calculate statistics
    actual_glucose = df_simulation.cgm_Actual
    pop_glucose = df_simulation.cgm_NNPop
    dt_glucose = df_simulation.cgm_NNDT
    
    stats = {
        'actual': {
            'mean': float(round(actual_glucose.mean(), 1)),
            'max': float(round(actual_glucose.max(), 1)),
            'min': float(round(actual_glucose.min(), 1)),
            'time_in_range': float(round(((actual_glucose >= 70) & (actual_glucose <= 180)).sum() / len(actual_glucose) * 100, 1))
        },
        'population': {
            'mean': float(round(pop_glucose.mean(), 1)),
            'max': float(round(pop_glucose.max(), 1)),
            'min': float(round(pop_glucose.min(), 1)),
            'time_in_range': float(round(((pop_glucose >= 70) & (pop_glucose <= 180)).sum() / len(pop_glucose) * 100, 1))
        },
        'digital_twin': {
            'mean': float(round(dt_glucose.mean(), 1)),
            'max': float(round(dt_glucose.max(), 1)),
            'min': float(round(dt_glucose.min(), 1)),
            'time_in_range': float(round(((dt_glucose >= 70) & (dt_glucose <= 180)).sum() / len(dt_glucose) * 100, 1))
        }
    }
    
    return jsonify(stats)

@app.route('/get_animation_frame/<int:frame>')
def get_animation_frame(frame):
    """Get animation frame"""
    global animation_frame
    animation_frame = frame
    plot_url = generate_plot(frame)
    return jsonify({'plot_url': plot_url, 'frame': frame})

@app.route('/start_animation')
def start_animation():
    """Start animation sequence"""
    global animation_frame
    animation_frame = 0
    return jsonify({'status': 'started', 'frame': animation_frame})

@app.route('/get_animation_data')
def get_animation_data():
    """Get animation data for client-side animation"""
    global animation_data, current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = create_simple_scenario()
    
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Prepare data for client-side animation
    time_hours = np.arange(len(df_simulation)) / 12
    animation_data = {
        'time_hours': time_hours.tolist(),
        'cgm_actual': df_simulation.cgm_Actual.tolist(),
        'cgm_pop': df_simulation.cgm_NNPop.tolist(),
        'cgm_dt': df_simulation.cgm_NNDT.tolist(),
        'insulin': df_simulation.input_insulin.tolist(),
        'meal_times': time_hours[df_simulation.input_meal_carbs != 0].tolist(),
        'meal_carbs': df_simulation.input_meal_carbs[df_simulation.input_meal_carbs != 0].tolist(),
        'total_frames': len(time_hours)
    }
    
    return jsonify(animation_data)

if __name__ == '__main__':
    print("Starting Greens Health Simulator...")
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 