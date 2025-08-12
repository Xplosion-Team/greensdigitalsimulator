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
import gc  # Garbage collector
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import with error handling
try:
    from t1dsim_ai.individual_model import DigitalTwin
    DIGITAL_TWIN_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import DigitalTwin: {e}")
    DIGITAL_TWIN_AVAILABLE = False

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
    
    return current_scenario

def generate_plot(frame=None):
    """Generate the simulation plot with optional animation frame"""
    global current_scenario, current_digital_twin, animation_data
    
    try:
        if current_scenario is None:
            current_scenario = create_simple_scenario()
        
        if not DIGITAL_TWIN_AVAILABLE:
            # Create dummy data for testing
            time_hours = np.arange(60) / 12  # 5 hours
            cgm_actual = 110 + 20 * np.sin(time_hours * np.pi / 2.5) + np.random.normal(0, 5, 60)
            cgm_pop = 110 + 15 * np.sin(time_hours * np.pi / 2.5) + np.random.normal(0, 3, 60)
            cgm_dt = 110 + 18 * np.sin(time_hours * np.pi / 2.5) + np.random.normal(0, 4, 60)
            
            # Create the plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
            
            # Color scheme
            color_actual = "#8B4513"
            color_pop = "#20B2AA"
            color_dt = "#006400"
            color_insulin = "#FF6347"
            
            # Plot CGM data
            ax1.plot(time_hours, cgm_actual, color=color_actual, linewidth=2, label='Actual CGM (Test)')
            ax1.plot(time_hours, cgm_pop, color=color_pop, linewidth=2, label='Population Model (Test)')
            ax1.plot(time_hours, cgm_dt, color=color_dt, linewidth=2, label='Digital Twin (Test)')
            
            # Add target range and thresholds
            ax1.axhspan(70, 180, facecolor='#20B2AA', alpha=0.2, label='Target Range')
            ax1.axhline(y=70, color='#FF6347', alpha=0.7, linestyle='--', label='Hypo Threshold')
            ax1.axhline(y=180, color='#FF6347', alpha=0.7, linestyle='--', label='Hyper Threshold')
            
            ax1.set_xlabel('Time (hours)')
            ax1.set_ylabel('CGM (mg/dL)')
            ax1.set_title('CGM Simulation Results (Test Mode)')
            ax1.legend()
            ax1.grid(True, alpha=0.3, color='#E0E0E0')
            ax1.set_facecolor('#FAFAFA')
            
            # Plot insulin data
            insulin_data = np.ones(60) * scenario_params['basal_insulin']
            ax2.plot(time_hours, insulin_data, color=color_insulin, linewidth=2, label='Insulin')
            ax2.set_xlabel('Time (hours)')
            ax2.set_ylabel('Insulin (U/h)')
            ax2.set_title('Insulin Delivery')
            ax2.legend()
            ax2.grid(True, alpha=0.3, color='#E0E0E0')
            ax2.set_facecolor('#FAFAFA')
            
            # Add scenario info
            scenario_text = f'Test Mode: CGM={scenario_params["init_cgm"]} mg/dL, Basal={scenario_params["basal_insulin"]} U/h'
            fig.suptitle(f'Greens Health Simulator - Patient {current_digital_twin}\n{scenario_text}', 
                         fontsize=14, fontweight='bold', color='#8B4513')
            
            # Store animation data
            animation_data = {
                'time_hours': time_hours,
                'cgm_actual': cgm_actual,
                'cgm_pop': cgm_pop,
                'cgm_dt': cgm_dt,
                'insulin': insulin_data,
                'meal_mask': np.zeros(60, dtype=bool)
            }
            
        else:
            # Use real DigitalTwin
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
            
            # Plot CGM data
            ax1.plot(time_hours_plot, cgm_actual_plot, color=color_actual, linewidth=2, label='Actual CGM')
            ax1.plot(time_hours_plot, cgm_pop_plot, color=color_pop, linewidth=2, label='Population Model')
            ax1.plot(time_hours_plot, cgm_dt_plot, color=color_dt, linewidth=2, label='Digital Twin')
            
            # Add meal markers
            meal_times = time_hours_plot[meal_mask_plot]
            if len(meal_times) > 0:
                meal_carbs = df_simulation.input_meal_carbs.iloc[:len(meal_mask_plot)][meal_mask_plot]
                ax1.scatter(meal_times, [250] * len(meal_times), color=color_carbs, s=100, marker='d', 
                           label='Meals', zorder=5)
            
            # Add target range and thresholds
            ax1.axhspan(70, 180, facecolor='#20B2AA', alpha=0.2, label='Target Range')
            ax1.axhline(y=70, color='#FF6347', alpha=0.7, linestyle='--', label='Hypo Threshold')
            ax1.axhline(y=180, color='#FF6347', alpha=0.7, linestyle='--', label='Hyper Threshold')
            ax1.axhline(y=250, color='#F0E68C', alpha=0.7, linestyle='--', label='High Threshold')
            
            ax1.set_xlabel('Time (hours)')
            ax1.set_ylabel('CGM (mg/dL)')
            ax1.set_title('CGM Simulation Results')
            ax1.legend()
            ax1.grid(True, alpha=0.3, color='#E0E0E0')
            ax1.set_facecolor('#FAFAFA')
            
            # Plot insulin data
            ax2.plot(time_hours_plot, insulin_plot, color=color_insulin, linewidth=2, label='Insulin')
            ax2.set_xlabel('Time (hours)')
            ax2.set_ylabel('Insulin (U/h)')
            ax2.set_title('Insulin Delivery')
            ax2.legend()
            ax2.grid(True, alpha=0.3, color='#E0E0E0')
            ax2.set_facecolor('#FAFAFA')
            
            # Add scenario info
            scenario_text = f'Scenario: CGM={scenario_params["init_cgm"]} mg/dL, Basal={scenario_params["basal_insulin"]} U/h, Meal={scenario_params["meal_size"]}g at {scenario_params["meal_time"]}min'
            fig.suptitle(f'Greens Health Simulator - Patient {current_digital_twin}\n{scenario_text}', 
                         fontsize=14, fontweight='bold', color='#8B4513')  # Dark Reddish Brown title
        
        # Adjust layout
        plt.tight_layout()
        fig.patch.set_facecolor('#FAFAFA')  # Light gray
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight', facecolor='#FAFAFA')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        # Force garbage collection
        gc.collect()
        
        return f'data:image/png;base64,{plot_url}'
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        # Return error plot
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.text(0.5, 0.5, f'Error: {str(e)}', ha='center', va='center', transform=ax.transAxes, fontsize=16)
        ax.set_title('Error Loading Plot')
        
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return f'data:image/png;base64,{plot_url}'

@app.route('/')
def index():
    try:
        print("Index route called")
        plot_url = generate_plot()
        print(f"Plot generated successfully")
        return render_template('index.html', plot_url=plot_url, params=scenario_params, digital_twin=current_digital_twin)
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'Greens Health Simulator is running',
        'digital_twin_available': DIGITAL_TWIN_AVAILABLE
    })

@app.route('/update_scenario', methods=['POST'])
def update_scenario():
    """Update scenario parameters and regenerate plot"""
    global current_scenario
    
    try:
        data = request.get_json()
        
        # Update scenario parameters
        if 'init_cgm' in data:
            scenario_params['init_cgm'] = float(data['init_cgm'])
        if 'basal_insulin' in data:
            scenario_params['basal_insulin'] = float(data['basal_insulin'])
        if 'carb_ratio' in data:
            scenario_params['carb_ratio'] = float(data['carb_ratio'])
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
    except Exception as e:
        print(f"Error in update_scenario: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_stats')
def get_stats():
    """Get simulation statistics"""
    try:
        if not DIGITAL_TWIN_AVAILABLE:
            # Return dummy stats
            return jsonify({
                'actual': {'mean': 120.5, 'max': 180.0, 'min': 80.0, 'time_in_range': 85.0},
                'population': {'mean': 118.2, 'max': 175.0, 'min': 82.0, 'time_in_range': 87.0},
                'digital_twin': {'mean': 119.8, 'max': 178.0, 'min': 81.0, 'time_in_range': 86.0}
            })
        
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
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Greens Health Simulator...")
    print(f"DigitalTwin available: {DIGITAL_TWIN_AVAILABLE}")
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 